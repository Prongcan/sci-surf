# Orchestrator 逻辑说明

本文档说明 PaperIgnition 当前 orchestrator 的数据流和执行逻辑，涵盖论文抓取、存储、推荐、博客生成以及用户 persona 生成。

## 1. 总体流程

生产配置位于 `orchestrator/configs/production.yaml`，主流程位于 `orchestrator/orchestrator.py`。

默认执行顺序如下：

```text
用户 persona 更新
       |
       v
从 arXiv 抓取论文并入库
       |
       v
根据用户兴趣检索候选论文
       |
       v
LLM 重排候选论文
       |
       v
生成个性化博客
       |
       v
保存用户推荐结果
```

`run_all_tasks()` 按以下 stage 顺序执行：

1. `extract_user_profiles`
2. `fetch_daily_papers`
3. `generate_per_user_blogs`

stage 可以通过命令行 `--stages` 覆盖配置。

## 2. 每日论文抓取

### 2.1 抓取时间窗口

`PaperPullService` 负责从 arXiv 抓取论文。生产配置当前使用：

```yaml
paper_pull:
  location: cloud
  count_delay: 2
  time_slots_count: 5
  max_workers: 1
```

- `location: cloud` 使用 UTC。
- `count_delay: 2` 抓取约两天前的 24 小时数据。
- 24 小时被拆成 5 个时间段，避免 arXiv API 限流。
- 时间段之间等待 30 秒。
- 只抓取 `cs.*` 类别，具体查询由 `ArxivClient` 执行。

### 2.2 去重

抓取开始前，orchestrator 从 RDS 的 `papers` 表读取所有 `doc_id`，设置为 `exclude_ids`。arXiv 返回结果中已经存在的论文会被跳过。

因此，full mode 只会对新抓到的论文执行内容提取，不会自动重新处理历史论文。

### 2.3 lazy mode 和 full mode

当前生产配置是：

```yaml
lazy_mode: false
```

#### lazy mode

```text
arXiv 元数据 -> papers 表 -> embedding
```

只保存标题、作者、abstract、分类和日期等元数据。正文提取延迟到论文被推荐时。

#### full mode

```text
arXiv 元数据
    -> 下载 PDF
    -> Baidu OCR 提取正文、图片、表格
    -> 保存 PDF/JSON
    -> 写入 RDS
    -> 生成 embedding
    -> 上传图片到 OSS
```

full mode 依赖 `BAIDU_OCR_URL` 和 `BAIDU_OCR_TOKEN`。如果 OCR 凭据不存在，任务仍可能抓取元数据，但正文、图片和表格提取会被跳过。

## 3. 论文存储

### 3.1 RDS 表

论文元数据写入 `papers` 表，主要字段包括：

- `doc_id`
- `title`
- `authors`
- `abstract`
- `categories`
- `published_date`
- `pdf_path`
- `HTML_path`
- `blog`

正文分块写入 `text_chunks` 表，每个 chunk 包含论文 ID、chunk ID、文本内容和顺序。

向量写入 `paper_embeddings` 表：

- `doc_id`
- `title`
- `abstract`
- `embedding`
- `updated_at`

embedding 使用 DashScope `text-embedding-v4`，维度为 1536，批量大小当前为 10。

### 3.2 本地文件和 OSS

orchestrator 的本地存储目录通常位于 `orchestrator/orchestrator/` 下：

```text
pdfs/              下载的论文 PDF
jsons/             DocSet JSON（当前配置不保留 JSON）
imgs/              提取的论文图片
blogsByGemini/     生成的 Markdown 博客
```

full mode 且 `store_images_on_index: true` 时，图片还会上传到 OSS。

## 4. 推荐逻辑

推荐逻辑由 `blog_generation_for_all_users()` 执行。

### 4.1 用户范围

默认处理最近 30 天登录过的用户。配置中可以通过 `active_days` 调整。

程序还会尝试加入 `Demo User`。用户名为 `BlogBot@gmail.com` 的用户会被跳过。

### 4.2 用户兴趣和 persona

orchestrator 从 backend 获取：

```python
query, profile = backend_client.get_user_search_context(username)
```

- `query`：用户研究兴趣文本，用于向量检索。
- `profile`：用户 persona JSON，用于个性化重排。

没有研究兴趣的用户会跳过推荐。

### 4.3 候选检索

当前生产配置：

```yaml
user_recommendation:
  retrieve_k: 20
  top_k: 5
  similarity_cutoff: 0.1
  search_strategy: vector
  search_days: 5
  user_retrieve_result: true
```

执行步骤：

1. 以用户研究兴趣生成 query embedding。
2. 调用 backend 的 pgvector 搜索接口。
3. 限制论文发布日期在最近 5 天内。
4. 排除该用户已经推荐过的论文。
5. 取得最多 20 篇候选论文，过滤相似度低于 0.1 的结果。
6. 保存 20 篇候选 ID 和最终选中的论文 ID 到 `user_retrieve_results`。

### 4.4 LLM 重排

当前配置：

```yaml
customized_recommendation: true
use_pdf_reranker: false
```

因此当前使用 abstract/text 重排器：

- 模型：`gpt-6-luna`
- 输入：候选论文的标题和 abstract
- 输出：候选论文 ID 的排序结果
- 最终选择：前 5 篇

PDF 重排器仍然保留在代码中，但当前未启用。启用时会上传每篇候选论文的第一页 PDF，耗时和超时风险更高。

### 4.5 推荐结果保存

最终论文会逐条提交到 backend 的推荐接口，并写入用户推荐记录。每条记录包含：

- 用户名
- 论文 ID、标题、作者、abstract
- 论文 URL
- 博客内容
- 推荐理由
- 相关度分数
- 论文提交日期

## 5. Blog 生成逻辑

博客生成发生在推荐重排之后，只针对最终选中的论文执行。

### 5.1 当前输入格式

当前主流程仍使用 PDF 输入：

```text
下载 PDF
    -> base64 编码
    -> Responses API input_file
    -> 附加博客 prompt
    -> 生成 Markdown
```

请求使用：

- 模型：`gpt-6-luna`
- endpoint：环境变量 `BASE_URL`
- API key：环境变量 `OPENAI_API_KEY`
- PDF detail：`high`
- 默认超时：180 秒，可由 `OPENAI_TIMEOUT_SECONDS` 覆盖
- SDK 自动重试：关闭，generator 自己负责重试

### 5.2 并发和重试

博客 generator 当前最多并发处理 2 篇论文。每篇论文最多重试 5 次，并使用递增等待时间。

并发数从原来的最多 50 降为 2，是因为真实 PDF 请求通常需要几十秒到两分钟，过高并发会导致网关超时。

### 5.3 输出和回写

成功响应会保存为：

```text
orchestrator/orchestrator/blogsByGemini/{paper_id}.md
```

随后 orchestrator 读取 Markdown 内容，并把博客内容和推荐元数据一起提交到 backend。

需要注意：generator 会吞掉单篇论文的异常并继续处理其他论文。因此 orchestrator 的整体 job 可能显示成功，但某些 Markdown 文件实际没有生成。检查结果时应同时检查：

1. blog 目录中的 Markdown 文件；
2. backend 推荐接口返回值；
3. `paper_recommendations` 表中的 blog 字段。

### 5.4 文本输入支持状态

底层 generator 和 `text_prompts.yaml` 已支持 `input_format: text`，但 orchestrator 当前没有完整接通这条链路：

- 推荐搜索结果转换成 `DocSet` 时，`text_chunks` 目前被初始化为空。
- orchestrator 调用博客 generator 时没有传递 `input_format: text`。
- 推荐阶段仍会尝试准备 PDF。

因此当前实际生产路径仍是 PDF 博客生成。

## 6. 用户 persona 生成

persona 生成不是对所有用户每日执行，而是只处理 backend 标记为：

```text
profile_boost_requested = true
```

入口是 `run_extract_user_profiles()`。

### 6.1 历史数据准备

对于目标用户：

1. 读取最多 1000 条历史推荐。
2. 按 `recommendation_date` 分组为多个 session。
3. 只保留至少包含一篇点赞论文的日期。
4. 点赞论文标记为 `label=1`。
5. 展示但未点赞的论文标记为 `label=0`。
6. 下载这些论文的 PDF。

如果没有推荐历史、没有点赞 session 或 PDF 全部下载失败，则跳过 persona 生成。

### 6.2 单 persona 提取

当 profile pool 被禁用，或有效 session 少于 10 天时，使用单次 profile extraction。

模型根据用户喜欢和不喜欢的论文输出 JSON：

```json
{
  "persona_definition": "...",
  "negative_constraints": ["..."],
  "ranking_heuristics": ["..."]
}
```

当前使用 `gpt-6-luna`，输入主要是历史论文的第一页 PDF。

### 6.3 Profile pool 优化

当前配置：

```yaml
profile_pool:
  enabled: true
  pool_size: 3
  max_mutations_per_cycle: 2
  max_val_days: 5
  max_papers: 20
  min_days_for_pool: 10
  fallback_to_single_profile: true
```

达到至少 10 个有效 session 时：

1. 读取已有 persona pool。
2. 使用新 session 作为训练数据。
3. 使用历史 session 组成验证集合。
4. 初始化或变异多个 persona 候选。
5. 用推荐重排器评估候选 persona。
6. 计算 precision、recall 和 F1。
7. 选择 Pareto 前沿中 F1 最高的候选作为 active profile。
8. 保存整个 pool 和 active profile。
9. 写入 profile boost history。

如果 pool 优化失败且 `fallback_to_single_profile=true`，会回退到单 persona 提取。

## 7. 运行状态和已知限制

当前生产配置和实现的关键状态：

- 论文抓取：full mode。
- 推荐重排：abstract/text 模式，不使用 PDF 重排。
- 博客生成：仍使用 PDF input_file。
- persona：使用历史点赞/未点赞记录和 PDF 首页面。
- LLM：OpenAI 兼容 Responses API，模型为 `gpt-6-luna`。
- embedding：DashScope `text-embedding-v4`，1536 维。
- 每日调度：orchestrator 本身没有内置 scheduler，需手动执行或由外部 cron/systemd 调用。
- full mode 只处理新论文；已有论文不会因为切换配置而自动补正文。
- API 请求成功、博客生成成功和推荐数据持久化是三个不同结果，需要分别核验。


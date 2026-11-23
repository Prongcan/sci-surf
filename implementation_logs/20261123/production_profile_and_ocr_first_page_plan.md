# GeminiRerankerPDF 生产推荐与 Boost OCR 首页改造计划

日期：2026-11-23。状态：待审核，本文仅记录计划。

## 现状

- 已生成的 Profile 通过 `POST /api/users/boost-complete/{username}` 保存在用户库 `users.profile_json`，字段包括 `persona_definition`、`negative_constraints`、`ranking_heuristics`。
- `BackendAPIClient.get_user_search_context()` 在推荐时返回查询和 `profile_json`。生产配置现为 `customized_recommendation: true`、`use_pdf_reranker: true`，因此推荐使用 `GeminiRerankerPDF`；现有调用已经传入 Profile。
- 两个开关分别控制是否启用 rerank、启用后选择哪一类：`customized_recommendation: false` 不创建 reranker；`true` 且 `use_pdf_reranker: true` 选择 `GeminiRerankerPDF`；`true` 且 `use_pdf_reranker: false` 选择 `GeminiReranker`。Boost 的 pool 评估另行实例化 `GeminiRerankerPDF`，不受此推荐开关控制。
- `GeminiRerankerPDF` 初始化时读取 `personalized_ranking_prompt`，在 `rerank()` 收到非 `None` 的 `user_profile` 时填入用户兴趣、persona、negative constraints、ranking heuristics，并连同论文首页 PDF 发给模型。Profile pool 的评估路径复用该类，提示词为 `personalized_subset_selection_prompt`。
- 生产配置 `paper_pull.lazy_mode: true`：新论文先存元数据与摘要，候选论文在 rerank 时通常还没有 OCR 正文；只有选中的论文随后才做 OCR。因此不能仅把生产推荐的候选 PDF 读取替换为数据库 OCR 查询，否则新候选会因缺页而无法正常排序。
- Boost 当前按推荐日期组装 session：当天至少一篇 `blog_liked is True` 才参与；其他 `blog_liked is not True`（包括 `False` 和 `NULL`）作为 contextual alternatives。然后从 arXiv 下载涉及的 PDF，抽取首页，执行单 Profile 提取或 Profile pool 优化，最后通过现有接口保存。

## 已完成配置调整：下一轮生产推荐使用 GeminiRerankerPDF

1. `orchestrator/configs/production.yaml` 的 `use_pdf_reranker` 已设为 `true`。下一轮使用该配置的生产推荐将下载候选论文 PDF，并把首页 PDF 与已保存 Profile 交给 `GeminiRerankerPDF`。无需修改 `GeminiReranker`。
2. 现有 PDF rerank 调用已传入 `user_profile=profile`；Profile 存在时使用 `personalized_ranking_prompt`。该生产调用仍使用 PDF 输入，避免改变 lazy 模式的检索与 OCR 时序。当前最终论文列表沿原始检索顺序组织；本计划不调整展示顺序。

## 待实施：Boost 的首页来源改为论文库 OCR 正文

1. 在 `orchestrator/storage_util.py` 的 `RDSDBManager` 增加批量只读查询：按 Boost 已选的 `all_paper_ids` 查询论文库 `text_chunks`，取 `chunk_order = 0` 且非空的 `text_content`，返回 `paper_id -> OCR 首页文字`。参考 `scripts/profile_from_ocr_feedback.py` 的现有 SQL；不调用 OCR 服务。
2. 在 `orchestrator/orchestrator.py` 的 `run_extract_user_profiles()` 中，用该查询替换 arXiv 下载循环和临时 PDF 目录。保持 `get_user_papers(limit=1000)`、按日期分组、正负例判定、`max_papers`、pool 门槛、训练/验证切分、fallback、保存接口不变。缺 OCR 首页时记录论文 ID 并跳过该论文；若全部缺失，沿用当前“无可用首页则不提取、不保存”的行为。不回退下载 PDF。
3. 在 `core/rerankers.py` 为 `GeminiProfileExtractor` 增加 OCR 首页文字输入路径，保留原有按 session、日期、正负例和 `max_papers` 组织模型输入的结构；将 PDF 文件 part 换成带论文 ID 和标签的 OCR 文字。OCR 路径的提示词说明输入为首页文字；Profile 的三个输出字段与解析方式不变。原 PDF 输入路径保留，避免影响其他调用方。
4. 在 `core/profile_pool.py` 中让 pool 初始化和带 framing 的提取使用同一 OCR 首页输入；评估器用论文 ID 对应的 OCR 首页文字进行 rerank。为 `GeminiRerankerPDF` 增加独立的 OCR 文字输入路径，并沿用现有 `personalized_subset_selection_prompt`、评价指标和重试逻辑。生产推荐仍调用该类原有的 PDF 输入路径。
5. 更新本路径的变量名、日志及“PDF 已提供”这类输入说明，使其准确描述 OCR 文字；不改变模型选择、Profile pool 决策和保存时机。

## 明确保持原样的行为

- Boost 的筛选条件完全照原 orchestrator：`NULL` 仍归入非点赞候选；不采用独立脚本的“仅明确赞踩、每篇取最新记录”规则。
- 不修改 `scripts/profile_from_ocr_feedback.py` 的独立预览行为。
- 不改论文抓取、PDF/OCR 生产及其存储流程；Boost 只读取已经写入论文库的 OCR 首页。生产推荐的候选 PDF 下载仍按现有逻辑运行。
- 不改 Profile pool 的训练/验证规则、评分、保存接口，也不修改推荐阶段的检索与博客生成。

## 审核后验证

1. 检查生产配置确实实例化 `GeminiRerankerPDF`；用不含 Profile 和含 Profile 的固定 PDF 首页样本，检查分别选择原提示词和 `personalized_ranking_prompt`，且规则字段完整。确认新增 OCR 输入路径不会改变原 PDF 输入路径。
2. 用固定 session 和 OCR 首页映射，检查 Boost 的单 Profile、pool 初始化和 pool 评估均不调用下载器或 PDF 首页提取函数；确认日期、标签、论文 ID、`max_papers` 仍正确。
3. 检查 `False` 和 `NULL` 的标签归类与当前 orchestrator 完全一致；检查部分/全部缺页时的日志与保存行为。
4. 在测试或受控环境运行一次 Boost 和一次推荐，检查 Profile 保存后的下一轮推荐确实将三类规则传给 PDF reranker；不在验证中覆盖线上用户 Profile。

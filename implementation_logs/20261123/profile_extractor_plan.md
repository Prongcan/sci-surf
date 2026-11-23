# 从明确赞踩和 OCR 首页生成 Profile

## 目标

增加独立命令，按指定用户从当前数据库读取明确点赞和点踩的论文，使用论文库已保存的 OCR 首页文字生成 `persona_definition`、`negative_constraints` 和 `ranking_heuristics`。运行结果输出为 JSON，供人工检查。

## 数据和行为

1. 从 `paper_recommendations` 读取指定用户每篇论文最新一条记录。仅保留 `blog_liked IS TRUE` 或 `IS FALSE`，排除未评价的 `NULL`。
2. 用论文 ID 从论文库 `text_chunks` 读取 `chunk_order = 0` 的非空 `text_content`。当前百度 PaddleOCR-VL 将页面按顺序写入该表，因此这条记录是第一页。
3. 如果没有明确反馈，或任一选中论文缺少 OCR 首页，终止并列出问题。不下载 PDF、不调用 OCR、不悄悄丢弃样本。
4. 将标题、推荐日期、明确赞踩标签和 OCR 首页文字交给当前 OpenAI Responses 客户端。提示词明确区别点赞、点踩和未评价，输出沿用现有 Profile 的三个字段。
5. 验证模型返回的 JSON 结构后打印结果。提供可选输出文件参数，默认不更新数据库。后续确认结果后可通过现有 `boost-complete` 接口保存。

## 与现有 Boost 的关系

复用 `GeminiProfileExtractor` 的模型客户端、模型配置和 JSON 解析。保留现有 orchestrator 路径，不更改日常任务。独立脚本使用 OCR 文本输入；现有 Boost 下载 PDF 并把首页 PDF 传给模型。当前反馈集中于单个推荐日期，脚本执行一次 Profile 提取，不运行需要多天样本的 Profile Pool 评估。

## 验证

检查命令行帮助、只读数据加载与样本标签、缺页处理、提示词构造及模型返回结构。验证过程不向线上数据库写入 Profile。

# AutoReviewer Reproduction v0.1.0

[简体中文](#简体中文) | [English](#english)

## 简体中文

这是《Towards End-to-End Automation of AI Research》AutoReviewer 复现的
首次公开版本。

### 包含内容

- 一次 200 篇 ICLR 2026 严格全初投稿评估。
- 一次 200 篇 Nature 混合版本评估：Accept 使用 camera-ready 文本，
  Reject 使用初投稿文本。
- 每篇论文由五个 DeepSeek V4 Flash Reviewer 评审，再由一个 Area Chair 汇总。
- 冻结预测、逐篇 review bundle、evaluation JSON、独立审计报告和 Nature 风格表格。
- AutoReviewer 报告和可复现协议。
- DeepSeek 近 30 天汇总用量截图。图片只显示 API Key 别名，不显示实际凭据。

### 重要解释边界

两次实验同时改变了稿件版本、提取格式、prompt/output 协议、采样配置和可见的
版本相关线索。两者差值只能作描述性比较，不能作为 camera-ready 影响的因果估计。

### 安全与数据边界

本版本不包含 API 凭据、<code>.env</code>、私有身份与标签映射、源 PDF、
固定 parquet 数据集或可重新分发的论文文本。运行 API 客户端前请阅读
<code>SECURITY.md</code> 和 <code>docs/PROTOCOL.md</code>。

### 验证

发布前全部 68 项测试通过。

## English

This is the first public release of the AutoReviewer reproduction accompanying
*Towards End-to-End Automation of AI Research*.

### Included

- A 200-paper ICLR 2026 strict all-initial evaluation.
- A 200-paper Nature-mixed evaluation using camera-ready text for accepted
  papers and initial-submission text for rejected papers.
- Five DeepSeek V4 Flash reviews and one Area Chair meta-review per paper.
- Frozen predictions, per-paper review bundles, evaluation JSON, independent
  audit reports, and Nature-style comparison tables.
- An AutoReviewer report and a documented, reproducible protocol.
- A DeepSeek dashboard screenshot showing aggregate 30-day usage. The image
  contains an API-key alias only and does not expose the credential value.

### Important interpretation boundary

The two runs differ in manuscript version, extraction format, prompt/output
protocol, sampling configuration, and visible version-related cues. Their
difference is descriptive and is not a causal estimate of the camera-ready effect.

### Security and data boundary

This release does not include API credentials, <code>.env</code> files, private
identifier-to-label mappings, source PDFs, the pinned parquet dataset, or
redistributable manuscript text. See <code>SECURITY.md</code> and
<code>docs/PROTOCOL.md</code> before running the API client.

### Verification

The release test suite contains 68 tests and passed before publication.

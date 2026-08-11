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
- DeepSeek 近 30 天汇总用量截图。

### 重要解释边界

两次实验同时改变了稿件版本、提取格式、prompt/output 协议、采样配置和可见的
版本相关线索。两者差值只能作描述性比较，不能作为 camera-ready 影响的因果估计。

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
- A DeepSeek dashboard screenshot showing aggregate 30-day usage.

### Important interpretation boundary

The two runs differ in manuscript version, extraction format, prompt/output
protocol, sampling configuration, and visible version-related cues. Their
difference is descriptive and is not a causal estimate of the camera-ready effect.

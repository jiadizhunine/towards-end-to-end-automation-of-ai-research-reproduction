# 更新日志 / Changelog

## Unreleased

### 简体中文

- 新增 Nature AutoReviewer 参数对照与结果解读，明确区分论文声明、冻结公开代码线索
  与 DeepSeek 适配。
- 补充原论文人类参考、稿件版本、可见线索、统计细节和 workshop 证据的解释边界。
- 在中英文首页、完整报告与简明说明中加入对应入口。
- 实验数据、冻结预测、统计结果和审计链均未改变。

### English

- Added a detailed Nature AutoReviewer protocol and results audit that separates
  paper-declared methods, pinned-public-code clues, and DeepSeek adaptations.
- Added interpretation boundaries for the paper's human reference, manuscript
  versions, visible clues, statistical details, and workshop evidence.
- Linked the audit from the Chinese and English homepages, full reports, and
  plain-language guides.
- Experimental data, frozen predictions, statistics, and audit chains are unchanged.

## v0.1.1 — 2026-08-11

### 简体中文

- 将 <code>README.md</code> 改为默认简体中文主页。
- 增加完整 <code>README.en.md</code>，并在两页顶部加入语言切换。
- 为 AutoReviewer 报告和复现协议增加中英文对应版本。
- 将 GitHub Release notes 改为中文在前、英文在后的双语格式。
- 实验数据、冻结预测、统计结果和审计链均未改变。

### English

- Made <code>README.md</code> the default Simplified Chinese landing page.
- Added a complete <code>README.en.md</code> with reciprocal language links.
- Added Chinese and English versions of the AutoReviewer report and protocol.
- Changed GitHub Release notes to a Chinese-first bilingual format.
- Experimental data, frozen predictions, statistics, and audit chains are unchanged.

## v0.1.0 — 2026-08-11

### 简体中文

首次公开复现版本：

- DeepSeek V4 Flash“五个 Reviewer + 一个 Area Chair”实现。
- 冻结的 Nature 对齐协议，记录 <code>temperature=0.75</code> 和 prompt 哈希。
- 两条经过审计的 ICLR 2026、每条 200 篇论文结果链。
- 400 份完整机器可读 review bundle。
- 冻结预测、bootstrap 评估、配对比较统计和独立审计报告。
- 包含 ICLR 2026 人类评分代理和 Nature 已发表基线的论文风格对照表。
- 供应商控制台用量截图。
- Fail-closed 的 camera-ready 获取器和混合版本输入构建器。

### English

Initial public reproduction release:

- DeepSeek V4 Flash five-reviewer plus Area-Chair implementation.
- Frozen Nature-aligned protocol with <code>temperature=0.75</code> and prompt hashes.
- Two audited 200-paper ICLR 2026 result chains.
- 400 complete machine-readable review bundles.
- Frozen predictions, bootstrap evaluations, paired comparison statistics, and
  independent audit reports.
- Nature-style comparison tables with an ICLR 2026 human-rating proxy and
  published Nature reference baselines.
- Provider dashboard usage screenshot.
- Camera-ready acquisition and mixed-version input builders that fail closed.

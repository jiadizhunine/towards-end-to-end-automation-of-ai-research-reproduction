<div align="center">

[English](./README.en.md) | **简体中文**

</div>

<div align="center">

# Towards End-to-End Automation of AI Research — Reproduction

**使用 DeepSeek V4 Flash 对论文 AutoReviewer 组件进行 200 篇论文复现**

![Version](https://img.shields.io/badge/release-v0.1.1-blue)
![License](https://img.shields.io/badge/license-Apache--2.0-green)
![Python](https://img.shields.io/badge/python-3.9%2B-3776AB)
![Cohort](https://img.shields.io/badge/ICLR%202026-200%20papers-orange)

</div>

本仓库复现 Nature 论文 [《Towards end-to-end automation of AI research》](https://www.nature.com/articles/s41586-026-10265-5)
中的 **Automated Reviewer** 组件。实验将原论文使用的 <code>o4-mini</code>
替换为 <code>deepseek-v4-flash</code>，并在同一批 200 篇 ICLR 2026
论文上评估两种输入条件。

仓库包含可运行实现、冻结的提示词与协议指纹、400 份完整审稿结果包、
冻结预测、评估文件、独立审计报告和论文风格对照表。

## 复现内容

每篇论文先由五个相互独立的 Reviewer 生成结构化评审，再由同一模型扮演
Area Chair，汇总五份评审并输出一份 meta-review 和二元 Accept/Reject
决定。正式 Reviewer 不具备浏览器、搜索、检索、RAG、URL 获取或其他模型
工具；联网仅用于调用 DeepSeek API。

| 条件 | 严格全初投稿条件 | Nature 对齐混合版本条件 |
|---|---|---|
| 样本 | 同一批 200 篇：78 Accept、122 Reject | 同一批 200 篇：78 Accept、122 Reject |
| Accept 稿件 | 初投稿 Markdown | ICLR 2026 官方 camera-ready PDF 提取文本 |
| Reject 稿件 | 初投稿 Markdown | 初投稿 Markdown |
| 可见身份与版本线索 | 已移除 | 提取文本中可见的线索均保留 |
| Reviewer prompt | 本地严格 JSON 协议 | Nature 基础 prompt + 冻结的完整 NeurIPS 表单 |
| DeepSeek 请求 | 开启 thinking；<code>reasoning_effort=max</code> | 关闭 thinking；<code>temperature=0.75</code> |
| 数值聚合 | 保留 Area Chair 原始数值和决定 | 保留 Area Chair 决定与文本；数值字段使用五审均值并取整 |

两种条件的差异不只有稿件版本，还包括 prompt、推理模式、输入格式、身份及
生命周期线索和数值聚合。因此，两者差值**不能解释为 camera-ready 修改的因果效应**。

## 主要结果

| 指标 | 严格全初投稿 | Nature 对齐混合版本 |
|---|---:|---:|
| 平衡准确率 | 0.537 [0.474, 0.601] | 0.597 [0.550, 0.646] |
| 准确率 | 0.585 [0.525, 0.645] | 0.525 [0.475, 0.580] |
| F1（Accept） | 0.376 [0.271, 0.474] | 0.603 [0.568, 0.639] |
| AUROC | 0.586 [0.503, 0.667] | 0.784 [0.720, 0.846] |
| FPR | 0.246 [0.172, 0.328] | 0.730 [0.648, 0.803] |
| FNR | 0.679 [0.577, 0.782] | 0.077 [0.026, 0.141] |

严格条件明显偏向 Reject。混合版本条件对 Accept 论文的排序更好，但把大多数
真实 Reject 判成了 Accept。两组结果都不能证明模型具备科学质量判断能力或
达到人类同行评审水平。

### Table 1a — 严格全初投稿条件

[![严格全初投稿结果](assets/table1a_strict_initial.png)](assets/table1a_strict_initial.svg)

### Table 1b — Nature 对齐混合版本条件

[![Nature 对齐混合版本结果](assets/table1b_nature_mixed.png)](assets/table1b_nature_mixed.svg)

ICLR 2026 的 Human 行是**人类评分代理指标**，不是两个独立评审委员会之间的
人类一致性实验。具体定义、不确定性、Nature 基线及解释边界见
[AutoReviewer 中文报告](docs/AUTOREVIEW_REPORT.md)。

## API 用量与成本

下图为 DeepSeek 控制台中 <code>Reviewer</code> 分组在近 30 天内的用量汇总：
**¥65.48、2,484 次 API 请求、60,964,615 tokens**。

![DeepSeek API 用量：¥65.48、2,484 次请求、60,964,615 tokens](assets/deepseek-api-usage.png)

控制台总量大于两次正式实验之和，其中可能包括 smoke test、重试和同一别名下
的其他调用。逐 bundle usage 记录给出的可审计正式实验估算为：

- 严格全初投稿：USD 4.61247628，可核验下界；
- Nature 对齐混合版本：USD 4.214517048；
- 两次正式实验合计约 USD 8.82699333。

价格是运行时写入 bundle 的计价假设，不代表 DeepSeek 当前或未来价格。

## 快速开始

~~~bash
git clone https://github.com/jiadizhunine/towards-end-to-end-automation-of-ai-research-reproduction.git
cd towards-end-to-end-automation-of-ai-research-reproduction
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
cp .env.example .env
~~~

在本地 <code>.env</code> 中设置 <code>DEEPSEEK_API_KEY</code>：

~~~dotenv
DEEPSEEK_API_KEY=replace_with_your_key
~~~

使用“五个 Reviewer + 一个 Area Chair”流程评审一篇 PDF：

~~~bash
deepseek-autoreviewer paper.pdf --output-dir outputs/example
~~~

对已经准备好的标签隔离数据运行 Nature 对齐协议：

~~~bash
iclr2026-autoreviewer run prepared/label_isolated results/new-run \
  --protocol nature-si-a3-base-v1 \
  --paper-jobs 2

iclr2026-autoreviewer freeze \
  results/new-run \
  results/new-run/frozen_predictions.json \
  --expected-count 200

iclr2026-autoreviewer evaluate \
  results/new-run/frozen_predictions.json \
  prepared/private/mapping.json \
  results/new-run/evaluation.json \
  --expected-count 200 \
  --bootstrap-samples 5000 \
  --bootstrap-seed 2026
~~~

只有在预测冻结后才会连接真实标签。数据准备与 camera-ready 获取流程见
[中文复现协议](docs/PROTOCOL.md)。

## 仓库结构

~~~text
src/deepseek_autoreviewer/   Reviewer、benchmark、盲化与协议代码
scripts/                     camera-ready 获取、人类评分代理和表格渲染脚本
tests/                       确定性单元测试与集成测试
results/strict-initial/      200 份 bundle、冻结预测、评估与审计
results/nature-mixed/        200 份 bundle、冻结预测、评估与审计
results/comparison/          配对统计和表格规格
assets/                      渲染表格与 API 用量截图
docs/                        中英文协议与总结报告
~~~

## 范围与局限

这是对论文单个组件的独立复现，不是对完整 AI Scientist 系统的复现。模型替换、
供应商适配、原论文未公开的采样细节、回顾性标签、潜在训练数据污染，以及混合
版本条件中的代理线索，都使其不能被称为逐参数精确复现。与会议最终决定一致，
也不等同于事实正确、可复现、新颖或具有科学价值。

## 致谢

复现协议和扩展 NeurIPS 评审表单参考 SakanaAI 的
[AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)，冻结于 commit
<code>6e8260925d17e1a0f6509751c19a9e1a481035b2</code>，原实现采用 Apache-2.0。
Nature 正文及补充材料是方法学的主要来源。本仓库与 Sakana AI、Nature、ICLR、
NeurIPS 或 DeepSeek 均无隶属关系。

仓库维护者：[@jiadizhunine](https://github.com/jiadizhunine)。

## 许可证

本项目采用 [Apache License 2.0](LICENSE)。第三方论文和数据集保留各自权利，
本仓库不重新分发这些内容。

<div align="center">

[English](./RESULTS_GUIDE.en.md) | **简体中文**

</div>

# 两张结果表，先这样读

这两张表评估的是同一批 200 篇 ICLR 2026 论文（78 Accept、122 Reject），但不是
一项只改变了 camera-ready 的消融实验。表中的 `0.54 ± 0.06` 表示点估计为 0.54，
`± 0.06` 是 95% bootstrap 区间的半宽；它不是百分比，也不是模型每次运行的波动。

| 条件 | Accept 输入 | Reject 输入 | 脱敏 | 其他同时变化的内容 |
|---|---|---|---|---|
| Table 1a：严格全初投稿 | 初投稿 Markdown | 初投稿 Markdown | 移除身份、版本和决定线索 | 本地严格 JSON 协议；DeepSeek thinking 开启 |
| Table 1b：Nature 对齐混合版本 | 官方 camera-ready PDF 文本 | 初投稿 Markdown | 不脱敏 | Nature 基础 prompt、完整 NeurIPS 表单、thinking 关闭、公开实现线索的 temperature=0.75、输入格式和数值聚合也不同 |

所以，Table 1b 与 Table 1a 的差异是“两个不同运行条件的结果差异”，不能说成
“camera-ready 让模型提高了多少”。

## Always reject 是什么

它不是可调参数，而是一条故意什么都不学的基准线：无论论文内容是什么，永远输出
Reject。当前队列中 Reject 占 122/200，因此它会得到：

| 平衡准确率 | 准确率 | F1（Accept） | AUROC | FPR | FNR |
|---:|---:|---:|---:|---:|---:|
| 0.50 | 0.61 | 0.00 | 0.50 | 0.00 | 1.00 |

它的 0.61 准确率只是在多数类上“猜中”了 122 篇 Reject；它一个 Accept 也找不到。
这条线的作用是防止把类别不平衡下看似不错的准确率误解成评审能力。一个有用的
Reviewer 至少应在平衡准确率、F1 或 AUROC 上明显优于它，而不是只靠“全部拒绝”。

## ICLR 2026 人类行是什么

ICLR 2026 的 Human 行来自同一批 200 篇论文的 775 份人类评分：每篇 3–5 份评分，
平均分大于 5 记为 Accept，等于 5 记为 Reject。它是**同队列人类评分代理**，可用于
给本项目的两张表提供背景；不是两个独立人类委员会之间的一致性实验，也不是最终
Area Chair 决定的复刻。

## Nature 的 2021 人类行和 2025 AI 行该怎么读

Nature Table 1 将 `Human (NeurIPS 2021)` 与 `AutoReviewer (ICLR 2025)` 并列，
但两行不共享论文、年份、会议、评审分配或标签生成过程。Nature Methods 自己写明
这种比较“不精确”。它可以作为外部参照，不能当成“同一批论文上 AI 对人类”的横向
竞赛，也不能只因两个数字接近就推出 AI 达到人类审稿能力。

本仓库仍将这几行放在表格下半部分，是为了忠实展示原论文报告的参照，而不是把它们
并入 ICLR 2026 的同队列比较。

## Nature 原始 AutoReviewer 实际怎么跑

1. 将论文 PDF 的可见文本、基础角色提示和完整 NeurIPS 审稿表单交给 `o4-mini`。
2. 对同一篇论文独立生成五份结构化审稿。
3. 由同一模型担任 Area Chair，汇总五审并给出 meta-review 和二元决定。
4. 以 ICLR 最终会议决定作为回顾性标签，计算一致度指标。

最终选定条件是基础 prompt 加五审 ensemble，不使用 VLM、few-shot 或 Reflexion。
论文没有完整公开最终 temperature、seed、AUROC 连续分数和所有失败处理。公开代码
中的细节因此只能视为实现线索，不等于论文逐参数规范。

若要逐项查看哪些参数确实来自论文、哪些来自冻结公开代码、哪些是本项目为 DeepSeek
所作的适配，以及由此带来的解释边界，见[Nature AutoReviewer 参数对照与结果解读](./NATURE_AUTOREVIEWER_AUDIT.md)。

AutoReviewer 本身没有报告使用浏览器、搜索、RAG 或文献检索工具；完整 AI Scientist
在想法与引用阶段使用的网页/文献工具属于另一个组件。原论文还将 Reject 设为初投稿、
Accept 设为 camera-ready，并直接处理 PDF 原始文本，没有报告脱敏步骤。这意味着版本、
作者、单位或出版页眉等可见线索可能影响结果。

## Workshop 证据的边界

Nature 论文报道三篇 AI 生成稿件投往 ICLR 2025 ICBINB workshop：其中一篇以 6、7、6
分达到 workshop 的接收阈值，另两篇没有达到。提交前有人工筛选候选、检查代码和
格式；论文同时说明该 workshop 接收率为 70%，ICLR 主会为 32%，且三篇均未达到作者
设定的主会标准。

因此，这支持的是“一次特定 workshop 场景下的人工评审成功实例”。它不单独证明稳定
的主会级产出、完全自动化科研，或普适的科学质量判断。论文更广泛的规模化结论主要
依赖 Automated Reviewer 本身，而该审稿器的人类比较又不是匹配的同队列实验。

更准确地说，论文的叙事有两类证据：一篇 workshop 成功稿件提供外部人工评审例子，
Automated Reviewer 提供规模化趋势指标。前者的证据范围很窄，后者又依赖一个没有
匹配人类基线的自动审稿器；两者合在一起仍不足以单独证明“稳定的端到端自动科研”。
因此，说论文只靠这一篇稿件证明全部结论并不准确，但把这篇稿件视为其最醒目的外部
人工评审证据则是合理的。

## 结论

这两张表最稳妥的读法是：DeepSeek AutoReviewer 对输入版本、文本格式和协议很敏感；
它与会议决定的某些一致度指标会变化，但这不能直接等同于科学质量判断，也不能作为
达到人类审稿水平的证据。

## 来源

- [Nature 正文与 Methods](https://www.nature.com/articles/s41586-026-10265-5)
- [Nature Supplementary Information](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10265-5/MediaObjects/41586_2026_10265_MOESM1_ESM.pdf)
- [AI Scientist ICLR 2025 Workshop Experiment](https://github.com/SakanaAI/AI-Scientist-ICLR2025-Workshop-Experiment)
- [完整 AutoReviewer 报告](./AUTOREVIEW_REPORT.md)

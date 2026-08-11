<div align="center">

[English](./NATURE_AUTOREVIEWER_AUDIT.en.md) | **简体中文**

</div>

# Nature AutoReviewer：参数对照与结果解读

## 先给结论

本仓库的 `nature-si-a3-base-v1` 是一个**以论文补充材料为主、以作者冻结公开
代码补足未展开细节、再对 DeepSeek 做显式适配**的协议。它复现了论文最重要的
评审拓扑：五个独立 Reviewer、一个 Area Chair、NeurIPS 风格结构化表单，以及
Area Chair 的二元决定。

它不是 Nature 最终实验的逐参数复刻，也不是对公开仓库每一行代码的机械复制：
论文使用 `o4-mini` 和 PDF 原始文本；本项目使用 `deepseek-v4-flash`，且混合版本
条件中 Accept 是 PDF 提取文本、Reject 是 Markdown。论文没有完整公开最终
temperature、seed、连续 AUROC 分数、失败处理和供应商采样接口。公开代码里的一些
实现细节也与补充材料的呈现顺序不同。

最准确的名称是：**Nature AutoReviewer 核心流程的 DeepSeek 对齐复现**。
“对齐”不等于“论文结果等价”，更不等于“精确重现论文的所有数值”。

本文也说明为什么原论文的结果需要谨慎解释。这些是方法学与证据边界，**不是**对
作者诚信或学术不端的指控。

## 证据层级

本项目按以下优先级解释方法：

1. **论文正文与补充材料**：确定作者声称的正式方法与最终条件。
2. **作者冻结公开代码**：补充论文没有逐字展开的表单、输出模板和实现线索；它不能
   自动覆盖论文的正式表述。
3. **DeepSeek 适配**：因模型与 API 不同而必须作出的选择；它们必须单独披露，而不
   应被写成 Nature 已报告的参数。

运行 manifest 因而将字段分为 `paper_declared`、`public_code_adapter` 和
`deepseek_adapter_choice_not_reported_by_paper`，并对提示词与协议记录 SHA-256。

## 原始 Nature AutoReviewer 怎样运行

AutoReviewer 是完整 AI Scientist 的一个组件，不等同于整个 AI Scientist。完整系统在
**想法生成与引用**阶段可使用 Semantic Scholar 和网页工具；AutoReviewer 本身的
描述是把稿件内容交给模型评审，未报告浏览器、搜索、RAG 或文献检索工具。

正式流程为：

1. `o4-mini` 读取一篇论文 PDF 的文本，配合基础角色提示和 NeurIPS 审稿表单，生成
   结构化审稿。
2. 对同一篇论文独立生成五份审稿。
3. 同一模型扮演 Area Chair，阅读五审，生成 meta-review 与最终 `Accept` / `Reject`
   决定。
4. 将该决定与 ICLR 最终会议决定作回顾性比较。

作者报告的最终条件是“基础 prompt + 五审 ensemble”，不使用 VLM、few-shot 或
Reflexion。Reviewer 的基础 system prompt 是：

```text
You are an AI researcher who is reviewing a paper that was submitted to a prestigious ML venue.
```

补充材料还展示了 Area Chair 指令，要求汇总多位 Reviewer、找出共识并尊重各方意见。

## 逐项参数对照

| 项目 | Nature 论文/补充材料明确说明 | 冻结公开代码提供的线索 | 本项目 Nature 对齐混合版本 | 判断 |
|---|---|---|---|---|
| Reviewer 模型 | `o4-mini` | 公开实现不是最终服务端配置的完整证明 | `deepseek-v4-flash` | **不同模型；本项目不是 o4-mini 数值复现** |
| 稿件来源 | 两类均描述为 PDF 原始文本；Reject 为初投稿，Accept 为 camera-ready | benchmark 从 OpenReview PDF 获取稿件 | Accept：官方 ICLR 2026 proceedings PDF + PyMuPDF；Reject：固定 ProReviewer 初投稿 Markdown | **版本策略接近，类别输入格式不同** |
| 可见线索 | 未报告对标题、作者、单位、出版页眉或状态的脱敏 | benchmark / 文本加载路径没有删除可见文字 | 混合版本保留提取文本中可见线索 | **接近未盲化设定，不能声称逐篇线索完全相同** |
| Reviewer 基础 prompt | 一句基础角色提示 | 部分代码路径还会增加谨慎/拒绝倾向句子 | 严格采用补充材料的一句，不加额外句子 | **论文优先；不机械复制全部代码分支** |
| 评审表单 | 详细 NeurIPS guidelines、结构化字段、无 few-shot | 展开后的完整表单、字段范围和输出模板 | 冻结表单，UTF-8 SHA-256 `41493738…3ffd2` | **表单与公开代码对齐；论文未逐字刊印表单** |
| 输出格式 | 论文确认结构化 JSON，不要求公开显示推理 | `THOUGHT` 后接 `REVIEW JSON` | 保留该格式契约；解析器也接受直接合法 JSON | **代码对齐，不应误写为论文要求保存推理** |
| Reviewer 数量 | 五个独立审稿 | 五审 ensemble | 每篇五个独立 HTTP Reviewer 请求 | **核心拓扑对齐；底层采样方式未公开** |
| Area Chair | 同一模型汇总五审，输出同格式 meta-review | 有明确 system prompt 和组装逻辑 | 使用补充材料的“先五审、后完整表单”顺序 | **以补充材料为准；与某些代码排列不同** |
| 最终二元决定 | Area Chair meta-review 的 `Decision` | 同样保留 meta 决定 | 最终预测取原始 Area Chair `Decision` | **对齐** |
| 数值字段 | 未明确是否以五审均值覆盖 Area Chair 数值 | 代码会以五审均值覆盖数值，保留 meta 文本/决定 | 保留 Area Chair 文本与决定；数值视图用五审均值并取整 | **公开代码兼容层，非论文已证实最终设定** |
| 采样温度 / seed | 未公布最终 temperature 或 seed | 有 `temperature=0.75` 的五审采样路径 | `temperature=0.75`；seed 未设置 | **温度来自代码线索，非论文确认参数** |
| DeepSeek thinking | 不适用 | 不适用 | 显式关闭 thinking，不传 `reasoning_effort` | **供应商适配，不是 Nature 参数** |
| 输出长度 / 重试 / 并发 | 未完整披露 | 旧代码失败回退不等于论文规范 | 16,384 输出 token；最多 3 次；五审不完整即失败；并发 5 | **运行工程选择，非论文对齐声明** |
| 工具与检索 | Reviewer 不执行显式文献检索 | reviewer 函数无工具接口 | 无 browser、search、RAG、URL fetch 或模型工具 | **Reviewer 层对齐；不要与完整 AI Scientist 的检索混同** |
| VLM / few-shot / Reflexion | 最终条件不使用三者 | 有相应消融实现 | 三者均未使用 | **对齐** |
| 统计 | 报告 bootstrap CI，但没有冻结所有重采样细节 | 代码不是完整统计规范 | 5,000 次论文级、按类别分层 percentile bootstrap，seed=2026 | **可复现项目选择，非逐参数复刻** |
| AUROC 连续分数 | 没有清楚给出最终连续 score | 历史二元代码路径不足以证明论文最终定义 | 五审 `Overall` 均值 | **本项目操作化定义；不能声称与 Nature 完全相同** |

### “和文章原本代码对齐吗？”

准确回答是：**核心对齐；细节是“论文优先 + 代码补全 + DeepSeek 适配”，不是 100% 对齐。**

- **论文与本项目明确一致**：五个独立审稿、一个 Area Chair、NeurIPS 风格结构化
  评审、基础 prompt、无 VLM/few-shot/Reflexion、Area Chair 最终决定、Reviewer
  无外部检索工具。
- **由冻结公开代码补齐**：完整表单文字、`THOUGHT`/JSON 外壳、`temperature=0.75`
  和数值均值覆盖。
- **不能声称对齐**：`o4-mini` 与 DeepSeek 的模型行为、Reject Markdown、DeepSeek
  thinking、HTTP 并发与重试、最大输出、seed、最终 AUC score 和论文服务端采样细节。

补充材料和公开代码并没有构成一个逐参数、逐位可执行的唯一规范。例如补充材料展示的
Area Chair 输入顺序和某些公开代码的组装顺序不同；论文也没有把完整表单或
temperature 写成最终实验规范。因此本项目以**补充材料优先**，把代码当作可追溯的
补充来源。

## 为什么 Nature 的结果会让人觉得“有问题”

下列事项不代表论文结果必然错误；它们说明从这些结果到“模型已经可靠达到人类评审
水平”或“端到端自动科研已被充分证明”之间，仍有明显证据距离。

| 观察到的设计边界 | 为什么会影响结论 | 已知的缓解或解释 | 仍需的验证 |
|---|---|---|---|
| `Human (NeurIPS 2021)` 与 `AutoReviewer (ICLR 2025)` 并列 | 不是同一批论文、同一年、同一会议或同一评审分配；同名指标不能变成配对的人机比赛 | 论文承认论文池不同、有 distribution shift，并称这是当时唯一可用的人类一致性参照 | 在同一稿件上安排独立人类委员会与模型并行评审，预先冻结指标 |
| Accept 使用 camera-ready、Reject 使用初投稿 | 版本与标签系统相关；修订、作者、单位、页眉、会议状态可能成为代理线索 | 补充材料承认该偏差；修订本身也可能真实改善稿件 | 同版本、同格式，做盲化/不盲化交叉实验 |
| PDF 可见文字未报告脱敏 | 模型可能学习 `Published as…`、`Under review…`、匿名占位符或作者/机构等版本代理，而非科学质量 | 公开实现直接抽取文本，这让流程透明但不消除混杂 | 逐篇 redaction audit；比较完整文本与去线索文本 |
| 回顾性“会议决定一致度” | 会议决定不是论文正确性、可复现性、新颖性或长期价值的真理标签 | 它是可获得的大规模现实标签 | 结果公布前冻结预测，并加入事实/复现性核验 |
| 三篇 workshop 投稿中只有一篇成功 | 样本很小，投稿前有人工筛选候选、检查代码和格式；workshop 接收率高于主会 | 论文明确说仅 1/3 成功，且不能稳定达到 top-tier 或甚至 workshop 标准 | 多轮预注册、完整候选集、统一阈值、独立审稿与外部复现 |
| 下游“生成论文质量随模型/算力提升”依赖同一个 AutoReviewer | 评价器的输入线索偏好或校准误差会传到下游曲线 | ensemble 可降低随机采样方差，但不会自动消除系统性偏差 | 用独立人类、不同模型和盲化设置交叉验证趋势 |
| 关键实现/统计细节未完全冻结在论文中 | 温度、seed、重试、连续 AUC score 和论文/代码差异使精确复现和归因变难 | 论文、补充材料、代码共同提供了大量但不完整的信息 | 发布最终 manifest、请求参数、可重算脚本和去标识预测 |
| 2025 数据集在知识截止后 | 日历切分是合理污染控制，但不是对训练数据的直接审计 | 论文确实报告了后截止年份性能下降 | 时间戳数据排除、训练数据证据或真正前瞻性会议队列 |

补充材料关于平衡准确率同时出现“按类别召回率平均”和“随机下采样较大类”的表述。
类别不平衡时两者不一定完全相同。最稳妥的做法是报告明确公式、固定实现和完整重采样
脚本，而不只引用指标名称。

### Workshop 成功稿件的证据边界

论文的强事实是：三篇 AI 生成稿件被提交到 ICLR 2025 ICBINB workshop；其中一篇获得
6、7、6 分，并按预先设定方案撤稿。评审人知道其中有 AI 生成稿，但不知道是哪一篇。
论文还说明候选在投稿前经过人工筛选，三篇中只有一篇达到 workshop 门槛，且作者团队
认为三篇都没有达到 ICLR 主会标准。

它是有价值但狭窄的外部人工评审实例：**在特定 workshop、主题和筛选流程下，一篇
AI 生成稿件获得了高于接受阈值的审稿分数。** 它不能单独证明稳定的主会级产出，也
不能单独支撑“端到端自动科研已普遍可靠”的更强说法；论文自己的 limitations 也承认
这一点。

更宽泛的叙事主要由 AutoReviewer 的规模化指标承载，而 AutoReviewer 的人类比较又不是
同队列实验。因此合理结论是“一个有趣的系统演示与有限外部证据”，而不是“已经以
匹配人类基线证明了通用科研质量”。

## 本项目两张表能与不能回答什么

### 能回答

- 同一批 200 篇 ICLR 2026 论文在严格全初投稿条件与 Nature 对齐混合版本条件下，
  DeepSeek 的决定行为显著不同。
- 在本项目的混合条件下，AUROC 为 `0.78 ± 0.06`，但二元 Decision 的 FPR 为
  `0.73 ± 0.08`；排序信号变强不等于可直接用于接收决定。
- 在严格、脱敏、全初投稿条件下，模型偏 Reject：FNR 为 `0.68 ± 0.10`。

### 不能回答

- 不能把两张表的差值解释成“camera-ready 的纯因果效应”：版本、格式、prompt、
  thinking、数值聚合和可见线索同时变化。
- 不能把 Nature 对齐混合版本称为 Nature `o4-mini` 结果的逐参数精确复现。
- 不能从会议决定一致度推出科学正确性、研究新颖性、可复现性或人类同等能力。
- 不能仅凭一篇 workshop 成功稿件推出稳定的端到端自动科研能力。

最有信息价值的下一步是预先注册的交叉设计：固定模型、prompt、提取格式和统计，
只交换稿件版本与是否脱敏；再在尚未公布决定的队列上冻结预测。这会把“版本变化”
与“标签相关线索”分开，也比回顾性决定一致度更接近真正的前瞻性验证。

## 可复核内容

- 协议定义：`src/deepseek_autoreviewer/nature_protocol.py`。
- Nature 对齐运行的 `run_manifest.json` 保存协议、提示词哈希、有效请求字段和三类
  证据分类。
- 每篇 `review_bundle.json` 保存五个 Reviewer、Area Chair、原始响应、结构化结果、
  usage 与输入文本哈希；预测冻结后才连接标签。
- 数字、成本和配对比较见[完整 AutoReviewer 报告](./AUTOREVIEW_REPORT.md)；更短的
  读法见[两张表的简明说明](./RESULTS_GUIDE.md)。

## 主要来源

- [Nature 正文与 Methods](https://www.nature.com/articles/s41586-026-10265-5)
- [Nature Supplementary Information，A.3](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10265-5/MediaObjects/41586_2026_10265_MOESM1_ESM.pdf)
- [SakanaAI AI-Scientist-v2 冻结 Reviewer 实现，commit `6e8260…`](https://github.com/SakanaAI/AI-Scientist-v2/blob/6e8260925d17e1a0f6509751c19a9e1a481035b2/ai_scientist/perform_llm_review.py)
- [SakanaAI 原始 ICLR benchmark 脚本，冻结 commit](https://github.com/SakanaAI/AI-Scientist/blob/d6576a38237c03205ba5ae0d4cc5aa7eae038577/review_iclr_bench/iclr_analysis.py)
- [AI Scientist ICLR 2025 Workshop Experiment](https://github.com/SakanaAI/AI-Scientist-ICLR2025-Workshop-Experiment)

<div align="center">

[English](./PROTOCOL.en.md) | **简体中文**

</div>

# 复现协议

## 范围

本协议只覆盖 AutoReviewer 组件，不复现完整 AI Scientist 系统中的想法生成、
实验执行、论文生成或 workshop 投稿组件。

## 固定论文队列

- 会议快照：ProReviewer 数据集的 ICLR 2026 test split。
- 源 parquet SHA-256：
  <code>c9cb7de219be6e4455fcb594ec8be39f8c0bdf5dcfc575d588774d33fd73e10b</code>。
- 合格标签：明确的 Accept 层级和精确 Reject。
- 排除标签：Withdrawn、Desk Reject、空值及其他状态。
- 固定队列：200 篇论文，其中 78 Accept、122 Reject。
- 选择结果与输入哈希记录在 run manifest 和冻结预测文件中。源稿件与私有映射
  不在仓库中重新分发。

## 评审拓扑

1. 五个相互独立的 Reviewer 调用使用相同稿件和评审条件。
2. 每个响应都必须完整解析为结构化评审 schema。
3. 五份结构化评审交给一个 Area Chair 调用。
4. Area Chair 原始 <code>Decision</code> 是权威二元预测。
5. 运行结果在没有标签的情况下冻结。
6. 评估阶段再使用 <code>blind_id + blind_text_sha256</code> 连接私有标签映射并计算指标。

## Nature 对齐协议记录

- 协议 ID：<code>nature-si-a3-base-v1</code>。
- 指纹：
  <code>593791d8c5435a95c06952f703409af0b64eaf3ad22bf1e47426d682ac4cd717</code>。
- 模型：<code>deepseek-v4-flash</code>。
- Reviewer 调用：5 个独立 HTTP 请求。
- Area Chair 调用：1 个。
- Temperature：<code>0.75</code>。
- DeepSeek thinking：关闭。
- 省略的请求字段：<code>reasoning_effort</code>、<code>response_format</code>、<code>tools</code>。
- 最大输出 tokens：16,384。
- 每个调用最多尝试：3 次。
- Reviewer 并行数：5。
- Few-shot 示例：0。
- Reflexion：0 次。
- VLM：0 次。
- 最终二元决定：Area Chair 原始 <code>Decision</code>。
- 公开代码兼容的数值视图：五个 Reviewer 分数的算术均值并取整，同时保留
  Area Chair 的文本和决定。

Run manifest 将“论文明确声明”“冻结公开代码细节”和“DeepSeek 适配选择”分别
记录。这样做是必要的，因为 Nature 论文没有公开所有采样参数和供应商参数。

## 稿件条件

### 严格全初投稿

两类论文都使用 ProReviewer 的初投稿 Markdown 快照。严格脱敏会移除标题、作者、
单位、论文与 forum ID、arXiv ID、会议与决定状态、URL、域名、DOI、电子邮箱、
ORCID、致谢、作者贡献、机构及生命周期线索。正式运行使用较早的严格 JSON 协议，
开启 DeepSeek thinking，并设置 <code>reasoning_effort=max</code>。

### Nature 对齐混合版本

Accept 论文使用 ICLR 2026 官方 proceedings PDF。获取脚本把固定 Accept 队列与
官方 proceedings 索引进行匹配，核验标题和作者证据，只下载官方 PDF URL，并检查
MIME、长度、PDF magic、SHA-256、页数和首页会议标记，同时保存私有来源 manifest。
PyMuPDF 按页面顺序提取可见文本。

Reject 论文继续使用 ProReviewer 初投稿 Markdown。混合版本条件不执行脱敏。
公开输入 manifest 明确记录：

~~~json
{
  "contains_source_identifiers": true,
  "contains_version_label_clues": true,
  "contains_input_format_label_clues": true,
  "strictly_blinded": false
}
~~~

因此，Accept 与 Reject 输入在稿件版本和格式上都不同。

## Camera-ready 获取

仓库不包含 78 份 PDF。拥有合法本地私有映射时，可在不写入正式目录的情况下
验证匹配：

~~~bash
python scripts/fetch_camera_ready.py \
  /path/to/private/mapping.json \
  /path/to/camera-ready-private \
  --dry-run
~~~

只有确实准备下载官方 PDF 时才应把 <code>--dry-run</code> 显式替换为
<code>--download</code>。构建器采用 fail-closed 策略，所有校验通过后才原子发布目标目录。

混合输入树通过 Python 函数
<code>deepseek_autoreviewer.mixed_version.build_mixed_version_benchmark</code>
构建，需要严格条件的私有映射、固定源 parquet、camera-ready 来源 manifest 和
一个全新输出目录。

## 指标

- 正类：Accept。
- 二元预测：Area Chair 原始决定。
- 平衡准确率：<code>(TPR + TNR) / 2</code>。
- AUROC 连续分数：五个独立 Reviewer 的 <code>Overall</code> 算术均值。
- 主要不确定性：按真实类别分层的论文级 percentile bootstrap。
- 严格条件：10,000 次，seed=20260811。
- 混合版本与配对比较：5,000 次，seed=2026。

Nature 没有完整公开 AUROC 连续分数、bootstrap seed、分层方式、供应商 batch
语义和全部失败处理细节。这里列出的值是冻结的可执行选择，不代表逐参数精确复现。

## 复现边界

要进行稿件版本的因果比较，必须在相同 prompt、提取格式、身份处理、模型请求和
聚合策略下，分别重新运行全初投稿输入和混合版本输入。本仓库发布的两次实验不满足
这一条件，因此不能被描述为 camera-ready 消融实验。

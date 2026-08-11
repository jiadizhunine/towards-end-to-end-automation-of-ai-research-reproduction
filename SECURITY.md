<div align="center">

[English](./SECURITY.en.md) | **简体中文**

</div>

# 安全与负责任使用

## API 凭据

绝不要提交 DeepSeek API Key 或其他凭据。客户端从进程环境读取
<code>DEEPSEEK_API_KEY</code>。只在可信机器上使用被 Git 忽略的本地
<code>.env</code> 文件：

~~~bash
cp .env.example .env
chmod 600 .env
~~~

仓库会忽略 <code>.env</code>、<code>.env.*</code>、凭据文件、原始数据集、
论文 PDF、提取后的论文文本和本地运行目录。示例文件中只包含占位符。

发布 fork 前，应检查所有已跟踪内容和 Git 历史：

~~~bash
git grep -nEi '(api[_-]?key|authorization|bearer|secret|token)'
git log -p --all -- . ':!*.png'
~~~

如果真实 Key 曾被提交，应立即在供应商处撤销并更换，再从 Git 历史中清除。
只删除最新版本中的文件并不足够。

## 稿件与标签

论文 PDF 和数据集快照可能受第三方条款约束。本仓库记录哈希和获取代码，但不
重新分发这些文件。私有映射负责连接 blind ID、原始身份和最终标签；除非已经
核实再分发权利与公开目的，否则它们应始终位于正式评审流程和公开 fork 之外。

## 网络边界

AutoReviewer 不向模型提供浏览器、搜索、检索、RAG、Shell 或 URL 获取能力。
运行时仍需通过网络调用配置的 DeepSeek <code>/chat/completions</code> 端点。
应用层 URL 检查不等同于操作系统防火墙。

## 高风险用途

本软件是评估产物和研究原型。不得把其 Accept/Reject 输出用作自主论文决定、
科学质量证明、学术不端结论、招聘决定或合格人类评审的替代品。

## 报告安全问题

请通过 GitHub Security Advisory 报告仓库安全漏洞。不要把 API Key、未公开稿件
或私有映射粘贴到公开 Issue。

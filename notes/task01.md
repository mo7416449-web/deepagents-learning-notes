# Task 1：环境准备与研究任务

## 环境和配置

在协助下，使用 WSL2 Ubuntu 配置 Python 3.12、uv、Node.js、npm 和 AgentSeek，并创建 `deepagents/research` 项目。项目安装了前后端依赖，配置了硅基流动模型、Tavily 搜索以及 LangSmith 追踪。

使用 `agentseek doctor --live` 检查时，项目的前端和后端均可访问。课程检查 `agentseek task course-check` 的 6 项测试通过。

## 实际研究任务

在协助下提交的问题是：查找 Python 官方文档，说明 `list` 和 `tuple` 的两个主要区别，并附上来源。

Agent 使用 Tavily 搜索，生成了中文回答。运行记录中可以看到模型调用、`tavily_search`、任务规划和文件操作；最终报告引用了 Python 官方文档。完整运行约 327 秒，LangSmith Trace 记录在 `deepagents-course` 项目中。

核对来源：[Python 官方文档：为什么区分 tuple 和 list](https://docs.python.org/3/faq/design.html#why-are-there-separate-tuple-and-list-data-types)。

## 后续学习

需要继续查看 Trace，理解调用次数、耗时和 Token 用量，学习心得将在进一步学习后补充。

课程来源：[AgentSeek 准备篇（上）](https://datawhalechina.github.io/deepagents-in-action/chapters/pre01-agentseek-create/)。

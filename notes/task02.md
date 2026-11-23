# Task 2：第一个 Agent 与工具调用

## 任务与代码

在协助下完成了两个运行：天气工具 Hello World，以及添加货币换算工具的示例。代码见 [task2_agent.py](../examples/task2_agent.py)。

`get_weather` 接收城市名称，返回固定的演示天气；`convert_currency` 接收金额与币种，使用固定的演示汇率。货币换算工具的参数包含类型标注、函数说明，以及目标币种的默认值 `CNY`。这两个工具返回的内容均为演示数据。

## 实际运行结果

- `weather` 模式调用 `get_weather`，返回北京的演示天气。
- `custom` 模式先调用 `get_weather`，再调用 `convert_currency`，按演示汇率将 100 美元换算为 720 人民币。
- LangSmith 中 `task2_custom` 的完整 Trace 显示 3 次 `ChatOpenAI` 模型调用和 2 次工具调用，运行约 17.91 秒。

本次代码编写、运行和 Trace 核对由 AI 助手协助完成；后续将亲自阅读代码并练习。

## 对工具调用过程的理解

模型接收问题后，可以根据工具的名称、说明和参数决定调用工具；程序执行工具，将结果返回模型，模型再组织回答。一次 `invoke()` 内可以有多次模型调用和工具调用。本例中天气和汇率均为固定演示数据，理解工具的实际数据来源有助于判断回答能否用于真实决策。

## 在已有研究项目环境中运行

在已经完成准备篇配置的 `research_deepagent` 项目根目录中，运行项目内的示例副本：

```bash
uv run python practice/task2_agent.py weather
uv run python practice/task2_agent.py custom
```

示例读取项目 `.env` 中已有的 `AGENTSEEK_MODEL`、`OPENAI_API_BASE` 和 `OPENAI_API_KEY`。请勿公开 API Key 或上传 `.env` 文件。模型调用会消耗账号额度。

## 后续学习

继续阅读 `create_deep_agent()`、工具参数和 `invoke()` 的输入输出，在 LangSmith 中查看模型和工具之间的调用过程，再补充自己的理解。

课程来源：[第 1 章：Agent Harness](https://datawhalechina.github.io/deepagents-in-action/chapters/ch01-agent-harness/)；[第 2 章：快速上手](https://datawhalechina.github.io/deepagents-in-action/chapters/ch02-quickstart/)。

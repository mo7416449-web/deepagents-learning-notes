# Task 5：子 Agent 与上下文隔离实验

本实验由 AI 助手在 WSL 中运行，使用 `deepagents==0.7.8`、硅基流动模型和本地共享文件后端。

实验代码：[task5_subagents.py](../examples/task5_subagents.py)。代码读取本机 Task 3 记录；换用其他环境时需要修改相应路径。

## 角色与任务

- 主 Agent：负责协调，依次委派任务并汇总结果。
- researcher：读取 Task 3 实验记录，整理事实并写入共享文件。
- writer：读取共享事实文件，编写简短报告。

## 实际运行结果

主 Agent 先通过 `task` 委派 researcher，后者读取资料、写入 `/facts.md`，并返回实验摘要。主 Agent 再通过 `task` 委派 writer，后者读取文件并返回报告。主 Agent 最终汇总了结果。LangSmith 的调用记录包含两次 `task` 调用，分别对应 researcher 和 writer；运行总时长约 297.74 秒。

两个子 Agent 使用独立的消息上下文，其中的文件读取和写入调用记录可在 Trace 中查看；主 Agent 的消息中记录了委派参数和子任务返回结果。两者共同使用 FilesystemBackend，因此 writer 可以读取 researcher 写入的文件。

## 需要区分的配置

声明式子 Agent 使用各自的 `system_prompt`；其 `skills` 需要单独配置。v0.7 中 Todo 中间件需要按角色单独配置。工具的继承和文件共享取决于具体配置；上下文隔离不等同于文件权限隔离。返回内容的详细程度也取决于子 Agent 的实际输出，本次 researcher 返回了较详细的摘要。

## 复现

使用已配置的研究项目环境，在 WSL 中执行：

```bash
cd ~/projects/research_deepagent
uv run python /mnt/e/datewhale/task5_subagents.py
```

脚本读取 Task 3 实验记录并向 `/home/olan/projects/research_deepagent/practice/task5_subagents` 写入文件；重复运行会覆盖同名输入文件。运行会消耗模型调用额度。

课程来源：[第 5 章：子 Agent 与上下文隔离](https://datawhalechina.github.io/deepagents-in-action/chapters/ch05-subagents/)。

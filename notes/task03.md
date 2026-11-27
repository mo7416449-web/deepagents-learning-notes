# Task 3：虚拟文件系统实验记录

本实验由 AI 助手使用 WSL 中 `deepagents==0.7.8` 和硅基流动模型运行。

实验代码：[task3_experiment.py](../examples/task3_experiment.py)。以下运行命令使用本机原始路径；代码中的 WSL 路径需要按实际环境调整。

## 文件工具

默认 StateBackend 中，Agent 依次调用 `write_file` 写入“物流实验 TASK3-KEY”、`read_file` 读取、`grep` 搜索，三项均成功。运行结果的 state 文件列表包含 `/task3-note.txt`，磁盘中没有该文件。

## 大结果卸载

测试工具生成 8000 行明确标记为演示的文本。为便于观察，本次将卸载阈值设为 1000 个估算 token。结果被写入 `/large_tool_results/01a209050d4ff3086e8b553a63b14bb7`，工具消息提供路径、前后各五行和省略行数，Agent 随后使用 `read_file` 分段读取。

## 后端对比

| 项目 | StateBackend | FilesystemBackend |
| --- | --- | --- |
| 存储位置 | Agent state | WSL 本地磁盘目录 |
| 本次重启验证 | 新建进程中的 `InMemorySaver` 没有原检查点 | 新进程中的后端成功读回 `task3-note.txt` |
| 适用场景 | 临时状态；配合持久化检查点可延续线程 | 需要在本地保留和查看文件 |

StateBackend 的持久性取决于检查点配置；本次仅测试内存检查点，不代表所有 StateBackend 配置。FilesystemBackend 的文件保存在 `/home/olan/projects/research_deepagent/practice/task3_files`。

## 运行

在 WSL 的 `research_deepagent` 项目目录中执行：

```bash
uv run python /mnt/e/datewhale/task3_experiment.py state
uv run python /mnt/e/datewhale/task3_experiment.py disk
uv run python /mnt/e/datewhale/task3_experiment.py eviction
```

脚本使用已有项目的 `.env` 配置；调用模型会消耗额度。磁盘实验会写入固定路径，重跑前应检查已有文件，避免覆盖。

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from deepagents.middleware.filesystem import FilesystemMiddleware
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv('/home/olan/projects/research_deepagent/.env')
model = ChatOpenAI(model=os.environ['AGENTSEEK_MODEL'], api_key=os.environ['OPENAI_API_KEY'], base_url=os.environ['OPENAI_API_BASE'])
root = Path('/home/olan/projects/research_deepagent/practice/task3_files')
root.mkdir(parents=True, exist_ok=True)


def large_demo_data() -> str:
    """生成用于观察大结果卸载的演示文本。"""
    return '\n'.join(f'实验行 {i}: 物流仓库记录，标记 TASK3-EVICTION。' for i in range(8000))


mode = sys.argv[1]
backend = FilesystemBackend(root_dir=root, virtual_mode=True) if mode in ('disk', 'eviction') else None
agent = create_deep_agent(model=model, backend=backend, checkpointer=InMemorySaver(), tools=[large_demo_data] if mode == 'eviction' else [], middleware=[FilesystemMiddleware(backend=backend, tool_token_limit_before_evict=1000)] if mode == 'eviction' else [])
config = {'configurable': {'thread_id': 'task3-' + mode}, 'run_name': 'task3_' + mode}
question = '请调用 large_demo_data 工具，并概述返回内容。' if mode == 'eviction' else '请依次调用 write_file 写入 /task3-note.txt 内容“物流实验 TASK3-KEY”，调用 read_file 读取，再调用 grep 搜索 TASK3-KEY，最后报告结果。'
result = agent.invoke({'messages': [{'role': 'user', 'content': question}]}, config=config)
for msg in result['messages']:
    for call in getattr(msg, 'tool_calls', []):
        print('TOOL_CALL', call['name'], call['args'])
    if getattr(msg, 'type', '') == 'tool':
        print('TOOL_RESULT', msg.name, str(msg.content)[:1600])
print('FINAL', result['messages'][-1].content)
print('STATE_FILES', list(result.get('files', {}).keys()))
print('DISK_EXISTS', (root / 'task3-note.txt').exists())

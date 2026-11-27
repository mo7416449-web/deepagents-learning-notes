import os
from pathlib import Path

from dotenv import load_dotenv
from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from langchain_openai import ChatOpenAI

load_dotenv('/home/olan/projects/research_deepagent/.env')
root = Path('/home/olan/projects/research_deepagent/practice/task5_subagents')
root.mkdir(parents=True, exist_ok=True)
source = Path('/mnt/e/datewhale/task3_实验记录.md').read_text(encoding='utf-8')
(root / 'task3_source.md').write_text(source, encoding='utf-8')
model = ChatOpenAI(model=os.environ['AGENTSEEK_MODEL'], api_key=os.environ['OPENAI_API_KEY'], base_url=os.environ['OPENAI_API_BASE'])
subagents = [
    {'name': 'researcher', 'description': '读取实验资料并提取关键事实，将摘要写入共享文件。', 'system_prompt': '你是资料分析员。读取 /task3_source.md，提取三个真实实验事实，写入 /facts.md，再简要返回结果。'},
    {'name': 'writer', 'description': '读取共享的事实文件并撰写简短说明。', 'system_prompt': '你是报告撰写员。读取 /facts.md，根据内容撰写不超过150字的中文总结，不添加文件以外的事实。'},
]
agent = create_deep_agent(model=model, backend=FilesystemBackend(root_dir=root, virtual_mode=True), subagents=subagents, system_prompt='你是任务协调员。必须先调用 task 委派 researcher 整理资料并写入共享文件，再调用 task 委派 writer 读取共享文件撰写报告，最后返回报告。')
result = agent.invoke({'messages': [{'role': 'user', 'content': '根据现有 Task 3 实验记录，先整理事实再写一段简短报告。请依次委派 researcher 和 writer。'}]}, config={'run_name': 'task5_subagent_demo', 'recursion_limit': 40})
for message in result['messages']:
    for call in getattr(message, 'tool_calls', []):
        print('主 Agent 调用:', call['name'], call['args'], flush=True)
    if getattr(message, 'type', '') == 'tool':
        print('主 Agent 收到:', message.name, str(message.content), flush=True)
print('最终报告:', result['messages'][-1].content, flush=True)
print('共享文件存在:', (root / 'facts.md').exists(), flush=True)

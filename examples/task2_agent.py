import os
import sys

from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI

load_dotenv()


def get_weather(city: str) -> str:
    """返回指定城市的固定天气演示文本，不查询真实天气。"""
    return f"{city}的演示天气：晴天。"


def convert_currency(amount: float, from_currency: str, to_currency: str = "CNY") -> str:
    """按固定演示汇率换算 USD 和 CNY，amount 为金额。"""
    rates = {"USD": 7.2, "CNY": 1.0}
    return f"{amount} {from_currency} = {amount * rates[from_currency] / rates[to_currency]:.2f} {to_currency}（演示汇率）"


model = ChatOpenAI(model=os.environ["AGENTSEEK_MODEL"], api_key=os.environ["OPENAI_API_KEY"], base_url=os.environ["OPENAI_API_BASE"], parallel_tool_calls=False)

mode = sys.argv[1] if len(sys.argv) > 1 else "custom"
if mode == "weather":
    tools = [get_weather]
    question = "请调用天气工具，查询北京的演示天气。"
elif mode == "custom":
    tools = [get_weather, convert_currency]
    question = "请先调用天气工具查询北京的演示天气，再调用货币换算工具，将100美元换成人民币，最后给出两个结果。"
else:
    raise ValueError("运行参数应为 weather 或 custom")

agent = create_deep_agent(model=model, tools=tools, system_prompt="你是一个助手。按用户要求使用工具，清楚说明工具返回的是演示数据。")
result = agent.invoke({"messages": [{"role": "user", "content": question}]}, config={"run_name": f"task2_{mode}"})
for message in result["messages"]:
    for call in getattr(message, "tool_calls", []):
        print(f"调用工具：{call['name']}，参数：{call['args']}")
    if getattr(message, "type", "") == "tool":
        print(f"工具结果：{message.content}")
print("最终回答：", result["messages"][-1].content)

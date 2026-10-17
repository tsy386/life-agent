import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from tools import (
    add_diet, get_diet, delete_diet,
    add_schedule, get_schedule, delete_schedule,
    add_expense, get_expenses, delete_expense
)

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com/v1",
    temperature=0
)

tools = [
    add_diet, get_diet, delete_diet,
    add_schedule, get_schedule, delete_schedule,
    add_expense, get_expenses, delete_expense
]
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=True)

def supervisor(state: MessagesState):
    messages = state["messages"]
    
    sys_msg = SystemMessage(
        content="""你是一个全能生活管家，拥有日程、饮食、财务三大专家。请根据用户的意图，精准调用工具。

【核心规则】
1. 添加/记录：调用 add_ 开头的工具（如 add_schedule, add_diet, add_expense）。
2. 查询/看看：调用 get_ 开头的工具（如 get_schedule）。
3. 删除/取消/记错了：调用 delete_ 开头的工具（如 delete_expense, delete_schedule）。
4. 替换/修改：例如“把低脂改成苹果”，你必须先调用 delete_diet(低脂)，再调用 add_diet(苹果)。

【绝对禁止】
- 绝对不允许用写入（add）去代替查询（get）。
- 如果用户要求删除，必须调用 delete_ 工具，绝对不能直接回复“已删除”但不调工具。"""
    )
    
    response = llm_with_tools.invoke([sys_msg] + messages)
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("supervisor", supervisor)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "supervisor")
builder.add_conditional_edges(
    "supervisor",
    lambda state: "tools" if state["messages"][-1].tool_calls else END,
    {"tools": "tools", END: END}
)
builder.add_edge("tools", "supervisor")

life_agent_graph = builder.compile()
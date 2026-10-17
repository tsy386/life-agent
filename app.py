import streamlit as st
from langchain_core.messages import HumanMessage
from graph import life_agent_graph

# 页面配置
st.set_page_config(page_title="多Agent生活管家", page_icon="🤖", layout="centered")

# ================= 侧边栏：控制面板 =================
with st.sidebar:
    st.header("⚙️ 控制面板")
    if st.button("🗑️ 清空当前对话", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("**使用提示**：\n- 试着说：安排明早8点吃药\n- 试着说：删除打车50元记录\n- 试着说：把低脂偏好改成苹果")

# ================= 主界面 =================
st.title("🤖 多 Agent 生活管家")
st.markdown("基于 LangGraph + DeepSeek 构建，支持**健康饮食、日程安排、财务记账**多专家协作与 CRUD 操作。")

# 初始化聊天历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 渲染历史消息
for msg in st.session_state.messages:
    if msg.type == "human":
        with st.chat_message("user"):
            st.write(msg.content)
    elif msg.type == "ai" and msg.content:
        with st.chat_message("assistant"):
            st.write(msg.content)

# 接收用户输入
if prompt := st.chat_input("试着对我说：我今晚8点有个重要会议，晚饭想吃点低脂的，顺便帮我记一下今天打车花了50块。"):
    # 显示用户消息
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    # 调用 LangGraph 执行，并展示实时状态（让界面显得更高级）
    with st.chat_message("assistant"):
        status_container = st.empty()
        with st.spinner("总管家正在调度..."):
            final_message = None
            
            # 使用 stream 捕获中间状态，展示 Agent 的流转
            for event in life_agent_graph.stream({"messages": st.session_state.messages}):
                for node_name, node_data in event.items():
                    status_container.caption(f"⚙️ 正在执行节点: `{node_name}`")
                    if "messages" in node_data:
                        final_message = node_data["messages"][-1]
            
            # 清除状态提示，打印最终结果
            status_container.empty()
            if final_message and final_message.content:
                st.write(final_message.content)
                
    if final_message:
        st.session_state.messages.append(final_message)
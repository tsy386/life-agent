# 🤖 Multi-Agent Life Assistant (多 Agent 生活管家)

基于 **LangGraph + DeepSeek + Streamlit** 构建的多智能体生活管家平台 MVP。

## 🌟 核心功能
- **多意图并发调度**：采用 Supervisor 架构，一句话可同时触发日程安排、饮食偏好、财务记账等多个专家的协同处理。
- **状态持久化（自我学习）**：使用本地 `memory.json` 模拟长期记忆，记录用户偏好。
- **严格的 CRUD 分离**：将 Agent 工具拆分为 `add_`、`get_`、`delete_`，有效解决大模型“工具幻觉”导致的数据污染问题。

## 🛠️ 技术栈
- **Agent 框架**：LangGraph (StateGraph, 条件路由)
- **大模型**：DeepSeek (兼容 OpenAI SDK)
- **前端界面**：Streamlit
- **开发语言**：Python 3.10

## 🚀 快速启动
1. 安装依赖：
   ```bash
   pip install streamlit langgraph langchain-openai python-dotenv

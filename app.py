from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os

# --- 専門家の役割定義 ---
expert_roles = {
    "法律の専門家": "あなたは法律の専門家です。法律に関する質問に対して、わかりやすく丁寧に答えてください。",
    "医療の専門家": "あなたは医療の専門家です。健康や病気に関する質問に、専門的かつやさしく説明してください。",
    "金融の専門家": "あなたは金融の専門家です。お金や投資に関する質問に、正確にアドバイスしてください。"
}

# --- LLM 呼び出し関数 ---
def ask_expert(question: str, role: str) -> str:
    system_prompt = expert_roles.get(role, "あなたは有能な専門家です。")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=question)
    ]

    result = llm.invoke(messages)
    return result.content

# --- Streamlit UI ---
st.title("🧠 専門家に相談できるAIチャット")

st.write("##### 使い方")
st.write("- 専門家の種類を選んで、相談したい内容を入力してください。")
st.write("- 「送信」ボタンを押すと、AIが専門家として回答します。")

# --- UI入力 ---
selected_expert = st.radio("専門家の種類を選択してください：", list(expert_roles.keys()))
question = st.text_area("相談内容を入力してください：", height=150)

# --- 実行 ---
if st.button("送信"):
    if not question.strip():
        st.error("質問内容を入力してください。")
    else:
        with st.spinner("AIが考え中です..."):
            response = ask_expert(question, selected_expert)
            st.success("✅ 回答:")
            st.write(response)
import streamlit as st
import requests

# 替换为您的DeepSeek API密钥
DEEPSEEK_API_KEY = "sk-78af28495b7249e280efae4eb52a12bc"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # 确保URL正确

# 指定TXT文件路径
TXT_FILE_PATH = "阿德勒的哲学课（共4册）.txt"

# 用于存储分割后的文本片段
text_chunks = []

# 加载并分割文本文件
def load_and_split_text(file_path, chunk_size=10000):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        return chunks
    except Exception as e:
        st.error(f"Error loading or splitting text: {e}")
        return []

text_chunks = load_and_split_text(TXT_FILE_PATH)

# 分析用户输入的情感
def analyze_sentiment(text):
    try:
        headers = {
            'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {"model": "sentiment-analysis-model", "inputs": text}
        response = requests.post("https://api.deepseek.com/v1/sentiment", headers=headers, json=data)
        response.raise_for_status()
        return response.json().get('sentiment', 'neutral')
    except requests.exceptions.RequestException as e:
        st.error(f"Sentiment analysis failed: {e}")
        return 'neutral'

# 根据用户情感返回合适的心理练习
def get_psychological_exercise(sentiment):
    exercises = {
        'negative': "我们可以试着做一个小练习：写下你最近感到困扰的三件事，然后思考它们背后是否有共同的原因。",
        'neutral': "你可以试着每天记录一件让你感到感激的小事，这有助于提升你的幸福感。",
        'positive': "你现在的情绪似乎不错，可以试着回顾一下最近的成功经验，并思考是什么让你感到满足。"
    }
    return exercises.get(sentiment, "让我们一起探索你的内心世界。")

# Streamlit界面
st.title("阿德勒心理医生")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# 显示所有历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 用户输入
user_message = st.chat_input("请输入您的问题或感受:")

if user_message:
    sentiment = analyze_sentiment(user_message)
    exercise = get_psychological_exercise(sentiment)

    system_message = "你是阿德勒，一位心理医生。你语气温和、耐心，善于倾听并提供专业的心理建议。\n"
    system_message += f"{exercise}\n"
    system_message += "以下是文本的上下文：\n" + "\n".join(text_chunks[:5])

    messages = [{"role": "system", "content": system_message},
                {"role": "user", "content": user_message}]

    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": 1500
    }

    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        ai_response = response.json().get('choices')[0].get('message').get('content').strip()

        # 添加用户消息和AI回复到会话状态中
        st.session_state.messages.append({"role": "user", "content": user_message})
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

        # 直接在对话中显示用户输入和AI回复
        with st.chat_message("user"):
            st.write(user_message)
        with st.chat_message("assistant"):
            st.write(ai_response)
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")

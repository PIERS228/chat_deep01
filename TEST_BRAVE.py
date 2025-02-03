import streamlit as st
import requests

# 替换为您的 DeepSeek API 密钥
DEEPSEEK_API_KEY = "sk-78af28495b7249e280efae4eb52a12bc"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

# 加载并分割文本文件
def load_and_split_text(file_url, chunk_size=10000):
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        text = response.text
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        return chunks
    except requests.exceptions.RequestException as e:
        print(f"Error downloading or splitting text: {e}")
        return []

# 根据您的GitHub仓库调整TXT文件路径为URL
TXT_FILE_URL = 'https://raw.githubusercontent.com/PIERS228/chat_deep01/main/%E9%98%BF%E5%BE%B7%E5%8B%92%E7%9A%84%E5%93%B2%E5%AD%B8%E8%AA%B2%EF%BC%88%E5%85%B14%E5%86%8A%EF%BC%89.txt'
text_chunks = load_and_split_text(TXT_FILE_URL)

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

def analyze_sentiment(text):
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "sentiment-analysis-model",
        "inputs": text
    }
    response = requests.post("https://api.deepseek.com/v1/sentiment", headers=headers, json=data)
    return response.json().get('sentiment', 'neutral')

def get_psychological_exercise(sentiment):
    exercises = {
        'negative': "我们可以试着做一个小练习：写下你最近感到困扰的三件事，然后思考它们背后是否有共同的原因。",
        'neutral': "你可以试着每天记录一件让你感到感激的小事，这有助于提升你的幸福感。",
        'positive': "你现在的情绪似乎不错，可以试着回顾一下最近的成功经验，并思考是什么让你感到满足。"
    }
    return exercises.get(sentiment, "让我们一起探索你的内心世界。")

st.title("心理咨询服务")

user_message = st.text_input("输入你的问题或感受:")

if user_message:
    sentiment = analyze_sentiment(user_message)
    exercise = get_psychological_exercise(sentiment)
    
    system_message = "你是阿德勒，一位心理医生。你语气温和、耐心，善于倾听并提供专业的心理建议。\n"
    system_message += f"{exercise}\n"  # 添加心理练习
    system_message += "以下是文本的上下文：\n" + "\n".join(text_chunks[:5])
    
    st.session_state.conversation_history.append({"role": "user", "content": user_message})
    
    messages = [{"role": "system", "content": system_message}] + st.session_state.conversation_history
    
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": 1500
    }

    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
    ai_response = response.json().get('choices')[0].get('message').get('content').strip()

    st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})

for conversation in st.session_state.conversation_history:
    if conversation["role"] == "user":
        st.write(f"用户: {conversation['content']}")
    else:
        st.write(f"阿德勒: {conversation['content']}")

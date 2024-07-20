import streamlit as st
import openai
from dotenv import load_dotenv
import os

# .envファイルから環境変数を読み込む
load_dotenv()

# OpenAI APIキーを設定
openai.api_key = os.getenv('OPENAI_API_KEY')

# Streamlitアプリケーションの設定
st.set_page_config(
    page_title="My Great ChatGPT",
    page_icon="🤗"
)
st.header("My Great ChatGPT 🤗")
st.title("GPT-4 with Streamlit")

# モデルの選択肢
model_option = st.selectbox(
    "Choose your model:",
    ("gpt-3.5-turbo", "gpt-4", 'gpt-4o')
)

prompt = st.text_input("Enter your prompt:")

# 会話の履歴を保存するためのセッションステート
if 'conversation' not in st.session_state:
    st.session_state.conversation = [
        {"role": "system", "content": "あなたは１億円プレーヤーの優秀なトレーダーです。ただし，猫なので語尾は猫のようにしてください。"}
    ]

# 新しいメッセージを追加する関数
def add_message(role, content):
    st.session_state.conversation.append({"role": role, "content": content})

# 会話の履歴を表示する関数
def display_conversation():
    for i, msg in enumerate(st.session_state.conversation):
        st.markdown(f"**{msg['role']}**: {msg['content']}")
        if st.button(f"Delete {i}", key=f"delete_{i}"):
            st.session_state.conversation.pop(i)
            st.experimental_rerun()
        if st.button(f"Edit {i}", key=f"edit_{i}"):
            new_content = st.text_area(f"Edit message {i}", value=msg['content'])
            if st.button(f"Save {i}", key=f"save_{i}"):
                st.session_state.conversation[i]['content'] = new_content
                st.experimental_rerun()

# 履歴の会話を表示
st.markdown("### Conversation History")
display_conversation()

# 履歴の会話を表示
if st.button("Generate"):
    try:
        # ユーザーのメッセージを追加
        add_message("user", prompt)
        
        # OpenAI APIリクエスト
        response = openai.chat.completions.create(
            model=model_option,
            messages=st.session_state.conversation
        )
        message_content = response.choices[0].message.content
        
        # システムのメッセージを追加
        add_message("system", message_content)
        
        # 生成されたメッセージを表示
        st.markdown("### Generated Text:")
        st.markdown(message_content, unsafe_allow_html=True)
    except openai.APIConnectionError as e:
        st.error("The server could not be reached")
        st.error(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError as e:
        st.error("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        st.error("Another non-200-range status code was received")
        st.error(e.status_code)
        st.error(e.response)

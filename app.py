
import pathlib
import textwrap
import google.generativeai as genai
import pandas as pd
from IPython.display import display
from IPython.display import Markdown
import streamlit as st


def to_markdown(text):
    text = text.replace('.', ' *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def setup_db():
    transaction_df = pd.read_csv('/data/transactions.csv')
    data_dict_df = pd.read_csv('/data/data_dict.csv')
    data_dict_text = '\n'.join('- '+data_dict_df['column_name']+
                            ': '+data_dict_df['data_type']+
                            '. '+data_dict_df['description'])

    df_name = 'transaction_df'

    return transaction_df, data_dict_df, data_dict_text, df_name

def gen_with_rag(question, prompt):

    transaction_df, data_dict_df, data_dict_text, df_name = setup_db()

try:
    key = st.secrets["gemini_api_key"]
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.0-flash-lite')

    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])

    st.title('Gemini Pro Test')

    def role_to_streamlit(role:str) -> str:
        if role == 'model':
            return 'assistant'
        else:
            return role

    for message in st.session_state.chat.history:
        with st.chat_message(role_to_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    if prompt := st.chat_input("Enter Text Here: "):
        st.chat_message('user').markdown(prompt)
        gen_with_rag("test","test")
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message('assistant'):
            st.markdown(response.text)
except Exception as e:
    st.error(f'Error: {e}')
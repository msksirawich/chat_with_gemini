
import google.generativeai as genai
import streamlit as st


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
        st.chat_messsage('user').markdown(prompt)
        response = st.session_state.chat.send_message(prompt)
        with st.chat_message('assistant'):
            st.markdown(response.text)
except Exception as e:
    st.error(f'Error: {e}')
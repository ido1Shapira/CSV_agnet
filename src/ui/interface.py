import streamlit as st

from src.agent.agent import Agent
from src.ui.enums.character import Character
from src.ui.utils import write_response, decode_response


class InteractionChat:
    def __init__(self):
        st.title("Ask your CSV 📈")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        self.csv_file = st.file_uploader("Upload a CSV file", type="csv")
        if self.csv_file is not None:
            self.agent = Agent(self.csv_file)

    def on_user_input(self):
        for message in st.session_state.messages:
            with st.chat_message(Character.user):
                st.markdown(message[0])
            with st.chat_message(Character.assistant):
                st.markdown(write_response(message[1]))

        if user_question := st.chat_input("Ask a question about your CSV: "):
            with st.chat_message(Character.user):
                st.markdown(user_question)

        if user_question is not None and user_question != "":
            with st.chat_message(Character.assistant):
                with st.spinner(text="In progress..."):
                    response = self.agent.run(user_input=user_question)
                    decoded_response = decode_response(response)
                    write_response(decoded_response)

            st.session_state.messages.append((user_question, decoded_response))

import os
from dotenv import load_dotenv
import openai
import requests
import json

import time
import logging
from datetime import datetime
import streamlit as st


load_dotenv()

client = openai.OpenAI()

model = "gpt-3.5-turbo"


    
# == Hardcoded ids to be used once the first code run is done and the assistant was created
assis_id = "asst_38kPaEjSDwkZPctpPittHHiT"
thread_id = "thread_rvJBTXJ2UCxChU33SEOEFotv"

# Initialize all the session
if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None


# Set up our front end page
# st.set_page_config(page_title="Study Buddy - Chat and Learn", page_icon=":books:")





st.session_state.start_chat = True

    # Create a new thread for this chat session
chat_thread = client.beta.threads.create()
st.session_state.thread_id = chat_thread.id
st.write("Thread ID:", chat_thread.id)

# If a file is uploaded, associate it with the current assistant

if st.session_state.file_id_list:
    for file_id in st.session_state.file_id_list:
        assistant_file = client.beta.assistants.files.create(
            assistant_id=assis_id, file_id=file_id
                )

        # Create a run with additional instructions
    run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assis_id,
            instructions="""Please answer the questions using the knowledge provided in textbook.pdf.
            when adding additional information, make sure to distinguish it with bold or underlined text.
            For more detailed information, please refer to the textbook.pdf. you must also cite where in the textbook you found this information. The tutoring you give should be straight to the point and you should provide examples to real world things whever you see fit.  """, 
    
        )


# Define the function to process messages with citations
def process_message_with_citations(message):
    """Extract content and annotations from the message and format citations as footnotes."""
    message_content = message.content[0].text
    annotations = (
        message_content.annotations if hasattr(message_content, "annotations") else []
    )
    citations = []

    # Iterate over the annotations and add footnotes
    for index, annotation in enumerate(annotations):
        # Replace the text with a footnote
        message_content.value = message_content.value.replace(
            annotation.text, f" [{index + 1}]"
        )

        # Gather citations based on annotation attributes
        if file_citation := getattr(annotation, "file_citation", None):
            # Check if the cited file is textbook.pdf
            if file_citation.filename == "textbook.pdf":
                citations.append(
                    f'[{index + 1}] {file_citation.quote} from {file_citation.filename}'
                )
        elif file_path := getattr(annotation, "file_path", None):
            # Placeholder for file download citation
            if file_path.filename == "textbook.pdf":
                citations.append(
                    f'[{index + 1}] Click [here](#) to download {file_path.filename}'
                )  # The download link should be replaced with the actual download path

    # Add footnotes to the end of the message content
    full_response = message_content.value + "\n\n" + "\n".join(citations)
    return full_response
# the main interface ...
st.title("Study Buddy")
st.write("Learn fast by chatting with your documents")


# Check sessions
if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show existing messages if any...
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # chat input for the user
    if prompt := st.chat_input("What's new?"):
        # Add user message to the state and display on the screen
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # add the user's message to the existing thread
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id, role="user", content=prompt
        )

        # Create a run with additioal instructions
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assis_id,
            instructions="""Please answer the questions using the knowledge provided in textbook.pdf.
        when adding additional information, make sure to distinguish it with bold or underlined text.
        For more detailed information, please refer to the textbook.pdf. """, 
        )

        # Show a spinner while the assistant is thinking...
        with st.spinner("Wait... Generating response..."):
            while run.status != "completed":
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id, run_id=run.id
                )
            # Retrieve messages added by the assistant
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )
            # Process and display assis messages
            assistant_messages_for_run = [
                message
                for message in messages
                if message.run_id == run.id and message.role == "assistant"
            ]

            for message in assistant_messages_for_run:
                full_response = process_message_with_citations(message=message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
                with st.chat_message("assistant"):
                    st.markdown(full_response, unsafe_allow_html=True)
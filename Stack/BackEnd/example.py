import os
import time
import random
import streamlit as st
import openai
from dotenv import load_dotenv

# Load environment variables and initialize OpenAI client
load_dotenv()
client = openai.OpenAI()
assis_id = "asst_CCGUYFRswjjNXrxndjagrJr6" # Replace with your actual assistant ID

# Quiz questions and answers
quiz_questions = [
    {
        "question": "What is the principle that states a quantum system can be in multiple states at once?",
        "options": ["Quantum entanglement", "Superposition", "Quantum tunneling", "Heisenberg Uncertainty Principle"],
        "answer": "Superposition"
    },
    {
        "question": "Which phenomenon describes the interconnectedness of quantum particles regardless of distance?",
        "options": ["Quantum entanglement", "Superposition", "Decoherence", "Quantum teleportation"],
        "answer": "Quantum entanglement"
    },
    {
        "question": "What is the uncertainty principle that asserts the fundamental limit to precision measurements of pairs of complementary variables?",
        "options": ["Einstein's Theory of Relativity", "Schrodinger's Cat Theory", "Heisenberg Uncertainty Principle", "Planck's Quantum Theory"],
        "answer": "Heisenberg Uncertainty Principle"
    },
    {
        "question": "What does 'qubit' stand for in quantum computing?",
        "options": ["Quantum bit", "Quality bit", "Quadratic bit", "Quick bit"],
        "answer": "Quantum bit"
    },
    # Add more questions here
    # ...
]

# Initialize session state
if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0

# Page configuration
st.set_page_config(page_title="Quantum Computing Study Buddy", page_icon=":books:")
st.title("QuantumEd")
st.write("Test your knowledge and learn more about quantum computing!")


    
def handle_chat(user_input, immediate_response=False):
    # Determine the current question index
    current_question_index = st.session_state.current_question_index

    # Ensure there's a chat history list for the current question
    if current_question_index not in st.session_state.chat_history:
        st.session_state.chat_history[current_question_index] = []

    # Process immediate response differently
    if immediate_response:
        st.session_state.chat_history[current_question_index].append({"role": "assistant", "content": user_input})
    else:
        st.session_state.chat_history[current_question_index].append({"role": "user", "content": user_input})
        with st.container():
            st.markdown(f"You: {user_input}")

    # Check if there's an active run on the current thread
    active_run = None
    try:
        # Attempt to get the latest run for the current thread
        runs = client.beta.threads.runs.list(thread_id=st.session_state.thread_id, limit=1)
        if runs.data:  # Ensure there is data
            latest_run = runs.data[0]
            if latest_run.status in ["running", "pending"]:
                active_run = latest_run
    except Exception as e:
        st.error(f"Error checking active runs: {e}")

    # Only create a new run if there is no active run
    if not active_run:
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assis_id,
            instructions=user_input,
        )

        # Wait for the response
        with st.spinner("Wait... Generating response..."):
            while run.status != "completed":
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id, run_id=run.id
                )

            # Retrieve and display the assistant's messages
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )
            assistant_messages_for_run = [
                message
                for message in messages
                if message.run_id == run.id and message.role == "assistant"
            ]

            for message in assistant_messages_for_run:
                st.session_state.chat_history[current_question_index].append({"role": "assistant", "content": message.content[0].text})
                with st.container():
                    st.markdown(f"Assistant: {message.content[0].text}")




def next_question():
    st.session_state.current_question_index = (st.session_state.current_question_index + 1) % len(quiz_questions)
    st.session_state.start_chat = False
    st.session_state.messages = []
    st.session_state.thread_id = None  # Resetting the thread_id if needed

    

# Display the current question
current_question = quiz_questions[st.session_state.current_question_index]
question = current_question["question"]
st.write(question)  # This line will display the question
options = current_question["options"]
answer = st.radio("Choose your answer:", options)


# Temporary variables for state changes
should_start_chat = False
should_move_to_next_question = False

# Check the answer and decide whether to start a chat session
if st.button("Submit"):
    correct = answer == current_question["answer"]
    response_message = "Correct!" if correct else "That's not quite right."
    if correct:
        st.success(response_message)
    else:
        st.error(response_message)

    should_start_chat = True
    st.session_state.correct_answer = correct

# Update the state to start chat session
if should_start_chat:
    st.session_state.start_chat = True
    explanation_prompt = f"Could you please explain why the answer '{answer}' is {'correct' if st.session_state.correct_answer else 'not correct'} for the question: '{question}'?"
    if st.session_state.thread_id is None:
        chat_thread = client.beta.threads.create()
        st.session_state.thread_id = chat_thread.id
    handle_chat(explanation_prompt, immediate_response=True)

# Initialize session state for new flags
if "continue_chat" not in st.session_state:
    st.session_state.continue_chat = False
if "move_to_next_question" not in st.session_state:
    st.session_state.move_to_next_question = False

# Chat session
if st.session_state.start_chat:
    user_input = st.text_input("Ask a follow-up question or request resources:")
    if user_input:
        handle_chat(user_input)

    if st.button("Continue Chatting"):
        st.session_state.start_chat = True

# Note: Moving the 'Next Question' button outside the chat session block
# Next Question button - ends the chat session and moves to the next question
if st.button("Next Question"):
    # Directly call next_question() and reset chat-related states
    st.session_state.current_question_index = (st.session_state.current_question_index + 1) % len(quiz_questions)
    st.session_state.start_chat = False
    st.session_state.messages = []
    st.session_state.thread_id = None  # Resetting the thread_id if needed

    # Manually force a rerun to immediately reflect the changes
    st.experimental_rerun()


# Process actions based on flags
if st.session_state.continue_chat:
    st.session_state.continue_chat = False
    st.session_state.start_chat = True

if st.session_state.move_to_next_question:
    st.session_state.move_to_next_question = False
    next_question()


# Display the chat for the current question
current_question_index = st.session_state.current_question_index
for message in st.session_state.chat_history.get(current_question_index, []):
    if message["role"] == "user":
        st.markdown(f"You: {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"Assistant: {message['content']}")
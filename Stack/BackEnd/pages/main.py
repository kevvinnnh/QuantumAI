import os
import time
import random
import streamlit as st
import openai
from dotenv import load_dotenv
import re


def show():
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
        "question": "Which phenomenon occurs when particles become interconnected such that the state of one cannot be described without the others?",
        "options": ["Quantum entanglement", "Superposition", "Decoherence", "Quantum teleportation"],
        "answer": "Quantum entanglement"
    },
    {
        "question": "What rule determines the probabilities of the outcomes of measurements on quantum systems?",
        "options": ["De Broglie Hypothesis", "The Born Rule", "Pauli Exclusion Principle", "Newton's Law of Universal Gravitation"],
        "answer": "The Born Rule"
    },
    {
        "question": "What is Schrödinger's Equation used for in quantum mechanics?",
        "options": ["To describe gravitational forces", "To predict chemical reactions", "To calculate energy levels", "To describe how the quantum state of a physical system changes over time"],
        "answer": "To describe how the quantum state of a physical system changes over time"
    },
    {
        "question": "Which algorithm demonstrated a potential threat to classical encryption methods?",
        "options": ["Grover's Algorithm", "Shor's Algorithm", "Deutsch-Jozsa Algorithm", "Vazirani's Algorithm"],
        "answer": "Shor's Algorithm"
    },
    {
        "question": "What describes the operators that can be applied to qubit states in quantum computing?",
        "options": ["Irreversible and non-unitary", "Unitary and reversible", "Non-involutive and reversible", "Asymmetric and non-linear"],
        "answer": "Unitary and reversible"
    },
    {
        "question": "What graphical representation is used to visualize the state of a qubit?",
        "options": ["The Fourier Transform", "The Newton Diagram", "The Bloch Sphere", "The Maxwell Chart"],
        "answer": "The Bloch Sphere"
    },
    {
        "question": "What concept is essential for understanding the capabilities and limits of quantum algorithms, according to the Gottesman-Knill and Solovay-Kitaev Theorems?",
        "options": ["Quantum supremacy", "The efficiency and approximation of quantum operations", "Quantum entanglement levels", "Quantum state coherence"],
        "answer": "The efficiency and approximation of quantum operations"
    } 

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
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answered_questions" not in st.session_state:
        st.session_state.answered_questions = set()

    # Page configuration
    st.title("Quantum AiEd")
    st.write("Test your knowledge and learn more about quantum computing!")
    st.markdown("<br><b>", unsafe_allow_html=True)


        
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
                st.markdown(f"<div style='display: none;'>You: {user_input}</div>", unsafe_allow_html=True)

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
                        st.markdown(f"<div style='display: none;'>Assistant: {message.content[0].text}</div>", unsafe_allow_html=True)



    def previous_question():
        st.session_state.current_question_index = (st.session_state.current_question_index - 1) % len(quiz_questions)
        st.session_state.start_chat = False
        st.session_state.messages = []
        st.session_state.thread_id = None  # Resetting the thread_id if needed

    def next_question():
        st.session_state.current_question_index = (st.session_state.current_question_index + 1) % len(quiz_questions)
        st.session_state.start_chat = False
        st.session_state.messages = []
        st.session_state.thread_id = None  # Resetting the thread_id if needed

    # Display buttons for navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Previous Question", key='prev_question'):
            previous_question()
            st.experimental_rerun()

    with col2:
        if st.button("Next Question", key='next_question'):
            next_question()
            st.experimental_rerun()
        st.markdown("<br>", unsafe_allow_html=True)

   # Temporary variables for state changes
    should_start_chat = False
    should_move_to_next_question = False

    current_question_index = st.session_state.current_question_index

    # Display the current question
    current_question = quiz_questions[st.session_state.current_question_index]
    question_number = st.session_state.current_question_index + 1
    question = current_question["question"]

    st.markdown(f"<h3>Question {question_number}: {question}</h3>", unsafe_allow_html=True)
    options = current_question["options"]
    if current_question_index not in st.session_state.answered_questions:
        answer = st.radio("Choose your answer:", options)

  
    # Check the answer and decide whether to start a chat session
    if st.button("Submit"):
        correct = answer == current_question["answer"]
        response_message = "Correct!" if correct else "That's not quite right."
        if correct:
            st.success(response_message)
            st.session_state.score += 1  # Increment score for correct answer
        else:
            st.error(response_message)
        st.session_state.answered_questions.add(st.session_state.current_question_index)  # Mark as answered

        # Update the state to start chat session
        st.session_state.start_chat = True
        explanation_prompt = f"Could you please explain why the answer '{answer}' is {'correct' if correct else 'not correct'} for the question: '{question}'?"
        if st.session_state.thread_id is None:
            chat_thread = client.beta.threads.create()
            st.session_state.thread_id = chat_thread.id
        explanation_container = st.empty()
        if explanation_prompt:
            explanation_container.write(explanation_prompt)
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

 # Show final score after all questions are answered
    if len(st.session_state.answered_questions) == len(quiz_questions):
        st.write(f"Quiz completed! Your score: {st.session_state.score}/{len(quiz_questions)}")

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
            if isinstance(message['content'], str):
        # If it's already a string, possibly no need for cleaning, but you can add checks if necessary
                cleaned_content = message['content']
            elif hasattr(message['content'], 'value'):  # Check if 'value' attribute exists
                # Access the 'value' attribute directly
                cleaned_content = message['content'].value
                # Optionally use regex to clean up if still necessary
                cleaned_content = re.sub(r"Text\(annotations=\[\], value='([^']+)'\)", r"\1", cleaned_content)
            else:
                # If the content is in an unexpected format, log it or handle it accordingly
                cleaned_content = "Content format is unexpected"
                st.write("Unexpected content structure:", message['content'])

            # Display the cleaned content
            st.markdown(f"Assistant: {cleaned_content}")



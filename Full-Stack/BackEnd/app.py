import streamlit as st
from pages import intro, main

# Set page configuration here, at the very top and only once
st.set_page_config(page_title="My Streamlit App", page_icon=":rocket:", layout="wide")

# Define pages
pages = [intro.show, main.show]

# Initialize session state for page navigation
if 'page_index' not in st.session_state:
    st.session_state.page_index = 0

# Function to navigate to the next page
def next_page():
    if st.session_state.page_index + 1 < len(pages):
        st.session_state.page_index += 1

# Function to navigate to the previous page
def prev_page():
    if st.session_state.page_index - 1 >= 0:
        st.session_state.page_index -= 1

# Navigation buttons
if st.session_state.page_index + 1 < len(pages):
    st.button("Next", on_click=next_page)

if st.session_state.page_index - 1 >= 0:
    st.button("Back to Intro", on_click=prev_page)

# Display the current page function
pages[st.session_state.page_index]()

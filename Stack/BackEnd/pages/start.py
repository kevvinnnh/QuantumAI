import streamlit as st

def show():
    """Displays a sophisticated introduction page for the Quantum Computing Quiz."""
    # Configure page settings

    # Use columns to create a centered layout for the content
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Add a welcoming header
        st.title("Welcome to the QuantumAI!")

        # Introduction text styled with a modern look
        st.markdown("""
            <div style='text-align: justify;'>
                    <br>
                Learn the fundamentals of quantum computing and test your knowledge.
                <br><br><br>
                        This interactive quiz will guide you through the basic concepts of quantum computing.
        Get ready to explore the fascinating world of qubits, superposition, and quantum entanglement
        through a series of engaging questions.
            </div>
            """, unsafe_allow_html=True)

        # Custom styles for a modern, clean look
        st.markdown("""
            <style>
                html, body, [class*="css"] {
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;  # Modern and readable font
                    background-color: #f4f4f8;  # Soft background color for reduced eye strain
                    color: #333366;  # Dark blue color for text for better readability
                }

            </style>
            """, unsafe_allow_html=True)
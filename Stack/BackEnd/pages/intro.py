import streamlit as st

def show():
    st.title("Quantum Computing Fundamentals")
    st.write("The following is information on the first chapter Quatum Computing: An Applied Approach by Jack D. Hidary ")

    # Expanded content for quantum computing introduction
    st.header("Chapter 1: Superposition, Entanglement, and Reversibility")
    st.subheader("1.1 Superposition and Entanglement")
    st.write("""
    - **Superposition**: Fundamental to quantum mechanics, superposition allows a quantum system (like a qubit) to be in multiple states simultaneously. This is not just a theoretical concept; it underpins the quantum computing's potential to process exponentially more data compared to classical computers.
    - **Entanglement**: Another cornerstone of quantum mechanics, entanglement occurs when pairs or groups of particles become interconnected such that the state of one particle cannot be described independently of the others, even when the particles are separated by large distances. This phenomenon was famously described by Einstein as "spooky action at a distance," and it is essential for protocols like quantum teleportation and for algorithms that outperform their classical counterparts.
    """)

    st.subheader("1.2 The Born Rule")
    st.write("""
    - Describes how to obtain probabilities from the state of a quantum system. It states that the probability of finding a system in a particular state is given by the square of the amplitude of the system's wave function for that state. This rule is fundamental for predicting outcomes in quantum experiments and operations.
    """)

    st.subheader("1.3 Schrödinger’s Equation")
    st.write("""
    - A key equation in quantum mechanics that describes how the quantum state of a physical system changes over time. It's particularly important in quantum computing for modeling the dynamics of quantum bits and understanding how quantum gates affect the state of a system.
    """)

    st.subheader("1.4 The Physics of Computation")
    st.write("""
    - Discusses the relationship between computation and physical laws, emphasizing that all computation, classical or quantum, is ultimately governed by the laws of physics. The section also touches on topics like the reversibility of quantum operations and the thermodynamic costs of computation.
    """)

    st.header("Chapter 2: A Brief History of Quantum Computing")
    st.subheader("2.1 Early Developments and Algorithms")
    st.write("""
    - Covers the initial theoretical groundwork laid by researchers like Richard Feynman and David Deutsch, who proposed the idea of a quantum computer and the first quantum algorithms, respectively.
    """)

    st.subheader("2.2 Shor and Grover")
    st.write("""
    - **Shor's Algorithm**: A groundbreaking algorithm for factoring integers efficiently, posing a significant threat to classical encryption methods.
    - **Grover's Algorithm**: Provides a quadratic speedup for unstructured search problems, showcasing quantum computing's potential to outperform classical computing in specific tasks.
    """)

    st.subheader("2.3 Defining a Quantum Computer")
    st.write("""
    - Outlines the basic criteria needed for a functional quantum computer, including coherent qubits, the ability to initialize, manipulate, and read out qubits, and the necessity of implementing error correction.
    """)

    st.header("Chapter 3: Qubits, Operators, and Measurement")
    st.subheader("3.1 Quantum Operators")
    st.write("""
    - Discusses the different types of quantum operators (unary, binary, ternary) and their role in manipulating qubit states to perform quantum computations.
    """)

    st.subheader("3.2 Comparison with Classical Gates")
    st.write("""
    - Illustrates how quantum gates differ from classical logic gates, highlighting their ability to perform operations based on complex superpositions and entanglements.
    """)

    st.subheader("3.3 Universality of Quantum Operators")
    st.write("""
    - Explains how a set of quantum gates can be combined to perform any quantum computation, similar to how a set of classical gates can perform any classical computation.
    """)

    st.subheader("3.4 Gottesman-Knill and Solovay-Kitaev Theorems")
    st.write("""
    - These theorems address the efficiency and approximation issues in quantum computing, crucial for understanding the capabilities and limits of quantum algorithms.
    """)

    st.subheader("3.5 The Bloch Sphere")
    st.write("""
    - Provides a graphical representation of the state of a qubit on the surface of a sphere, useful for visualizing the effects of quantum gates and measurements.
    """)

    st.subheader("3.6 The Measurement Postulate")
    st.write("""
    - Outlines the principles of measuring quantum states, emphasizing the probabilistic nature of quantum measurement and its impact on the state of the system.
    """)

    st.subheader("3.7 Computation-in-Place")
    st.write("""
    - Describes a computation paradigm unique to quantum computing where operations are performed directly on the data encoded in the quantum state, leveraging the principles of superposition and entanglement.
    """)


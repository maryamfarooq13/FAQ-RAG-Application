import streamlit as st
from apphelper import get_qa_chain

# Set page configuration
st.set_page_config(
    page_title="Knowledge Streams Q&A",
    page_icon="logo.png",  # Set the page icon to your logo
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTextInput>div>div>input {
        border: 2px solid #e91e63;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #e91e63;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ad1457;
        color: white;
    }
    .stHeader {
        color: #e91e63;
    }
    .stWrite {
        font-size: 18px;
        font-weight: bold;
        color: #333;
        margin-top: 10px;
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Use columns to place logo and title
col1, col2 = st.columns([1,8])

with col1:
    st.image('logo.png', width=100)  # Adjust the width as needed

with col2:
    st.title('Ask Knowledge Streams')

# Page description
st.markdown("""
    Welcome to the Knowledge Streams Q&A platform! 
    Enter your question below and get instant answers about our courses, fees, and more.
""")

# Input field for the question
question = st.text_input("Type your question here:", placeholder="e.g., What is the fee structure?")

if question:
    chain = get_qa_chain()
    response = chain(question)

    result = response['result']

    # Remove the initial "answer: "
    if result.lower().startswith('\nanswer:') or result.lower().startswith('?'):
        result = result.split(':', 1)[-1].strip()


    # Split the result string at the first occurrence of "question"
    answer = result.split('question', 1)[0].strip()

    st.header('Answer:')
    st.write(f"<div class='stWrite'>{answer}</div>", unsafe_allow_html=True)

# Footer with additional information
st.markdown("""
    ---
    <div style='text-align: center; color: #666;'>
        Powered by Knowledge Streams | 
        <a href="https://knowledge.tech/" target="_blank" style='color: #e91e63;'>Visit our website</a>
    </div>
""", unsafe_allow_html=True)

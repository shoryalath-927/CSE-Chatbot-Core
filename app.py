import streamlit as st
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate



import streamlit as st
st.title("CSE Chatbot")

# ----------------------------
# Load Environment Variables
# ----------------------------
load_dotenv()

my_key = os.getenv("GROQ_API_KEY")


# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="CSE Core Subject Chatbot", page_icon="📘")
st.title("📘 CSE Core Subject Personalized Chatbot")


# ----------------------------
# User Personalization Section
# ----------------------------
st.sidebar.header("👤 Student Profile")

name = st.sidebar.text_input("Enter Your Name")
semester = st.sidebar.selectbox("Select Semester", ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"])
answer_style = st.sidebar.selectbox(
    "Answer Style",
    ["Exam Oriented", "Conceptual Explanation", "Short Notes"]
)


# ----------------------------
# Load Embeddings + Vector DB
# ----------------------------
@st.cache_resource
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore


vectorstore = load_vector_store()


# ----------------------------
# Load LLM
# ----------------------------
llm = ChatGroq(
    api_key=my_key,
    temperature=0.2,
    model_name="llama-3.1-8b-instant"
)


# ----------------------------
# Create Prompt Template
# ----------------------------
prompt_template = """
You are a Computer Science Professor.

Student Name: {name}
Semester: {semester}
Preferred Answer Style: {answer_style}

Answer ONLY from the provided context.
If answer is not available in context, say:
"The answer is not available in the provided CSE core books."

Context:
{context}

Question:
{question}

Answer:
"""




# ----------------------------
# Create Retriever + QA Chain
# ----------------------------
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff"
)

# ----------------------------
# Chat Section
# ----------------------------
question = st.text_input("💬 Ask your CSE question:")

if question:
   personalized_query = f"""
    You are a Computer Science professor.

    Student Name: {name}
    Semester: {semester}
    Answer Style: {answer_style}

    Answer clearly using CSE core subject knowledge.

    Question:
    {question}
    """

   result = qa_chain.invoke({
        "query": personalized_query
    })
   st.markdown("### 📘 Answer:")
   st.write(result["result"])
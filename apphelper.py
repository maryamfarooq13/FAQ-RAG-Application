# to set environment with hugging face API token
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Access the token using os.getenv
hf_token = os.getenv('hugging_face_hub_token')
# Set the token in os.environ for Hugging Face Hub API
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token
# Loader
from langchain.document_loaders import CSVLoader
# for embedding model
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
# for vector database
from langchain.vectorstores import FAISS
# for calling models from hugging face
from langchain_huggingface import HuggingFaceEndpoint
# for generation
from langchain.chains import RetrievalQA
# to define prompt to prevent hallucination
from langchain.prompts import PromptTemplate

# setting llm
repo_id="mistralai/Mistral-7B-Instruct-v0.3"
llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.1, token= hf_token)

fast_embeddings = FastEmbedEmbeddings()

def get_qa_chain():
    # load the vector database from the local folder
    vector_db = FAISS.load_local(
        'D:/PROJECTS/Gen Ai Projects/KS RAG Application/vector_db/faiss.index',
        embeddings=fast_embeddings,
        allow_dangerous_deserialization=True)

    # create a retriever for querying the vector database
    retriever = vector_db.as_retriever(search_kwargs={"k": 2})

    prompt_template = """Only use the exact context to the answer the user's question, don't add explicit text to answer.
    Give Single, to the point and short answer. If you don't have an answer, kindly say "Sorry, I don't know, PLease contact us: https://knowledge.tech/contact-us", 
    don't try to make up an answer.

    Context = {context}
    Question: {question}"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"])

    chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type='stuff',
                                        retriever=retriever,
                                        input_key='question',
                                        return_source_documents=False,
                                        chain_type_kwargs={'prompt': prompt})

    return chain

if __name__ == "__main__":
    chain = get_qa_chain()
    print(chain('do you facilitate in job?'))
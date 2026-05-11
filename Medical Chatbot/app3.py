from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Extract text from PDF files
def load_pdf_files(data):
    loader = DirectoryLoader(
        data,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()
    return documents
extracted_data = load_pdf_files("data")

from typing import List
from langchain_core.documents import Document

def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs
minimal_docs = filter_to_minimal_docs(extracted_data)
# Split the documents into smaller chunks
def text_split(minimal_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
    )
    texts_chunk = text_splitter.split_documents(minimal_docs)
    return texts_chunk
texts_chunk = text_split(minimal_docs)
from langchain.embeddings import HuggingFaceEmbeddings

def download_embeddings():
    """
    Download and return the HuggingFace embeddings model.
    """
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name
    )
    return embeddings

embedding = download_embeddings()
from dotenv import load_dotenv
import os
load_dotenv()
PINECONE_API_KEY = os.getenv("pinecone_api_key")


os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

from pinecone import Pinecone
pc = Pinecone(api_key="pcsk_6U88Sa_92PWKqFtVTe7HCwBif6LZaHeiidGYeQ4VWpo1NhKCsQc4fKbVwRfkYNC7o4w7br")
# Load Existing index


# Embed each chunk and upsert the embeddings into your Pinecone index.
from pinecone import ServerlessSpec

index_name = "medical-chatbot"

if not pc.has_index(index_name):
    pc.create_index(
        name = index_name,
        dimension=384,  # Dimension of the embeddings
        metric= "cosine",  # Cosine similarity
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )


# Load Existing index

from langchain_pinecone import PineconeVectorStore
# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embedding
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":6})

from dotenv import load_dotenv
# Load variables from .env
load_dotenv()

# Access the key securely

key = os.getenv("GROQ_API_KEY")
from langchain_groq import ChatGroq


chatModel = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=key,
    temperature=0
)

import sys
import types

# Create fake module for missing memory
fake_memory_module = types.ModuleType("langchain_core.memory")
sys.modules["langchain_core.memory"] = fake_memory_module
import sys
import types

# Create fake module
fake_memory_module = types.ModuleType("langchain_core.memory")

# Create dummy BaseMemory class
class BaseMemory:
    pass

# Attach it to module
fake_memory_module.BaseMemory = BaseMemory

# Register module
sys.modules["langchain_core.memory"] = fake_memory_module
from langchain.chains import create_retrieval_chain,create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# This prompt re-writes the user query based on chat history
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

history_aware_retriever = create_history_aware_retriever(
    chatModel, retriever, contextualize_q_prompt
)

# --- 4. Answer Logic ---
system_prompt = (
    "Analyze the provided medical context carefully. Identify the specific symptoms or conditions mentioned. "
    "If the context contains specific treatments or dosages, list them clearly. "
    "If the context is insufficient, state exactly what is missing."
    "\n\n"
    "{context}"
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(chatModel, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)





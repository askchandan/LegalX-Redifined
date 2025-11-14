# build_vector_store.py

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer
import json
from langchain.docstore.document import Document


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
model.save('./all-MiniLM-L6-v2')  # Save the model to a specific directory


# Load all PDFs from folder
pdf_folder = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(pdf_folder):
    print(f"PDF folder '{pdf_folder}' does not exist. Please create it and add your PDFs.")
    pdf_paths = []
else:
    pdf_paths = [os.path.join(pdf_folder, f) for f in os.listdir(pdf_folder) if f.endswith(".pdf")]



documents = []
for path in pdf_paths:
    print(f"Loading: {path}")
    loader = PyPDFLoader(path)
    documents.extend(loader.load())

print(f"Loaded {len(documents)} documents.")

# Load JSON file and add its entries as documents
json_path = os.path.join(pdf_folder, "ipc_sections_cleaned.json")
if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        ipc_data = json.load(f)
    print(f"Loaded {len(ipc_data)} entries from JSON.")
    for entry in ipc_data:
        # Combine fields into a single string for vectorization
        content = f"Section: {entry.get('Section', '')}\nOffense: {entry.get('Offense', '')}\nPunishment: {entry.get('Punishment', '')}"
        documents.append(Document(page_content=content, metadata={"source": "ipc_json", "section": entry.get("Section", "")}))
else:
    print(f"JSON file '{json_path}' not found. Skipping JSON import.")

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)
print(f"Split into {len(chunks)} chunks.")

# Embedding model (local HuggingFace)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Build Chroma vectorstore
persist_directory = os.path.join(os.path.dirname(__file__), "chroma_store")
vectorstore = Chroma.from_documents(documents=chunks, embedding=embedding_model, persist_directory=persist_directory)
# vectorstore.persist() -- since persistance is now automatic in chroma 0.4x or above
print(f"Chroma vector store saved to: {persist_directory}")
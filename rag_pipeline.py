import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

# Configuration
DOCS_DIR = "docs"
CHROMA_DB_DIR = "chroma_db"

def initialize_vector_store():
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        print(f"Created '{DOCS_DIR}' directory. Please add PDF compliance documents here.")
        
    print("Loading documents from directory...")
    loader = PyPDFDirectoryLoader(DOCS_DIR)
    documents = loader.load()
    
    if not documents:
        print("No documents found in 'docs/' directory. Add some to build the Vector store.")
        # Create a dummy markdown doc if no PDFs
        with open(os.path.join(DOCS_DIR, "dummy_policy.txt"), "w") as f:
            f.write("Artificial Intelligence usage requires prior compliance board approval. "
                    "Models shall not use PII data. System must maintain an audit log of tokens and model versions.\n"
                    "Automated emails are strictly regulated by Section 4A.")
        from langchain_community.document_loaders import DirectoryLoader
        txt_loader = DirectoryLoader(DOCS_DIR, glob="**/*.txt")
        documents = txt_loader.load()

    print(f"Loaded {len(documents)} document pages.")

    # Chunking: Implement Semantic/Recursive chunking
    # We use 500 characters with 100 overlap to keep legal phrasing intact
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Split down to {len(chunks)} chunks.")

    # Embeddings implementation details: Sentence-Transformer (Local for Privacy/Governance)
    print("Initializing Sentence-Transformer Embeddings (all-MiniLM-L6-v2)...")
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"Creating Chroma DB at {CHROMA_DB_DIR}...")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )
    
    db.persist()
    print("Vector Store successfully built and persisted.")

if __name__ == "__main__":
    initialize_vector_store()

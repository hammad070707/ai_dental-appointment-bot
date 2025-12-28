import os
from dotenv import load_dotenv
from langchain_core.documents import Document 
from langchain_community.vectorstores import Chroma
from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
load_dotenv(os.path.join(root_dir, '.env'))
FAQ_FILE_PATH = os.path.join(root_dir, 'data', 'faqs.txt')

vectorstore = None

def initialize_knowledge_base():
    """
    This function reads the text file and creates a searchable 
    vector database using OpenAI Embeddings.
    """
    global vectorstore
    
    if not os.path.exists(FAQ_FILE_PATH):
        print(f"❌ Critical Error: Data file file error! Path: {FAQ_FILE_PATH}")
        return None
    print("📚 Loading Knowledge Base (OpenAI Powered)...")
    documents = []
    try:
        with open(FAQ_FILE_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()    
        for line in lines:
            text = line.strip()
            if text and len(text) > 5: 
                documents.append(Document(page_content=text))
        print(f"✂️ Processed {len(documents)} Data Lines.")
        print("⬇️ Connecting to OpenAI Embeddings API...")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        vectorstore = Chroma.from_documents(
            documents=documents, 
            embedding=embeddings,
            collection_name="clinic_faqs_openai"
        )
        print("✅ Knowledge Base Ready! (High Speed Mode)")
        return vectorstore

    except Exception as e:
        print(f"❌ Error initializing Knowledge Base: {e}")
        return None

@tool
def lookup_policy_faq(query: str):
    """
    Use this tool to answer questions about the clinic's:
    - Services & Pricing (Fees)
    - Doctor Name
    - Address / Location
    - Timings
    - Policies
    Input should be the user's question (e.g., "Scaling price?", "Kahan hai clinic?").
    """
    global vectorstore

    if vectorstore is None:
        initialize_knowledge_base()
    if vectorstore is None:
        return "System Error: Database not loadd"
    print(f"🔍 Searching for: '{query}'")
    docs = vectorstore.similarity_search(query, k=3)
    
    if not docs:
        return "Sorry, I couldn't find any information regarding this"
    info = "\n".join([f"- {doc.page_content}" for doc in docs])
    return f"Database Search Result (Context):\n{info}"

if __name__ == "__main__":
    print("\n--- 🧪 Testing FAQ Module ---")
    initialize_knowledge_base()
    test_query = "Any question?"
    print(f"\n❓ User: {test_query}")
    
    result = lookup_policy_faq.invoke(test_query)
    print(f"💡 Tool Output:\n{result}")
    
    print("\n--- ✅ Test Complete ---")


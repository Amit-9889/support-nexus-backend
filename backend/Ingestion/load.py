from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.vector_database.vector_store import vector_db
from dotenv import load_dotenv

load_dotenv()

class data_loader:

    def __init__(self,path:str):

        self.path = path

    def load(self):

        document_object = PyPDFLoader(self.path)

        documents = document_object.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)

        chunks = text_splitter.split_documents(documents)

        ## Initializing pinecone

        vector_db().ingest(chunks)

        return "Document uploaded successfully"

        
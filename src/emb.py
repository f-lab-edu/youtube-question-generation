import time, math
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

def make_embedder():
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

hf = make_embedder()

def document_split(texts):
  # Document splitting
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
  texts = text_splitter.split_documents(texts)

  db = Chroma.from_documents(texts, hf) 
  return db
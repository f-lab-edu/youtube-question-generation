from typing import List
from fastapi import Depends
from pydantic import BaseModel
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

class SpliteDoc(BaseModel):
    '''
    [
        Document(page_content="..."),
        Document(page_content="...")
    ]
    '''
    texts : List[Document]
    
def make_embedder() -> HuggingFaceEmbeddings:
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

def document_split(texts:SpliteDoc, embedder: HuggingFaceEmbeddings=Depends(make_embedder)) -> Chroma:
  # Document splitting
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
  texts = text_splitter.split_documents(texts)

  db = Chroma.from_documents(texts, embedder) 
  return db

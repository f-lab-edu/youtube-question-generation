import torch
import openai
import time, math
import yt_dlp as yt
from pytube import YouTube
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


youtube_url = "https://www.youtube.com/watch?v=ttoAibdUOAU"
AUDIO_FOLDER = "."

# Define download options
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': f'{AUDIO_FOLDER}/%(id)s.%(ext)s',
}

with yt.YoutubeDL(ydl_opts) as ydl:
  ydl.download([youtube_url])
  
yt = YouTube(youtube_url)
audio = yt.streams.get_audio_only()
fn = audio.download(output_path=AUDIO_FOLDER, filename=f'ttoAibdUOAU.mp4')
# fn = audio.download(output_path=os.path.join(AUDIO_FOLDER, 'clips'), filename=f'{video_id}.mp4')

device = "cuda:0"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model_id = "distil-whisper/distil-large-v2"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id,
    torch_dtype=torch_dtype,
    low_cpu_mem_usage=True,
    use_safetensors=True,
    use_flash_attention_2=True # Remove is using a CPU
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipeline = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=15,
    batch_size=16,
    torch_dtype=torch_dtype,
    device=device,
)

def transcribe_file(filename):
    print (f"Transcribing New file: {filename}")
    transcription = pipeline(filename, return_timestamps=True)
    return transcription

audio_filename = f'./ttoAibdUOAU.webm'
start = time.time()
transcription = transcribe_file(audio_filename) 
runtime = time.time() - start
rounded_runtime = math.ceil(runtime)
print("Runtime: ", rounded_runtime, " seconds")
print(transcription['text'][:100])

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
texts = [Document(page_content=transcription['text'])]
# Document splitting
text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
texts = text_splitter.split_documents(texts)

db = Chroma.from_documents(texts, hf) ##

def make_qa_chain():
    # openai.api_key = "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"
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key="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")
    return RetrievalQA.from_chain_type(
        llm,
        retriever=db.as_retriever(search_type="mmr", search_kwargs={'fetch_k': 3}),
        return_source_documents=True
    )

qa_chain = make_qa_chain()

def ask_question(q):
    result = qa_chain({"query": q}) #############################
    print(f"Q: {result['query'].strip()}")
    print(f"A: {result['result'].strip()}\n")
    print('\n')
    
## Demonstration original question: **What is retrieval augmented generation (RAG)?**
q = "What is retrieval augmented generation (RAG)?"
ask_question(q)
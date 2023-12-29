import logging
from functools import lru_cache

import torch
from pydantic import BaseModel
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from transformers.pipelines import Pipeline

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model_id = "distil-whisper/distil-large-v2"


class TextResponse(BaseModel):
    # speech -> text
    transcription: str


@lru_cache(maxsize=None)
# Singleton Pattern
def get_pipeline() -> Pipeline:
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True,
        use_flash_attention_2=True,  # Remove is using a CPU
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)
    return pipeline(
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


def transcribe_file(filename: str) -> TextResponse:
    logging.info("Transcribing New file: {filename}")

    pipeline = get_pipeline()
    transcription = pipeline(filename, return_timestamps=True)
    return TextResponse(transcription=transcription["text"])

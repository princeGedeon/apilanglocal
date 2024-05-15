import os
import uuid

import torch
import whisper
from TTS.api import TTS
from fastapi import FastAPI, HTTPException, UploadFile, File
from speechbrain.inference import EncoderASR
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from transformers import pipeline

from models.entry import TextInput, TranslationInput
from utils.asr import asr_fon, asr_multi
from utils.mt import translate_text
from utils.tts import text_to_speech_fon, text_to_speech_yor

# Directory to save generated audio files and uploads
output_dir = "output"
upload_dir = "uploads"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(upload_dir, exist_ok=True)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Global variables to hold the models
tts_fon_model = None
tts_yor_model = None
asr_fon_model = None
multi_model =None

@app.on_event("startup")
async def load_models():
    global tts_fon_model, tts_yor_model, asr_fon_model,multi_model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts_fon_model = pipeline("text-to-speech", model="facebook/mms-tts-fon")
    tts_yor_model = TTS("tts_models/yor/openbible/vits").to(device)
    asr_fon_model = EncoderASR.from_hparams(source="speechbrain/asr-wav2vec2-dvoice-fongbe",
                                        savedir="pretrained_models/asr-wav2vec2-dvoice-fongbe")

    multi_model=whisper.load_model("medium")

@app.post("/tts/fon")
async def tts_fon_endpoint(text_input: TextInput):
    try:
        file_url = f"output/temp_fon.mp3"
        file_name = text_to_speech_fon(tts_fon_model, text_input.text,file_url)

        return {"message": "Audio file created successfully!", "file_url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tts/yor")
async def tts_yor_endpoint(text_input: TextInput):
    try:
        file_url = f"output/temp_yor.mp3"
        file_name = text_to_speech_yor(tts_yor_model, text_input.text,file_url)
        return {"message": "Audio file created successfully!", "file_url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/asr/fon")
async def asr_fon_endpoint(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(upload_dir, f"{uuid.uuid4()}_{file.filename.replace(' ','')}")
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        print(file_path)
        text,lang = asr_fon(asr_fon_model, file_path)
        return {"message": "Transcription successful!", "text": text,"lang":lang}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/asr/multi/{lang}")
async def asr_multi_endpoint(lang: str = "yor",file: UploadFile = File(...)):
    try:
        file_path = os.path.join(upload_dir, f"{uuid.uuid4()}_{file.filename}")
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        text,lang = asr_multi(multi_model, file_path,lang)
        return {"message": "Transcription successful!", "text": text,"lang":lang}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
async def translate_endpoint(translation_input: TranslationInput):
    try:
        translated_text = translate_text(
        translation_input.source, translation_input.target, translation_input.text)

        return {"translated_text": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/output", StaticFiles(directory="./output"), name="output")
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
#from transformers import pipeline
import shutil
import os
from inference import inference  

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploaded_audio"


@app.get('/')
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/get_answer/')
def get_answer(query: str):
    response = {
        "answer": inference(query)  
    }
    return response

def speech2text(audio_path: str) -> str:
    #pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large")
    result ="How to clean and maintain the Shredder?"
    # result=pipe(audio_path)
    # return result["text"]
    return result


@app.post('/get_voice_answer/')
async def get_voice_answer(audio: UploadFile = File(...)):
    audio_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    with open(audio_path, "wb") as audio_file:
        shutil.copyfileobj(audio.file, audio_file)
    transcribed_text = speech2text(audio_path)
    answer = inference(transcribed_text)
    return {"answer": answer}


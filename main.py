from fastapi import FastAPI, UploadFile, File
import whisper
from gtts import gTTS
import shutil

app = FastAPI()

model = whisper.load_model("base")


def generate_llm_response(text):
    return f"I heard you say: {text}. How can I help further?"


@app.get("/")
def home():
    return {"message": "Voice AI Backend Working"}


@app.post("/voice-input")
async def voice_input(file: UploadFile = File(...)):

    # save uploaded audio
    with open("audio.mp3", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # speech → text using :contentReference[oaicite:0]{index=0}
    result = model.transcribe("audio.mp3")
    transcript = result["text"]

    # generate response
    response_text = generate_llm_response(transcript)

    # text → speech using :contentReference[oaicite:1]{index=1}
    tts = gTTS(response_text)
    tts.save("response.mp3")

    return {
        "transcript": transcript,
        "response": response_text,
        "audio_download": "http://127.0.0.1:8000/response.mp3"
    }
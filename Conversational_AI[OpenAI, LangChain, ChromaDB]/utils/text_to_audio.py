
import os
from pathlib import Path
from openai import OpenAI

OpenAI_Key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=OpenAI_Key)
audio_path = Path(__file__).parent / "speech.mp3"

async def convertToAudio(txt):    
    response = client.audio.speech.create(model="tts-1",
        voice="alloy",
        input=txt,
    )
    response.stream_to_file(audio_path)

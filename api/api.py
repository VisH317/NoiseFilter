from fastapi import FastAPI, WebSocket
from multiprocessing import Process
import sounddevice as sd 
import base64
import numpy as np

CHUNK = 2048
sample_freq = 44100

virtual_input_channel = "bruh"
virtual_output_channel = "bruh"

# audio helper fucntions

# start output websocket process
p = Process(target=send_output)
p.daemon = True
p.start()

inputaudio = []
streaming = False

@app.websocket("/input")
async def getInput(websocket: WebSocket):
    await websocket.accept()
    try:
        async for message in websocket:
            msg = json.loads(message)
            if msg['event']=='start':
                streaming = True
            if msg['event']=='stop':
                streaming=False
            if msg['event']=='media':
                inputaudio.append(base64.b64decode(media['payload']))
                rec = await process_audio()
                await websocket.send_text(base64.b64encode(rec))

async def process_audio():
    sd.default.device = virtual_input_channel
    rec = sd.playrec(np.array(inputaudio), fs=sample_freq)
    inputaudio.clear()
    return rec

async def send_output():


import requests
import pyaudio
import wave
import os

FORMAT = pyaudio.paInt16
CHUNK = 1024
WIDTH = 2
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILE = "temp.wav"

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH, unsigned=False),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)  #read audio stream
    stream.write(data, CHUNK)  #play back audio stream
    frames.append(data)

print("* done")

stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open(WAVE_OUTPUT_FILE, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(WIDTH))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

with open('./temp.wav', 'rb') as f:
    r = requests.post('http://localhost:5000/model/predict', files={'./temp.wav': f})

# fill this ßup!!!!!!!!!!!!

#os.remove("./temp.wav")
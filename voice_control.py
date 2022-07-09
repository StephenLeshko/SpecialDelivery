import os
import pathlib
import wave
import pyaudio
 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf
import audioop
 
from tensorflow.keras import layers
from tensorflow.keras import models
from IPython import display
 
 
#setting basics for creating an audio file
 
FRAMES_PER_BUFFER = 800 #frames per second
FORMAT = pyaudio.paInt16 #if stereo, make 32
CHANNELS = 1 #if stereo, make 2
RATE = 16000 #recording frequency
 
 
 
#everything for the model
 
commands = ['down', 'go', 'left', 'right', 'stop', 'up']
 
model = models.load_model('sd_model.h5')
 
 
#turns audio into tensor
def decode_audio(audio_binary):
    # Decode WAV-encoded audio files to `float32` tensors, normalized
    # to the [-1.0, 1.0] range. Return `float32` audio and a sample rate.
    audio, _ = tf.audio.decode_wav(contents=audio_binary)
    # Since all the data is single channel (mono), drop the `channels`
    # axis from the array.
    return tf.squeeze(audio, axis=-1)
 
#turns wave file into spectrogram
def get_spectrogram(waveform):
    # Zero-padding for an audio waveform with less than 16,000 samples.
    input_len = 16000
    waveform = waveform[:input_len]
    zero_padding = tf.zeros(
        [16000] - tf.shape(waveform),
        dtype=tf.float32)
       
    # Cast the waveform tensors' dtype to float32.
    waveform = tf.cast(waveform, dtype=tf.float32)
    # Concatenate the waveform with `zero_padding`, which ensures all audio
    # clips are of the same length.
    equal_length = tf.concat([waveform, zero_padding], 0)
    # Convert the waveform to a spectrogram via a STFT.
    spectrogram = tf.signal.stft(
        equal_length, frame_length=255, frame_step=128)
    # Obtain the magnitude of the STFT.
    spectrogram = tf.abs(spectrogram)
    # Add a `channels` dimension, so that the spectrogram can be used
    # as image-like input data with convolution layers (which expect
    # shape (`batch_size`, `height`, `width`, `channels`).
    spectrogram = spectrogram[..., tf.newaxis]
    return spectrogram
 
#gets the file
 
def predict_audio(file_name):
    audio_binary = tf.io.read_file(file_name)
    waveform = decode_audio(audio_binary)
    spectrogram = get_spectrogram(waveform)
    spectrogram = tf.reshape(spectrogram, [1, 124, 129, 1])
    prediction = model(spectrogram)
    return commands[int(tf.argmax(prediction, 1).numpy())]
 
 
#idea is that the stream will continously run, and it will write data
#once the audio reaches a certain volume, create a file, then run
#the master audio function, then delete that file, then
#reset what is in the loop
#ends recording after 1 second, executes, and begins
 
#----THE LOOP----
# data = stream.read(CHUNK)
# rms = audioop.rms(data, 2)
pa = pyaudio.PyAudio()
 
stream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)
 
seconds = 10
frames = []
second_tracking = 0
second_count = 0
making_file = False
file_count = 0
file_max = 1
 
#gets called once the making_file has returned to false
def create_audio(frames):
    obj = wave.open('noise.wav', 'wb')
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(pa.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b''.join(frames))
    obj.close()
 
def kill_audio():
    os.remove('noise.wav')
 
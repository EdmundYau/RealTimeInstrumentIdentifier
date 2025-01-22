# Import Libraries
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import layers, models
import tensorflow_datasets as tfds
import IPython.display as ipd
import librosa
import os

def mel_spectrogram(example):
    # Extract and normalize
    audio = example["audio"].numpy()
    audio = librosa.util.normalize(audio)

    # Acquire Mel spectrogram
    mel_spect = librosa.feature.melspectrogram(
        y=audio,           # Audio time data
        sr=44100,          # Sample rate
        n_fft=2048,        # Window size
        hop_length=512,    # Hop size
        n_mels=128         # Number of Mel bands
    )
    mel_spect_db = librosa.power_to_db(mel_spect, ref=np.max)

    return mel_spect_db

# Create CNN Model
input_shape = (128, 128, 1)
num_classes = 10

model = models.Sequential()
model.add(layers.Conv2D(16, (3, 3), activation='relu', input_shape=input_shape))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(num_classes, activation='softmax'))

model.compile(optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])
    

track_dirs = [os.path.join("slakh2100_flac_redux", d) for d in os.listdir("slakh2100_flac_redux") if d.startswith("Track")]

with open(output_file, "w") as f:
    for track in track_dirs:
        result = extract_program_numbers(track)
        if result:
            f.write(result)

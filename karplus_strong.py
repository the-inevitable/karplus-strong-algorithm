"""
The simulation proceeds until the sample buffer is filled in a kind of feed-
back scheme. For each step of the simulation, we'll do the following:
1. Store the first value from the ring buffer in the samples buffer.
2. Calculate the average of the first two elements in the ring buffer.
3. Multiply this average value by an attenuation factor (in this case, 0.996).
4. Append this value to the end of the ring buffer.
5. Remove the first element of the ring buffer.
"""

import os
import wave
import time
import random
import argparse
from collections import deque

import pygame
import numpy as np

# Notes of a Pentatonic Minor scale.
# Piano C4-E(b)-F-G-B(b)-C5
pm_notes = {'C4': 262, 'Eb': 311, 'F': 349, 'G':391, 'Bb':466}
store_folder = './media/'


def generate_note(frequency):
    n_samples = 44100
    sample_rate = 44100
    attenuation_factor = 0.996
    N = int(sample_rate / frequency)

    # Initialize the ring buffer.
    buffer = deque([random.random() - 0.5 for _ in range(N)])

    # Initialize samples buffer.
    samples = np.array([0] * n_samples, 'float32')
    for i in range(n_samples):
        samples[i] = buffer[0]
        avg = attenuation_factor * 0.5 * (buffer[0] + buffer[1])
        buffer.append(avg)
        buffer.popleft()

    # Convert samples to 16-bit values and then to a string.
    # The maximum value is 32767 for 16-bit.
    samples = np.array(samples * 32767, 'int16')
    return samples.tostring()


def write_wave(filename, data):
    # Open file.
    file = wave.open(''.join([store_folder, filename]), 'wb')
    # WAV file parameters.
    n_channels = 1
    sample_width = 2
    frame_rate = 44100
    n_frames = 44100

    # Set parameters.
    file.setparams((n_channels, sample_width, frame_rate, n_frames, 'NONE', 'noncompressed'))

    # Write data.
    file.writeframes(data)
    file.close()


class NotePlayer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()

        self.store_folder = './media/'
        self.notes = {}

    def compose_filepath(self, filename):
        return ''.join([self.store_folder, filename])

    # Add a note.
    def add(self, filename):
        self.notes[filename] = pygame.mixer.Sound(self.compose_filepath(filename))

    # Play a note.
    def play(self, filename):
        try:
            self.notes[filename].play()
        except FileNotFoundError:
            print(f'{filename} not found!')

    def play_random(self):
        idx = random.randint(0, len(self.notes)-1)
        note = list(self.notes.values())[idx]
        note.play()


def main():
    parser = argparse.ArgumentParser(description="Generating sounds with Karplus Strong Algorithm")

    # Add arguments.
    parser.add_argument('--replay', action='store_true', required=False)
    parser.add_argument('--play', action='store_true', required=False)
    args = parser.parse_args()

    # Create note player.
    note_player = NotePlayer()

    print('creating notes...')
    for name, frequency in pm_notes.items():
        filename = ''.join([name, '.wav'])
        if not os.path.exists(''.join([store_folder, filename])) or args.replay:
            data = generate_note(frequency)
            print(f'creating {filename} ...')
            write_wave(filename, data)
        else:
            print(f'{filename} already created, skipping...')

        # Add note to player.
        note_player.add(filename)

        # Play note if replay flag is set.
        if args.replay:
            note_player.play(filename)
            time.sleep(0.5)

    # Play a random tune.
    if args.play:
        while True:
            try:
                note_player.play_random()
                # Rest - 1 to 8 beats.
                rest = np.random.choice([1, 2, 4, 8], 1, p=[0.15, 0.7, 0.1, 0.05])
                time.sleep(0.25 * rest[0])
            except KeyboardInterrupt:
                exit()


if __name__ == '__main__':
    main()

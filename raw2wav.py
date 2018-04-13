#!/usr/bin/env python3
import os
import sys
import numpy as np
from scipy.io.wavfile import write

SAMPLE_RATE = 2000 # hz
RANGE = 4096 # volumn

def get_argv_params():

    if len(sys.argv) != 3:
        print("Usage: ./raw2wav.py input output.wav")
        raise Exception("Invalid input parameters")

    fin_path, fout_path = sys.argv[1:3]
    if not os.path.exists(fin_path):
        raise Exception("Input file not found")

    return fin_path, fout_path

def get_raw_data(fin_path):
    arr = []
    with open(fin_path) as fin:
        for line in fin:
            arr.append(int(line, 16))
    data = np.array(arr)
    # Normalization
    return (data - RANGE/2) / (RANGE/2)

def save_wav(data, fout_path):
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
    write(fout_path, SAMPLE_RATE, scaled)

if __name__ == "__main__":

    fin_path, fout_path = get_argv_params()
    data = get_raw_data(fin_path)
    save_wav(data, fout_path)

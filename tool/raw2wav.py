#!/usr/bin/env python3
import os
import sys
import numpy as np
import string
from scipy.io.wavfile import write

SAMPLE_RATE = 2000 # hz
RANGE = 4096 # volumn

def get_argv_params():

    if len(sys.argv) != 3:
        print("Usage: ./raw2wav.py input output.wav")
        sys.exit(-1)

    fin_path, fout_path = sys.argv[1:3]
    if not os.path.exists(fin_path):
        sys.exit(-1)

    return fin_path, fout_path

def get_raw_data(fin_path):
    arr = []
    count = 0
    with open(fin_path) as fin:
        for line in fin:
            line = line.strip()
            if len(line) != 4:
                count += 1
                continue
            try:
                arr.append(int(line, 16))
            except Exception:
                import pdb; pdb.set_trace()

    data = np.array(arr)
    print("Ignored line number is %d for %s" % (count, fin_path))
    # Normalization
    return (data - RANGE/2) / (RANGE/2)

def save_wav_from_file(fin_path, fout_path):
    data = get_raw_data(fin_path)
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
    write(fout_path, SAMPLE_RATE, scaled)

if __name__ == "__main__":

    fin_path, fout_path = get_argv_params()
    save_wav_from_file(fin_path, fout_path)

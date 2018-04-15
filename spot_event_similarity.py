#!/usr/bin/env python3
import os
import sys
import numpy as np
import itertools
import matplotlib.pyplot as plt
from config import Config as cfg
from preprocess import chop

def main():

    # Loads the input/output filepaths
    input_pattern, input_test, output_file = get_io_files()

    # Loads data into numpy objects
    pattern = load_data(input_pattern)[-cfg.WINDOW_SIZE:]   # trimmed
    test = load_data(input_test)
    test_segments = np.array(chop(test, cfg.WINDOW_SIZE, cfg.STEP_SIZE))

    ##
    similarity = get_similarity(pattern, test_segments)
    save_plot(similarity, output_file)

def get_io_files():

    if len(sys.argv[1:]) != 3:
        print("Usage: ./spot_event_similarity.py " +\
              "input_pattern input_test output_file")
        sys.exit(-1)

    input_pattern, input_test, output_file = sys.argv[1:]

    if not os.path.exists(input_pattern) or not os.path.exists(input_test):
        print("Input file not is invalid")
        sys.exit(-1)

    return input_pattern, input_test, output_file

def load_data(input_file):
    with open(input_file) as f:
        arr = [int(line.strip(), 16) for line in f]
    return np.array(arr)


def get_similarity(pattern, segments):
    return [-1 * np.linalg.norm(segment - pattern) for segment in segments]

def save_plot(arr, output_file):
    plt.clf()
    plt.plot(arr)
    plt.savefig(output_file)
    print("Figure saved to %s" % output_file)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import sys
import numpy as np
import itertools
import matplotlib.pyplot as plt

WINDOW_SIZE = 8000
STEP_SIZE = 50

def main():

    # Loads the input/output filepaths
    input_pattern, input_test, output_file = get_io_files()

    # Loads data into numpy objects
    pattern = load_data(input_pattern)[-WINDOW_SIZE:]   # trimmed
    test = load_data(input_test)
    test_segments = chop(test, WINDOW_SIZE, STEP_SIZE)

    ##
    distances = get_distances(pattern, test_segments)
    save_plot(distances, output_file)

def get_io_files():

    if len(sys.argv[1:]) != 3:
        print("Usage: ./spot_event.py input_pattern input_test output_file")
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

def chop(data, window_size, step_size):

    left = 0
    segments = []

    while True:
        right = left + window_size
        if right >= len(data):
            return np.array(segments)
        segments.append(data[left:right])
        left += step_size

def get_distances(pattern, segments):
    return [np.linalg.norm(segment - pattern) for segment in segments]

def save_plot(arr, output_filepath):
    plt.clf()
    plt.plot(arr)
    plt.savefig(output_filepath)
    print("Figure saved to %s" % output_filepath)

if __name__ == "__main__":
    main()

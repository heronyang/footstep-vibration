#!/usr/bin/env python3
import os
import itertools
import shutil
import numpy as np
import random
from tool.raw2wav import save_wav
from config import Config as cfg

DATA_ROOT = "./data/"
DATA_MERGE_ROOT = "./merged_data/"
WAVE_ROOT = "./wave/"
PLOT_ROOT = "./plot/"
TRAIN_ROOT = "./svm/train/"
TEST_ROOT = "./svm/test/"

SINGLE_TRUE_DATA = ["heron", "harvey"]
SINGLE_LONG_FALSE_DATA = ["long"]
TRAIN_TEST_RATIO = 3

def main():
    clear_dir([DATA_MERGE_ROOT, WAVE_ROOT, PLOT_ROOT, TRAIN_ROOT, TEST_ROOT])
    generate_merged_files(DATA_ROOT, DATA_MERGE_ROOT)
    generate_wave_files(DATA_MERGE_ROOT, WAVE_ROOT)
    generate_plots(DATA_MERGE_ROOT, PLOT_ROOT)
    generate_train_test_data(DATA_MERGE_ROOT, TRAIN_ROOT, TEST_ROOT)

def clear_dir(dir_list):
    for d in dir_list:
        if os.path.exists(d) and os.path.isdir(d):
            shutil.rmtree(d)
            print("Removed %s" % d)

def generate_merged_files(input_dir, output_dir):
    for subdir in os.listdir(input_dir):
        print("Found %s" % subdir)
        for index in itertools.count():
            input_subdir = input_dir + subdir + "/" + subdir + "-" \
                    + str(index + 1)
            output_file = "%s%s/%02d" % (output_dir, subdir, index + 1)
            if os.path.exists(input_subdir):
                merge_dir(input_subdir, output_file)
            else:
                print("Exit %s" % subdir)
                break

def merge_dir(input_dir, output_file):

    data = ""

    for index in itertools.count():
        input_file = "%s/data_%d" % (input_dir, index)
        if not os.path.exists(input_file):
            break
        with open(input_file) as fin:
            for line in fin:
                line = line.strip()
                if len(line) != 4:
                    continue
                data += (line + "\n")

    mkdir(os.path.dirname(output_file))
    with open(output_file, "w") as fout:
        fout.write(data)

    print("%s => %s merged" % (input_dir, output_file))

def generate_wave_files(input_dir, output_dir):
    for subdir in os.listdir(input_dir):
        for index in itertools.count():
            input_file = "%s%s/%02d" % (input_dir, subdir, index + 1)
            output_file = "%s%s/%02d.wav" % (output_dir, subdir, index + 1)
            if not os.path.exists(input_file):
                break
            mkdir(os.path.dirname(output_file))
            save_wav(input_file, output_file)
            print("%s => %s generated" % (input_file, output_file))

def generate_plots(input_dir, output_dir):
    import matplotlib.pyplot as plt
    for subdir in os.listdir(input_dir):
        for index in itertools.count():
            input_file = "%s%s/%02d" % (input_dir, subdir, index + 1)
            output_file = "%s%s/%02d.png" % (output_dir, subdir, index + 1)
            if not os.path.exists(input_file):
                break
            with open(input_file) as f:
                arr = [int(line.strip(), 16) for line in f]
            mkdir(os.path.dirname(output_file))
            plt.clf()
            plt.plot(arr)
            plt.savefig(output_file)
            print("%s => %s generated" % (input_file, output_file))

def generate_train_test_data(input_dir, train_root, test_root):

    # Reads data
    true_data, false_data = read_true_false_data(input_dir)
    
    # Shuffle
    random.shuffle(true_data)
    random.shuffle(false_data)

    # Writes into train/test data
    write_true_false_data(train_root, test_root, true_data, false_data)

def read_true_false_data(input_dir):

    true_data, false_data = [], []

    for subdir in os.listdir(input_dir):
        for index in itertools.count():

            # Reads the input file into an array
            input_file = "%s%s/%02d" % (input_dir, subdir, index + 1)
            if not os.path.exists(input_file):
                break
            with open(input_file) as f:
                arr = [int(line.strip(), 16) for line in f]

            # Generates X data with Y = 1
            if subdir in SINGLE_TRUE_DATA:
                if len(arr) < cfg.WINDOW_SIZE:
                    print("Ignore %s since it's smaller than the window size" %
                          input_file)
                    continue
                true_data.append(arr[-cfg.WINDOW_SIZE:])

            # Generates X data with Y = 0
            elif subdir in SINGLE_LONG_FALSE_DATA:
                false_data += chop(arr, cfg.WINDOW_SIZE, cfg.STEP_SIZE)

    return true_data, false_data

def write_true_false_data(train_root, test_root, true_data, false_data):

    true_data_splitter = int(len(true_data) * \
                             (TRAIN_TEST_RATIO / (TRAIN_TEST_RATIO + 1)))
    false_data_splitter = int(len(false_data) * \
                             (TRAIN_TEST_RATIO / (TRAIN_TEST_RATIO + 1)))

    # Writes train data
    write_data_list_to_file(true_data[:true_data_splitter], train_root + "1/")
    write_data_list_to_file(false_data[:false_data_splitter], train_root + "0/")

    # Writes test data
    write_data_list_to_file(true_data[true_data_splitter:], test_root + "1/")
    write_data_list_to_file(false_data[false_data_splitter:], test_root + "0/")

def write_data_list_to_file(data_list, output_dir):

    mkdir(output_dir)
    for i, data in enumerate(data_list):
        output_file = "%s%03d" % (output_dir, i + 1)
        with open(output_file, "w") as fout:
            fout.write("\n".join([str(d) for d in data]))
        print("%s saved" % output_file)

    np_file = output_dir + "metric.txt"
    np.savetxt(np_file, np.array(data_list), fmt="%d")
    print("%s saved" % np_file)

def chop(data, window_size, step_size):

    left = 0
    segments = []

    while True:
        right = left + window_size
        if right >= len(data):
            return segments
        segments.append(data[left:right])
        left += step_size

def mkdir(dir_path):
    os.makedirs(dir_path, exist_ok=True)

if __name__ == "__main__":
    main()

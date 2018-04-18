#!/usr/bin/env python3
import os
import itertools
import shutil
import numpy as np
import random
from scipy.io.wavfile import write
from config import Config as cfg

DATA_ROOT = "./raw_data/"
DATA_MERGE_ROOT = "./merged_data/"
WAVE_ROOT = "./wave/"
PLOT_ROOT = "./plot/"
TRAIN_ROOT = "./svm/train/"
TEST_ROOT = "./svm/test/"
PROCESSED_DATA_ROOT = "./data/"
DATA_WAVE_ROOT = "./data/wave/"
TMP_FILE = "/tmp/t"

SINGLE_TRUE_DATA = ["heron", "harvey"]
SINGLE_LONG_FALSE_DATA = ["uncontrol"]

def main():
    clear_dir([DATA_MERGE_ROOT, WAVE_ROOT, PLOT_ROOT, TRAIN_ROOT, TEST_ROOT,
               PROCESSED_DATA_ROOT])
    generate_merged_files(DATA_ROOT, DATA_MERGE_ROOT)
    generate_wave_files(DATA_MERGE_ROOT, WAVE_ROOT)
    generate_plots(DATA_MERGE_ROOT, PLOT_ROOT)
    generate_train_test_data(DATA_MERGE_ROOT, TRAIN_ROOT, TEST_ROOT)
    generate_processed_data(DATA_MERGE_ROOT, PROCESSED_DATA_ROOT)
    generate_data_wave_files(PROCESSED_DATA_ROOT, DATA_WAVE_ROOT)

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
            save_wav_from_file(input_file, output_file)
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

def generate_processed_data(input_dir, output_dir):

    true_data, false_data = read_true_false_data(input_dir)
    mkdir(output_dir)

    # Shuffle
    random.shuffle(true_data)
    random.shuffle(false_data)

    # Generates true data
    output_true_file = output_dir + "1"
    np.savetxt(output_true_file, np.array(true_data), fmt="%d")
    print("%s saved" % output_true_file)

    # Generates false data
    output_false_file = output_dir + "0"
    np.savetxt(output_false_file, np.array(false_data), fmt="%d")
    print("%s saved" % output_false_file)

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

    # Gets the splitter index
    true_data_splitter = int(len(true_data) * cfg.TRAIN_TEST_RATIO)
    false_data_splitter = int(len(false_data) * cfg.TRAIN_TEST_RATIO)

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

def generate_data_wave_files(input_dir, output_dir):

    events = np.loadtxt(input_dir + "1")
    unknowns = np.loadtxt(input_dir + "0")

    events_splitter = int(len(events) * cfg.TRAIN_TEST_RATIO)
    unknowns_splitter = int(len(unknowns) * cfg.TRAIN_TEST_RATIO)

    save_batch_wav(
        events[:events_splitter],
        "%strain/event/" % output_dir
    )
    save_batch_wav(
        unknowns[:unknowns_splitter],
        "%strain/unknown/" % output_dir
    )

    save_batch_wav(
        events[events_splitter:],
        "%stest/event/" % output_dir
    )
    save_batch_wav(
        unknowns[unknowns_splitter:],
        "%stest/unknown/" % output_dir
    )

def save_batch_wav(data_list, output_dir):

    index = 0
    for data in data_list:
        output_file = "%s%03d.wav" % (output_dir, index + 1)
        mkdir(os.path.dirname(output_file))
        save_wav(output_file, data)
        index += 1
        print("%s saved" % output_file)


def save_wav(output_file, data):
    data = (data - cfg.RANGE / 2) / (cfg.RANGE / 2)
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
    write(output_file, cfg.SAMPLE_RATE, scaled)

def save_wav_from_file(fin_path, fout_path):
    data = get_raw_data(fin_path)
    scaled = np.int16(data/np.max(np.abs(data)) * 32767)
    write(fout_path, cfg.SAMPLE_RATE, scaled)

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
    return (data - cfg.RANGE/2) / (cfg.RANGE/2)


def mkdir(dir_path):
    os.makedirs(dir_path, exist_ok=True)

if __name__ == "__main__":
    main()

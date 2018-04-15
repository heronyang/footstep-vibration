#!/usr/bin/env python3
import os
import itertools
from tool.raw2wav import save_wav

DATA_ROOT = "./data/"
DATA_MERGE_ROOT = "./merged_data/"
WAVE_ROOT = "./wave/"
PLOT_ROOT = "./plot/"

def generate_merged_files(input_dir, output_dir):
    for subdir in os.listdir(input_dir):
        print("Found %s" % subdir)
        for index in itertools.count():
            input_dir = input_dir + subdir + "/" + subdir + "-" + str(index + 1)
            output_filepath = "%s%s/%02d" % (output_dir, subdir, index + 1)
            if os.path.exists(input_dir):
                merge_dir(input_dir, output_filepath)
            else:
                break

def merge_dir(input_dir, output_filepath):

    data = ""

    for index in itertools.count():
        input_filepath = "%s/data_%d" % (input_dir, index)
        if not os.path.exists(input_filepath):
            break
        with open(input_filepath) as fin:
            for line in fin:
                line = line.strip()
                if len(line) != 4:
                    continue
                data += (line + "\n")

    mkdir(os.path.dirname(output_filepath))
    with open(output_filepath, "w") as fout:
        fout.write(data)

    print("%s => %s merged" % (input_dir, output_filepath))

def generate_wave_files(input_dir, output_dir):
    for subdir in os.listdir(input_dir):
        for index in itertools.count():
            input_filepath = "%s%s/%02d" % (input_dir, subdir, index + 1)
            output_filepath = "%s%s/%02d.wav" % (output_dir, subdir, index + 1)
            if not os.path.exists(input_filepath):
                break
            mkdir(os.path.dirname(output_filepath))
            save_wav(input_filepath, output_filepath)
            print("%s => %s generated" % (input_filepath, output_filepath))

def generate_plots(input_dir, output_dir):
    import matplotlib.pyplot as plt
    for subdir in os.listdir(input_dir):
        for index in itertools.count():
            input_filepath = "%s%s/%02d" % (input_dir, subdir, index + 1)
            output_filepath = "%s%s/%02d.png" % (output_dir, subdir, index + 1)
            if not os.path.exists(input_filepath):
                break
            with open(input_filepath) as f:
                arr = [int(line.strip(), 16) for line in f]
            mkdir(os.path.dirname(output_filepath))
            plt.clf()
            plt.plot(arr)
            plt.savefig(output_filepath)
            print("%s => %s generated" % (input_filepath, output_filepath))

def mkdir(dir_path):
    os.makedirs(dir_path, exist_ok=True)

if __name__ == "__main__":
    generate_merged_files(DATA_ROOT, DATA_MERGE_ROOT)
    generate_wave_files(DATA_MERGE_ROOT, WAVE_ROOT)
    generate_plots(DATA_MERGE_ROOT, PLOT_ROOT)

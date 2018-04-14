#!/usr/bin/env python3
import os
import itertools
from tool.raw2wav import save_wav

DATA_ROOT = "./data/"
DATA_MERGE_ROOT = "./merged_data/"
WAVE_ROOT = "./wave/"

def generate_merged_files(root_dir):
    for subdir in os.listdir(root_dir):
        print("Found %s" % subdir)
        for index in itertools.count():
            input_dir = root_dir + subdir + "/" + subdir + "-" + str(index + 1)
            output_filepath = "%s%s/%02d" % (DATA_MERGE_ROOT, subdir, index + 1)
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

def generate_wave_files(root_dir):
    for subdir in os.listdir(root_dir):
        for index in itertools.count():
            input_filepath = "%s%s/%02d" % (root_dir, subdir, index + 1)
            output_filepath = "%s%s/%02d.wav" % (WAVE_ROOT, subdir, index + 1)
            if not os.path.exists(input_filepath):
                break
            mkdir(os.path.dirname(output_filepath))
            save_wav(input_filepath, output_filepath)
            print("%s => %s generated" % (input_filepath, output_filepath))

def mkdir(dir_path):
    os.makedirs(dir_path, exist_ok=True)

if __name__ == "__main__":
    generate_merged_files(DATA_ROOT)
    generate_wave_files(DATA_MERGE_ROOT)

#!/usr/bin/env python3
import os
import itertools

DATA_ROOT = "./data/"
DATA_MERGE_ROOT = "./merged_data/"

def merge_all():
    for subdir in os.listdir(DATA_ROOT):
        print("Found %s" % subdir)
        for index in itertools.count():
            input_dir = DATA_ROOT + subdir + "/" + subdir + "-" + str(index + 1)
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

    print("%s => %s done" % (input_dir, output_filepath))

def mkdir(dir_path):
    os.makedirs(dir_path, exist_ok=True)

if __name__ == "__main__":
    merge_all()

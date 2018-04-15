#!/usr/bin/env python3

def get_io_files():

    if len(sys.argv[1:]) != 3:
        print("Usage: ./spot_event_svm.py train_data_folder test_data_folder")
        sys.exit(-1)

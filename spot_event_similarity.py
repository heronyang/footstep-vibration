#!/usr/bin/env python3
import numpy as np
from config import Config as cfg

INPUT_DIR = "./data/"

def main():

    # Load all processed true/false data
    x0 = np.loadtxt(INPUT_DIR + "0")
    x1 = np.loadtxt(INPUT_DIR + "1")

    # Split x1 into trainign and test set.
    splitter = int(len(x1) * cfg.TRAIN_TEST_RATIO)
    x1_train, x1_test = x1[:splitter], x1[splitter:]

    # Gets the test data using partial x1 and x0 (1:1)
    x_test = np.vstack((x1_test, x0[:len(x1_test)]))
    y_test = np.array([1] * len(x1_test) + [0] * len(x1_test))

    # Predict
    for threshold in range(20000, 60000, 500):
        y_predict = predict(x_test, y_test, x1_train, threshold)
        correctness = (y_predict == y_test).mean()
        print("Threshold %d, correctness %f" % (threshold, correctness))

def predict(x_test, y_test, x1_train, threshold):

    if x_test.shape[0] != y_test.shape[0]:
        raise Exception("Size mismatched")
    
    y_predict = []
    for i in range(len(x_test)):
        xi = x_test[i]
        yi = y_test[i]

        simiarity = np.array([get_similarity(i, xi) for i in x1_train]).mean()
        y_predict_i = 1 if simiarity > threshold else 0
        y_predict.append(y_predict_i)
    return np.array(y_predict)

def get_similarity(pattern, segment):
    return np.abs(np.linalg.norm(pattern - segment))

if __name__ == "__main__":
    main()

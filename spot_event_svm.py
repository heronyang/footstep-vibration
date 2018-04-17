#!/usr/bin/env python3
import numpy as np
from sklearn import svm

TRAIN_ROOT = "./svm/train/"
TEST_ROOT = "./svm/test/"

def get_input():

    # Train
    X_0 = np.loadtxt(TRAIN_ROOT + "0/metric.txt")
    X_1 = np.loadtxt(TRAIN_ROOT + "1/metric.txt")
    X = np.vstack((X_0, X_1))
    y = np.array([0] * len(X_0) + [1] * len(X_1))

    # Test
    X_test_0 = np.loadtxt(TEST_ROOT + "0/metric.txt")
    X_test_1 = np.loadtxt(TEST_ROOT + "1/metric.txt")
    X_test = np.vstack((X_test_0, X_test_1))
    y_test = np.array([0] * len(X_test_0) + [1] * len(X_test_1))

    return X, y, X_test, y_test

def main():

    X, y, X_test, y_test = get_input()
    model = svm.SVC(kernel="linear", C=1, gamma=1)

    # Train
    model.fit(X, y)
    y_predict = model.predict(X)
    print("[Train] Correctness: %f" % ((y == y_predict).sum() / len(y)))

    # Predict
    y_test_predict = model.predict(X_test)
    print("predict", y_test_predict)
    print("truth", y_test)
    print("[Test] Correctness: %f" %
          ((y_test == y_test_predict).sum() / len(y_test)))

if __name__ == "__main__":
    main()

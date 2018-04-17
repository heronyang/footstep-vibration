# Vibration + Footstep

## Preprocessing

    $ ./preprocess.py

## Spot event using Similarity

    $ ./spot_event_similarity.py

## Spot event using SVM

    $ ./spot_event_svm.py

## Spot event using Keyword Spotting

- Install [anaconda](https://www.anaconda.com/download/#macos)
- Install [CUDA](https://developer.nvidia.com/cuda-downloads?target_os=MacOSX&target_arch=x86_64&target_version=1013&target_type=dmglocal)
    - `export CMAKE_PREFIX_PATH=/Users/heron/anaconda3`
    - `conda install numpy pyyaml mkl mkl-include setuptools cmake cffi typing`

    $ brew install portaudio
    $ pip install torch torchvision
    $ pip install -r requirements.txt
    $ git clone https://github.com/castorini/honk.git
    $ cd honk
    $ ./fetch_data.sh
    $ vim config.json # turn off cuda
    $ unzip models.zip && mv honk-models-master model

[update]

    export PYTHON_BIN_PATH=/Users/heron/anaconda3/bin/python

## Result

Correctness: 0.865031 (dummy small set of data)

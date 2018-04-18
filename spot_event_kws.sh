# Install
export PYTHON_BIN_PATH=/Users/heron/anaconda3/bin/python
pip install tf-nightly # https://github.com/tensorflow/tensorflow/issues/12807
git clone https://github.com/tensorflow/tensorflow.git
bazel run tensorflow/examples/speech_commands:train -- --data_dir=/home/ubuntu/footstep-vibration/data/wave/train/ --wanted_words=event --sample_rate=2000 --how_many_train_steps=400

# Run monitor
tensorboard --logdir /tmp/retrain_logs

# Freeze
python tensorflow/examples/speech_commands/freeze.py --start_checkpoint=/tmp/speech_commands_train/conv.ckpt-900 --sample_rate=2000 --output_file=/tmp/my_frozen_graph.pb --wanted_words=event

# Predict
python tensorflow/examples/speech_commands/label_wav.py --graph=/tmp/my_frozen_graph.pb --labels=/tmp/speech_commands_train/conv_labels.txt --wav=/home/ubuntu/footstep-vibration/data/wave/test/unknown/001.wav

# Result Example
    # 2018-04-18 07:55:50.794095: E tensorflow/core/kernels/mfcc_mel_filterbank.cc:179] Input too short to compute filterbank
    # event (score = 0.80537)
    # _silence_ (score = 0.18075)
    # _unknown_ (score = 0.01388)

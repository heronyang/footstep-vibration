git clone https://github.com/mindorii/kws.git

wget http://www.mega-nerd.com/SRC/libsamplerate-0.1.9.tar.gz
tar -xvzf libsamplerate-0.1.9.tar.gz
./configure
make
sudo make install

remove tensorflow-gpu==1.4 in requirements.txt

add -I/usr/include/ in Makefile decoder/ and utils/

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
######

sudo apt-get install python2.7-dev
sudo apt-get install python-pip python-dev
pip install --upgrade  https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.4.1-cp27-none-linux_x86_64.whl
apt-get install libpulse0:i386

sudo apt-get install libopenblas-dev

sudo apt-get install libboost-all-dev
sudo apt-get update
sudo apt-get install libsamplerate-dev


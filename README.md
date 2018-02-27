# Darknet object recognition

How to train Darknet to detect custom object on Ubuntu 16.04 LTS, GPU Nvidia 1080 Ti and OpenCV supported.

## Prerequisites: CUDA, cuDNN, OpenCV

[Installing OpenCV for C and Python](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)

[Installing CUDA and cuDNN] (https://yangcha.github.io/GTX-1080/)

## Cloning the project

You can clone it direcly from the Git repository

```
git clone https://github.com/pjreddie/darknet.git
cd darknet
```

Open Makefile and change some lines:

```
GPU=1
CUDNN=1
OPENCV=1
```

Run make

```
make
```

Download the pre-trained weight

```
wget https://pjreddie.com/media/files/yolo.weights
```

Test to see if it work.

```
./darknet detect cfg/yolo.cfg yolo.weights data/dog.jpg
```


# Darknet object recognition

How to train Darknet to detect custom object on Ubuntu 16.04 LTS, GPU Nvidia 1080 Ti and OpenCV supported.

## Prerequisites: CUDA, cuDNN, OpenCV

[Installing OpenCV for C and Python](https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/)

[Installing CUDA and cuDNN](https://yangcha.github.io/GTX-1080/)

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

## Reparing the data

We have to create `.txt`-file for each `.jpg`-image-file - in the same directory and with the same name, but with `.txt`-extension, and put to file: object number and object coordinates on this image, for each object in new line: `<object-class> <x> <y> <width> <height>`

  Where: 
  * `<object-class>` - integer number of object from `0` to `(classes-1)`
  * `<x> <y> <width> <height>` - float values relative to width and height of image, it can be equal from 0.0 to 1.0 
  * for example: `<x> = <absolute_x> / <image_width>` or `<height> = <absolute_height> / <image_height>`
  * atention: `<x> <y>` - are center of rectangle (are not top-left corner)

  For example for `img1.jpg` you should create `img1.txt` containing:

  ```
  1 0.716797 0.395833 0.216406 0.147222
  0 0.687109 0.379167 0.255469 0.158333
  1 0.420312 0.395833 0.140625 0.166667
  ```

Let's the [BBox Label Tool](https://github.com/puzzledqs/BBox-Label-Tool). Change line 128 in main.py to your data's directory.

```
128            s = r'D:\workspace\python\labelGUI'
129  ##        if not os.path.isdir(s):
130  ##            tkMessageBox.showerror("Error!", message = "The specified dir doesn't exist!")
131  ##            return
```

The current tool requires that the images to be labeled reside in /Images/001, /Images/002, etc... The coordinate of the bounding box will be in /Labels/001, /Labels/002, etc... This give the coordinate of the bounding box and is still not the right format.

Then write a script to transform these number from the output to the right format. I'll upload it here soon.

## Start training

1. Create file `yolo-obj.cfg` with the same content as in `yolo-voc.2.0.cfg` (or copy `yolo-voc.2.0.cfg` to `yolo-obj.cfg)` and:

  * change line batch to [`batch=64`](https://github.com/AlexeyAB/darknet/blob/master/build/darknet/x64/yolo-voc.2.0.cfg#L2)
  * change line subdivisions to [`subdivisions=8`](https://github.com/AlexeyAB/darknet/blob/master/build/darknet/x64/yolo-voc.2.0.cfg#L3)
  * change line `classes=20` to your number of objects
  * change line #237 from [`filters=125`](https://github.com/AlexeyAB/darknet/blob/master/cfg/yolo-voc.2.0.cfg#L224) to: filters=(classes + 5)x5, so if `classes=2` then should be `filters=35`. Or if you use `classes=1` then write `filters=30`, **do not write in the cfg-file: filters=(classes + 5)x5**.
  
  (Generally `filters` depends on the `classes`, `num` and `coords`, i.e. equal to `(classes + coords + 1)*num`, where `num` is number of anchors)

  So for example, for 2 objects, your file `yolo-obj.cfg` should differ from `yolo-voc.2.0.cfg` in such lines:

  ```
  [convolutional]
  filters=35

  [region]
  classes=2
  ```

2. Create file `obj.names` in the directory `darknet/data`, with objects names - each in new line

3. Create file `obj.data` in the directory `darknet/data`, containing (where **classes = number of objects**):

  ```
  classes= 2
  train  = data/train.txt
  valid  = data/test.txt
  names = data/obj.names
  backup = backup/
  ```

4. Put image-files (.jpg) of your objects in the directory `darknet/data/obj/`


6. Create file `train.txt` in directory `darknet/data/`, with filenames of your images, each filename in new line, with path relative to `darknet.exe`, for example containing:

  ```
  data/obj/img1.jpg
  data/obj/img2.jpg
  data/obj/img3.jpg
  ```

7. Download pre-trained weights for the convolutional layers (76 MB): http://pjreddie.com/media/files/darknet19_448.conv.23 and put to the directory `darknet/`

8. Start training by typing in the terminal: 

`./darknet detector train cfg/obj.data cfg/yolo-obj.cfg darknet19_448.conv.23`

9. After training is complete - get result `yolo-obj_final.weights` from path `darknet/backup/`

## Testing the results

Run

```
./darknet detect cfg/obj.data cfg/yolo-obj.cfg backup/yolo-obj.backup
```

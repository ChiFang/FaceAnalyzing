# FaceAnalyzing
Face analyzing by caffe for gender and age predict

I rewrite it just for fun. The network and algorithm is not SOTA anymore...

The DNN on OpenCV now is incredible. This version maybe friendy for beginner of deep learning^^

## Introduction

This repository contains a pyCaffe-based implementation of face analyzing such as age, gender and emotion etc...

You can read the paper in following link:

Age & Gender
http://www.openu.ac.il/home/hassner/projects/cnn_agegender/

Emotion
http://www.openu.ac.il/home/hassner/projects/cnn_emotions/

Face detect
https://github.com/opencv/opencv/tree/master/samples/dnn/face_detector


the model above are all available in caffe model zoo or OpenCV git

according my test, only gender predict is reliable... HaHa


## Requirements

 - Python >= 3.0
 - OpenCV

## example usage.

```
python FaceAnalyzing.py -i <input_image>
```

if you do not input image name it will use default image for demo.
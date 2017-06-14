# FaceAnalyzing
Face analyzing by caffe for gender and age predict

## Introduction

This repository contains a pyCaffe-based implementation of face analyzing such as age, gender etc...

You can read the paper in following link:

http://www.openu.ac.il/home/hassner/projects/cnn_agegender/


## Requirements

 - Python >= 2.7
 - CUDA >= 6.5 (highly recommended)
 - Caffe

CUDA will enable GPU-based computation in Caffe.

## example usage.

```
python GenderAge_Predict.py -i <input_image>
```

if you do not input image name it will use default image for demo.
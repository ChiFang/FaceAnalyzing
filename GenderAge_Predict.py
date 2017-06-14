
# example code  

print ("Start caffe server example...")
import os
import numpy as np
#import FileDialog
import matplotlib.pyplot as plt
import argparse

import PIL
from PIL import Image, ImageDraw, ImageFont

import sys
import time

print ("import CaffeFunc...")
import CaffeFunc as CF
print ("import CaffeFunc done")

print ("import caffe...")
import caffe
print ("import caffe done")

########## init setting for caffe stuff ##########
print ("init setting for caffe stuff")

# path
InputImg = 'Input_8.png'
Gender_Age_model_root = './model/GenderAge/'
age_listFile = 'AgeList.txt'
gender_listFile = 'GenderList.txt'
mean_filename=  Gender_Age_model_root + 'mean.binaryproto'
age_net_pretrained= Gender_Age_model_root + 'age_net.caffemodel'
age_net_model_file= Gender_Age_model_root + 'deploy_age.prototxt'
gender_net_pretrained= Gender_Age_model_root + 'gender_net.caffemodel'
gender_net_model_file= Gender_Age_model_root + 'deploy_gender.prototxt'

#Labels
age_list = CF.LoadLabel(age_listFile)
gender_list = CF.LoadLabel(gender_listFile)

#Loading the mean image
mean = CF.LoadMean(mean_filename)

#Loading the age network
age_net = caffe.Classifier(age_net_model_file, age_net_pretrained, channel_swap=(2,1,0),raw_scale=255,image_dims=(256, 256))

#Loading the gender network
gender_net = caffe.Classifier(gender_net_model_file, gender_net_pretrained, channel_swap=(2,1,0),raw_scale=255,image_dims=(256, 256))


########## load image and start predict ##########

# argparse
parser = argparse.ArgumentParser(description="Gender and age predict.",
                                 usage="GenderAge_Predict.py -i <input_image> ")
parser.add_argument("-i", "--input-image", type=str, required=False, help="input image")

args = parser.parse_args()

print (args)

if(args.input_image == None):
    print("None input image name, use default image!!!")
    args.input_image = InputImg

print (args.input_image)

print ("load image and start predict")
input_image = caffe.io.load_image(InputImg)


tStart = time.time()
#Age prediction
Age_Index = CF.GetPredictMaxIndex(input_image, age_net)


#Gender prediction
Gender_Index = CF.GetPredictMaxIndex(input_image, gender_net)
tEnd = time.time()

print ('\n\n-------------result-------------')	
print ("It cost %f sec for Age and Gender prediction~~~" % (tEnd - tStart))
print ('predicted age:', age_list[Age_Index])
print ('predicted gender:', gender_list[Gender_Index])
print ('-------------result-------------\n\n')	
########## load image and start predict ##########



########## log output ##########
img = Image.open(InputImg)
draw = ImageDraw.Draw(img)

ttFont = ImageFont.truetype('C:/windows/fonts/Arial.ttf', size=15) # in wondows
#font_path=os.environ.get("FONT_PATH", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf") # in linux
#ttFont = ImageFont.truetype(font_path, 20) # in linux

draw.text((0, 0),"Gender: " + gender_list[Gender_Index],(255,0,0),font=ttFont)
draw.text((0, 20),"Age: " + age_list[Age_Index],(255,0,0),font=ttFont)
img.save("result" + ".png")
########## log output ##########


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

def showimage(im):
    if im.ndim == 3:
        im = im[:, :, ::-1]
    plt.set_cmap('jet')
    plt.imshow(im,vmin=0, vmax=0.2)
    

def vis_square(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()
    
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    
    showimage(data)

########## init setting for caffe stuff ##########
print ("init setting for caffe stuff")

# path
InputImg = './test_img/happy.jpg'
model_root = './model/'
age_listFile = 'AgeList.txt'
gender_listFile = 'GenderList.txt'
emotion_listFile = 'EmotionList.txt'
mean_filename=  model_root + 'GenderAge/' +'mean.binaryproto'
age_net_pretrained= model_root + 'GenderAge/' + 'age_net.caffemodel'
age_net_model_file= model_root + 'GenderAge/' + 'deploy_age.prototxt'
gender_net_pretrained= model_root + 'GenderAge/' + 'gender_net.caffemodel'
gender_net_model_file= model_root + 'GenderAge/' + 'deploy_gender.prototxt'
emotion_net_pretrained= model_root + 'Emotion/' + 'EmotiW_VGG_S.caffemodel'
emotion_net_model_file= model_root + 'Emotion/' + 'deploy.prototxt'

#Labels
age_list = CF.LoadLabel(age_listFile)
gender_list = CF.LoadLabel(gender_listFile)
emotion_list = CF.LoadLabel(emotion_listFile)

#Loading the mean image
mean = CF.LoadMean(mean_filename)

#Loading the age network
age_net = caffe.Classifier(age_net_model_file, age_net_pretrained, channel_swap=(2,1,0),raw_scale=255,image_dims=(256, 256))

#Loading the gender network
gender_net = caffe.Classifier(gender_net_model_file, gender_net_pretrained, channel_swap=(2,1,0),raw_scale=255,image_dims=(256, 256))

#Loading the emotion network
emotion_net = caffe.Classifier(emotion_net_model_file, emotion_net_pretrained, channel_swap=(2,1,0), raw_scale=255, image_dims=(256, 256))


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
else:
    InputImg = args.input_image

print (args.input_image)

print ("load image and start predict")
input_image = caffe.io.load_image(InputImg)


tStart = time.time()
#Age prediction
Age_Index = CF.GetPredictMaxIndex(input_image, age_net)

#Gender prediction
Gender_Index = CF.GetPredictMaxIndex(input_image, gender_net)

#Emotion prediction
Emotion_Index = CF.GetPredictMaxIndex(input_image, emotion_net)
tEnd = time.time()

print ('\n\n-------------result-------------')	
print ("It cost %f sec for Age and Gender prediction~~~" % (tEnd - tStart))
print ('predicted age:', age_list[Age_Index])
print ('predicted gender:', gender_list[Gender_Index])
print ('predicted emotion:', emotion_list[Emotion_Index])
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
draw.text((0, 40),"Emotion: " + emotion_list[Emotion_Index],(255,0,0),font=ttFont)
img.save("result" + ".png")
########## log output ##########

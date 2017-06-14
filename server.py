
# server  

print ("Start caffe server example...")
import os
import numpy as np
import FileDialog
import matplotlib.pyplot as plt

import PIL
from PIL import Image, ImageDraw, ImageFont

import sys
import time

print ("import CaffeFunc...")
import CaffeFunc as CF
print ("import CaffeFunc done")

print ("import socket function...")
import SocketFunc as SF
print ("import socket function done")

print ("import caffe...")
import caffe
print ("import caffe done")

########## init setting for caffe stuff ##########
print ("init setting for caffe stuff")

# path
InputImg = 'tmp.png'
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
age_net = caffe.Classifier(age_net_model_file, age_net_pretrained, mean=mean, channel_swap=(2,1,0),raw_scale=255,image_dims=(256, 256))

#Loading the gender network
gender_net = caffe.Classifier(gender_net_model_file, gender_net_pretrained, mean=mean, channel_swap=(2,1,0),raw_scale=255,image_dims=(256, 256))

print '--------------------'
########## init setting for caffe stuff ##########


########## init socket setting ##########
print '--------------------'
print ("init socket setting...")
ip,port,DataSize,repeat = SF.LoadCfg("ClientCFG.ini")
print ("server IP: " + ip)
print ("port: " + str(port))
print ("image size: " + str(DataSize))
print ("repeat: " + str(repeat))
print '--------------------'
########## init socket setting ##########

sock = SF.SetServer(ip, port, 5)
print 'waiting for a connection...'
connection, client_address = sock.accept()
print 'got connected from',client_address

while True:
	print '--------------------'
	connection.send('Server: Ready to receive data...')  
	print ("receive data.......")
	
	########## image transfer by socket ##########
	print ("image transfer by socket...")
	data_size = SF.GetDataSize(connection)
	print (data_size)
	if data_size > 0:
		data = ""
		data,enable = SF.ReceiveData(connection, data_size)

		print ("Receive data size: " + str(len(data)) + " (byte)")

		if enable==False:	# data size missmatch
			print ("data size missmatch, Quit this program~~~")
			connection.send("data size missmatch !")
			if repeat:
				print ("repeat~~~")
			else:		# stop server
				break
		else:	# data size match >> start calculating
			print 'writting file...'			
			SF.SaveDataBinary(InputImg)
			print 'writting file finish...'
			
			########## load image and start predict ##########
			print ("load image and start predict")
			input_image = caffe.io.load_image(InputImg)

			#Age prediction
			Age_Index = CF.GetPredictMaxIndex(input_image, age_net)
			print ('predicted age:', age_list[Age_Index])
			
			#Gender prediction
			tStart = time.time()
			Gender_Index = CF.GetPredictMaxIndex(input_image, gender_net)
			tEnd = time.time()	
			print ("It cost %f sec for gender prediction~~~" % (tEnd - tStart))
			print ('predicted gender:', gender_list[Gender_Index])
			########## load image and start predict ##########
			
			########## Tell client result, log output ##########
			connection.send("Gender: " + gender_list[Gender_Index] + " " + "Age: " + age_list[Age_Index])
			img = Image.open(InputImg)
			draw = ImageDraw.Draw(img)

			ttFont = ImageFont.truetype('C:/windows/fonts/Arial.ttf', size=15) # in wondows
			#font_path=os.environ.get("FONT_PATH", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf") # in linux
			#ttFont = ImageFont.truetype(font_path, 20) # in linux

			draw.text((0, 0),"Gender: " + gender_list[Gender_Index],(255,0,0),font=ttFont)
			draw.text((0, 20),"Age: " + age_list[Age_Index],(255,0,0),font=ttFont)
			img.save("out" + ".png")
			########## Tell client result, log output ##########
	else:
		print ("can not get image size, break the link")
		connection.send("can not get image size, break the link !")
		break
			
########## close socket ##########
connection.close()  
sock.close()
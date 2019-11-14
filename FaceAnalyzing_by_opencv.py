
# example code  

print ("Start caffe server example...")
import os
import numpy as np
import argparse
import cv2
import time
import sys
import time


def LoadLabel(filename):
	List = []
	file = open(filename, 'r')
	while True :
		line = file.readline()
		line = line.rstrip('\r\n')
		
		if line=='':
			break
		else:
			List.append(line)
	file.close()
	return List
    

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False, default='./test_img/test_sample.png', help="path to input image")


    # path
    InputImg = './test_img/test_sample.png'
    model_root = './model/'
    age_listFile = 'AgeList.txt'
    gender_listFile = 'GenderList.txt'
    emotion_listFile = 'EmotionList.txt'
    age_net_pretrained= model_root + 'GenderAge/' + 'age_net.caffemodel'
    age_net_model_file= model_root + 'GenderAge/' + 'deploy_age.prototxt'
    gender_net_pretrained= model_root + 'GenderAge/' + 'gender_net.caffemodel'
    gender_net_model_file= model_root + 'GenderAge/' + 'deploy_gender.prototxt'
    emotion_net_pretrained= model_root + 'Emotion/' + 'EmotiW_VGG_S.caffemodel'
    emotion_net_model_file= model_root + 'Emotion/' + 'deploy.prototxt'
    detect_net_pretrained= model_root + 'face_detect/' + 'res10_300x300_ssd_iter_140000.caffemodel'
    detect_net_model_file= model_root + 'face_detect/' + 'deploy.prototxt'
    
    confidence_th = 0.5
    model_sise_classify = (256, 256)
    model_sise_detect = (256, 256)

    #Labels
    age_list        = LoadLabel(age_listFile)
    gender_list     = LoadLabel(gender_listFile)
    emotion_list    = LoadLabel(emotion_listFile)

    age_net     = cv2.dnn.readNetFromCaffe(age_net_model_file, age_net_pretrained)          #Loading the age network
    gender_net  = cv2.dnn.readNetFromCaffe(gender_net_model_file, gender_net_pretrained)    #Loading the gender network
    # emotion_net = cv2.dnn.readNetFromCaffe(emotion_net_model_file, emotion_net_pretrained)  #Loading the emotion network
    detect_net  = cv2.dnn.readNetFromCaffe(detect_net_model_file, detect_net_pretrained)    #Loading the face detect network


    ########## load image and start predict ##########
    print ("load image and start predict")
    image = cv2.imread(InputImg)
    image_draw = cv2.imread(InputImg)
    (h, w) = image.shape[:2]
    blob_detect = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    
    print("[INFO] computing object detections...")
    detect_net.setInput(blob_detect)
    
    start_time = time.time()
    detections = detect_net.forward()
    duration = time.time() - start_time
    print("detect Time: ", round(duration*1000, 2), " ms")
    
    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the prediction
        confidence = detections[0, 0, i, 2]
     
        # filter out weak detections by ensuring the `confidence` is greater than the minimum confidence
        if confidence > confidence_th:
            # compute the (x, y)-coordinates of the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            roiImg = image[startY:endY,startX:endX]
            cv2.imwrite("roiImg.png", roiImg)
            
            blob_gender = cv2.dnn.blobFromImage(cv2.resize(roiImg, model_sise_classify), 1.0, model_sise_classify)
            gender_net.setInput(blob_gender)
            result_gender = gender_net.forward()
            
            blob_age = cv2.dnn.blobFromImage(cv2.resize(roiImg, model_sise_classify), 1.0, model_sise_classify)
            age_net.setInput(blob_age)
            result_age = age_net.forward()
            
            '''
            blob_emotion = cv2.dnn.blobFromImage(cv2.resize(roiImg, model_sise_classify), 1.0, model_sise_classify)
            emotion_net.setInput(blob_emotion)
            result_emotion = emotion_net.forward()
            '''
            
            Gender_Index    = result_gender.argmax()
            Age_Index       = result_age.argmax()
            # Emotion_Index   = result_emotion.argmax()
            
            print ('\n\n-------------result-------------')	
            # print ("It cost %f sec for Age and Gender prediction~~~" % (tEnd - tStart))
            print ('predicted age:', age_list[Age_Index])
            print ('predicted gender:', gender_list[Gender_Index])
            # print ('predicted emotion:', emotion_list[Emotion_Index])
            print ('-------------result-------------\n\n')	
            
            # draw the bounding box of the face along with the associated probability
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(image_draw, (startX, startY), (endX, endY), (0, 0, 255), 2)
            cv2.putText(image_draw, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            cv2.putText(image_draw, age_list[Age_Index], (startX, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
            cv2.putText(image_draw, gender_list[Gender_Index], (startX, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
                
    cv2.imwrite("cv_facedetect.png", image_draw)


if __name__ == '__main__':
    main()

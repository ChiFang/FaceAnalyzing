
print ("import caffe...")
import caffe
print ("import caffe done")

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


def LoadMean(filename):
	proto_data = open(filename, "rb").read()
	a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
	mean  = caffe.io.blobproto_to_array(a)[0]
	return mean
	
def GetPredictMaxIndex(input, Net):
	prediction = Net.predict([input],oversample=False)
	Index = prediction[0].argmax()
	return Index
	
if __name__ == '__main__':
	print ("test...")
	########## init setting for caffe stuff ##########
	print ("init setting for caffe stuff...")
	
	# path
	InputImg = 'tmp.png'
	Gender_Age_model_root = './model/GenderAge/'
	age_listFile = 'AgeList.txt'
	gender_listFile = 'GenderList.txt'
	
	#Labels
	age_list = LoadLabel(age_listFile)
	print (age_list)
	gender_list = LoadLabel(gender_listFile)
	print (gender_list)

	#Loading the mean image
	mean_filename=  Gender_Age_model_root + 'mean.binaryproto'
	mean = LoadMean(mean_filename)

	#Loading the age network
	age_net_pretrained= Gender_Age_model_root + 'age_net.caffemodel'
	age_net_model_file= Gender_Age_model_root + 'deploy_age.prototxt'
	age_net = ca.caffe.Classifier(age_net_model_file, age_net_pretrained, mean=mean, channel_swap=(2,1,0),raw_scale=255,image_dims=(256, 256))

	#Loading the gender network
	gender_net_pretrained= Gender_Age_model_root + 'gender_net.caffemodel'
	gender_net_model_file= Gender_Age_model_root + 'deploy_gender.prototxt'
	gender_net = ca.caffe.Classifier(gender_net_model_file, gender_net_pretrained, mean=mean, channel_swap=(2,1,0),raw_scale=255,image_dims=(256, 256))

	print ('--------------------')
	########## init setting for caffe stuff ##########
	
	########## load image and start predict ##########
	print ("load image and start predict")
	input_image = ca.caffe.io.load_image(InputImg)

	#Age prediction
	Age_Index = GetPredictMaxIndex(input_image, age_net)
	print ('predicted age:', age_list[Age_Index])
	
	#Gender prediction
	tStart = time.time()
	Gender_Index = GetPredictMaxIndex(input_image, gender_net)
	tEnd = time.time()
	print ('predicted gender:', gender_list[Gender_Index])
	print ("It cost %f sec for gender prediction~~~" % (tEnd - tStart))
	########## load image and start predict ##########

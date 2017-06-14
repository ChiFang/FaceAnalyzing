# socket function by ncre
 
import sys
import socket  
import ConfigParser # for read config
import time

def LoadCfg(name):
	print (name)
	Config = ConfigParser.ConfigParser()
	Config.read(name)

	# list all sections
	Config.sections()

	# get as string
	ip = Config.get('socket', 'server_IP')

	# get as number
	port = Config.getint('socket', 'port')

	# get as number
	DataSize = Config.getint('data', 'image_size')

	# get as boolean
	repeat = Config.getboolean('mode', 'repeat')

	return (ip, port, DataSize, repeat)

def ReceiveData(connection, size):
	cnt = 0
	data = ""
	while 1:
		buff = connection.recv(DataSize)
		cnt +=len(buff)
		data += buff
		
		print ("buffer size: " + str(len(buff)) + " (byte)")
		print ("total size: " + str(cnt) + " (byte)")
		
		if cnt > data_size:
			print ("too much data")
			enable = False
			break
		if cnt == data_size:
			print ("Receive Data done")
			enable = True
			break
			
	return (data, enable)
	
def ReceiveData_TimeLimit(connection, size, sec):
	cnt = 0
	data = ""
	tStart = time.time()
	while 1:
		
		buff = connection.recv(DataSize)
		cnt +=len(buff)
		data += buff
		#print ("buffer size: " + str(len(buff)) + " (byte)")
		
		tTimeCost = time.time() - tStart
		if cnt > data_size:
			print ("too much data")
			enable = False
			break
		if cnt == data_size:
			print ("Receive Data done")
			enable = True
			break
		if tTimeCost > sec:
			print ("timeout !")
			enable = False
			break
			
			
	return (data, enable)

def SaveDataBinary(name):
	file_out = open(name, 'wb')
	file_out.write(data)
	file_out.close()

def SetServer(ip, port, listenNum):
	address = (ip, port)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # sock = socket.socket()  
	sock.bind(address)  
	sock.listen(listenNum)
	return sock

def SetClient(ip, port):
	address = (ip, port)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # sock = socket.socket()  
	sock.connect(address) 
	return sock

def GetDataSize(connection):
	string = 'size:'
	DataSize = 0
	buff = connection.recv(512)
	print (buff)
	index = buff.find(string)

	if index < 0: # match fail
		print ("Get DataSize fail !")
		DataSize = -1
	else:
		try:
			DataSize = int(buff.strip(string))
		except:
			print ("Data size is not number !")
			DataSize = -1
	
	connection.send(buff) # repeat same msg to client or server
	return DataSize
		
	
	
if __name__ == '__main__':
########## init socket setting ##########
	print ('--------------------')
	print ("init socket setting...")
	ip,port,DataSize,repeat = LoadCfg("ClientCFG.ini")
	print ("server IP: " + ip)
	print ("port: " + str(port))
	print ("image size: " + str(DataSize))
	print ("repeat: " + str(repeat))
	print ('--------------------')
########## init socket setting ##########


########## image transfer by socket ##########
	print ("image transfer by socket...")
	sock = SetServer(ip, port, 5)
	print ('waiting for a connection...')
	connection, client_address = sock.accept()
	print ('got connected from',client_address)
	connection.send('Server: Ready to receive data...')  
	print ("receive data.......")

	data_size = GetDataSize(connection)

	if data_size > 0:
		data = ""
		data,enable = ReceiveData(connection, data_size)

		print ("Receive data size: " + str(len(data)) + " (byte)")

		if enable==False:	# data size missmatch
			print ("data size missmatch, Quit this program~~~")
			connection.send("data size missmatch !")
			connection.close()  
			sock.close()
		else:	# data size match >> start calculating
			print ('writting file...')			
			SaveDataBinary('tmp_1.png')
			print ('writting file finish...')

########## image transfer by socket ##########

	connection.send('Server: end of calculating')
	sock.close()
	


# client  
  
import socket  
  
print ("import socket function...")
import SocketFunc as SF
print ("import socket function done")

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

sock = SF.SetClient(ip, port)
print '--------------------'

data = sock.recv(512)  
print data  
  
file = open('Input_8.png', 'rb')
content = file.read()
file.close()

print 'content size is ', len(content)  
  
#sock.send(content)
sock.send("size:"+str(len(content)))

print 'content transfer is done.'

print ("calculating....")
data = sock.recv(512)  
print 'the result is: ',data

print '--------------------'

data = sock.recv(512)  
print data

content = "stop"
print 'content size is ', len(content) 

sock.send(content)

print 'content transfer is done.'

print ("calculating....")
data = sock.recv(512)  
print 'the result is: ',data

print '--------------------'
  
sock.close()

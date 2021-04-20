import socket
# from time import ctime
# import os
# import Cytron27Aug2019 as c
# import pigpio
#
# #servo setup:
# pi=pigpio.pi()
# pi.set_mode(23,pigpio.OUTPUT)
# pi.set_servo_pulsewidth(23,1500)
# print("servo setup")

#Eth0Status = os.popen("sudo ifconfig eth0").read()

#print(Eth0Status)

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432  # The port used by the server
BUFSIZE=1024
ADDR=(HOST,PORT)
tcpSerSock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
print('Waiting for connection')
tcpCliSock,addr=tcpSerSock.accept()
print('...connected from:',ADDR)
# tcpSerSock.settimeout(0.5) #Socket reader moves on after waiting for a new message for 1 second
scale = 90

L=0
R=0
V=0
cam=100
angle=1000+cam*1000/180
n=0
while True:
    print("while true")
    try:
        
        '''START Disconnect Safety Override'''      
        try:
            #reads new commands from socket
            tcpCliSock,addr=tcpSerSock.accept()
            print('Connected by', addr)
            Dat=tcpCliSock.recv(BUFSIZE).decode("utf-8")
            n=0
            if not Dat:
                print('break1')
                break
            print(Dat)
        
        except:
            #catches any exception (most likely timeout after 0.5 second) that prevents successful command read.'''
            Dat = "0,0,0,0,0,0,0,0,0,A"
            
        '''END Disconnect Safety Override'''
        
        try:
            data=Dat.split(",")
            if data[9] == 'R':
                i=float(data[0])
                j=float(data[1])
                k=float(data[2])

                if(abs(i)<0.2):
                    i=0
                if(abs(j)<0.2):
                    j=0
                if(abs(k)<0.2):
                    k=0
                L=i
                R=j
                V=k
                print(i,j,k,float(data[3]))
                if data[6] == 1:
                    angle = angle + 5
                if data[7] == 1:
                    angle = angle - 5
                if data[8] == 1:
                    angle = angle + 1
                if data[9] == 1:
                    angle = angle - 1
                if(angle<1200):
                    angle=1200
                if(angle>2000):
                    angle=2000
                # pi.set_servo_pulsewidth(23,angle)
                #
                #
                # c.L(L*scale)
                # c.R(R*scale)
                # c.LV(V*scale)
                # c.RV(V*scale)

                data = str('%2.2f,%2.2f,%2.2f,%2.2f' % (L*scale, R*scale, V*scale,angle))
                tcpSerSock.send(data.encode())
                
        except:
            continue
    except KeyboardInterrupt:
        break
tcpSerSock.close()
            

from socket import *
import os
import sys
import subprocess
import time

ip = sys.argv[1]
port = int(sys.argv[2])
clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect((ip, port))

print('connection starts.')
#filename = input('Type the name of file: ')
filename = 'hello.sh'
clientSock.sendall(filename.encode('utf-8'))

data = clientSock.recv(1024)
data_transferred = 0

if not data:
    print('file %s does not exit' %filename)
    sys.exit()

nowdir = os.getcwd()
with open(filename, 'wb') as f: #현재dir에 filename으로 파일을 받는다
    try:
        while data: #데이터가 있을 때까지
            f.write(data) #1024바이트 쓴다
            data_transferred += len(data)
            data = clientSock.recv(1024) #1024바이트를 받아 온다
    except Exception as ex:
        print(ex)
print('file %s has been succefully transferred. data %d' %(filename, data_transferred))
clientSock.close()


subprocess.call("sh ./hello.sh", shell=True)
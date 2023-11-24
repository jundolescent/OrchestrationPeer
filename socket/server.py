from socket import *
from os.path import exists
import sys
import subprocess
import time

ip = sys.argv[1]
port = int(sys.argv[2])
serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind((ip, port))
serverSock.listen(1)

subprocess.call("./dockerswarm.sh %s" % ip, shell=True)

connectionSock, addr = serverSock.accept()

print(str(addr),'has connected')

filename = connectionSock.recv(1024) #클라이언트한테 파일이름(이진 바이트 스트림 형태)을 전달 받는다
print('Received data : ', filename.decode('utf-8')) #파일 이름을 일반 문자열로 변환한다
data_transferred = 0

if not exists(filename):
    print("no file")
    sys.exit()

print("file %s sending starts" %filename)
with open(filename, 'rb') as f:
    try:
        data = f.read(1024) #1024바이트 읽는다
        while data: #데이터가 없을 때까지
            data_transferred += connectionSock.send(data) #1024바이트 보내고 크기 저장
            data = f.read(1024) #1024바이트 읽음
    except Exception as ex:
        print(ex)
print("Complete %s, data %d" %(filename, data_transferred))

time.sleep(3)
serverSock.close()
connectionSock.close()


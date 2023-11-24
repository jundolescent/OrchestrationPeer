from socket import *
import os
import sys

CHUNKSIZE = 1_000_000

# Make a directory for the received files.
os.makedirs('client',exist_ok=True)

ip = sys.argv[1]
port = int(sys.argv[2])
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((ip,port))
with sock,sock.makefile('rb') as clientfile:
    while True:
        raw = clientfile.readline()
        if not raw: break # no more files, server closed connection.

        filename = raw.strip().decode()
        length = int(clientfile.readline())
        print(f'Downloading {filename}...\n  Expecting {length:,} bytes...',end='',flush=True)

        path = os.path.join('client',filename)
        os.makedirs(os.path.dirname(path),exist_ok=True)

        # Read the data in chunks so it can handle large files.
        with open(path,'wb') as f:
            while length:
                chunk = min(length,CHUNKSIZE)
                data = clientfile.read(chunk)
                if not data: break
                f.write(data)
                length -= len(data)
            else: # only runs if while doesn't break and length==0
                print('Complete')
                continue

        # socket was closed early.
        print('Incomplete')
        break 

sock.close()
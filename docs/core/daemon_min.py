import socket,threading,hashlib
HOST="127.0.0.1";PORT=31337

def h(c):
 d=c.recv(4096)
 sig=hashlib.sha256(d).hexdigest()
 c.send(("[ACK] "+sig+"\n").encode())
 c.close()

s=socket.socket()
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((HOST,PORT))
s.listen(5)

while 1:
 c,_=s.accept()
 threading.Thread(target=h,args=(c,),daemon=1).start()

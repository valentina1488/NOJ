#!/usr/bin/python3
from socket import *
import threading, subprocess, argparse, sys,time,asyncio
ANOTHER_APPLOGIC=None
class client(threading.Thread):
    def __init__(self, socket, address):
        threading.Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()
    def run(self):
        while 1:
            req=self.sock.recv(1024).decode()
            print('Client sent: '+req) 
            logg('\n[*] '+time.asctime()+' received '+str(len(req))+' bytes from '+str(self.addr)+'(client):\n'+req) 
            self.sock.send(b'Oi you sent something to me')
def client_handler(client):
    pass
def threading_server(port=8888,ip='127.0.0.1'):
    s=socket(); s.bind((ip,port))
    s.listen(5)
    while 1:
        cs,addr=s.accept()
        th=threading.Thread(target=client_handler, args=(cs,)); th.start()
class Applogic:
    info=None
    def parse_income(self,data):
        logg('[*] '+time.asctime()+' received '+str(len(data))+' bytes from '+str(self.info)+' (client):\n'+data+'\n')
        print('got data:\n'+data+'\nfrom '+str(self.info))
class tcp(asyncio.Protocol):
    trans=None
    def __init__(self,applogic):
        self.applogic=applogic
    def connection_made(self,transport):
        print('im here')
        self.trans=transport
        self.applogic.info=transport.get_extra_info('peername')
        logg('[*] '+time.asctime()+' connection from '+str(self.applogic.info)+'\n')
        print('{} connected'.format(self.applogic.info))
    def data_received(self, data):
        mess=data.decode()
        self.applogic.parse_income(data=mess)
        # self.applogic.ans(trans)
        self.trans.write(b'dadaprivet')
    def connection_lost(self,exc):
        logg('[*] '+time.asctime()+'{} disconnected'.format(str(self.applogic.info))+'\n')
        print('{} leaved'.format(str(self.applogic.info)))
def get_tcp_prot(applogic=Applogic):
    return tcp(applogic())
def tcp_server(applogic,port=8888):
    loop=asyncio.get_event_loop()
    zuko=loop.create_server(get_tcp_prot, '0.0.0.0', 8888)
    server=loop.run_until_complete(zuko)
    print(server)
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('\nstopped')
def drop(string, s,host):
    try:
        s.send(string.encode())
        logg('[*]'+time.asctime()+' sent '+str(len(string))+' bytes from '+host+'\n'+string+'\n')
        ln=1488; buf=''; resp=''
        while 1:
            if ln<1488:
                break
            buf=s.recv(1488).decode()
            ln=len(buf)
            resp+=buf
        logg('[*]'+time.asctime()+' recieved '+str(len(resp))+' bytes from '+host+' (host) :\n'+resp+'\n')
        return resp
    except:
        print('\nSOMETHING WENT WRONG\n')
        logg('\n[shit happens]\n')
def interact_dflt(host,port=80, from_file=None):
    s=socket(AF_INET,SOCK_STREAM)
    s.connect((host,port))
    print(s)
    buf=''
    if from_file: buf=open(from_file,'rb').read()
    else: buf=sys.stdin.read()
    ans=drop(buf,s,host); print(ans)
    s.close()
if __name__=='__main__':
    parser=argparse.ArgumentParser(description='moe detishe')
    parser.add_argument('-t','--target',help='host to connet')
    parser.add_argument('-sf', '--send-file', help='send from file')
    parser.add_argument('-l','--listen', help='listen to port', action='store_true')
    parser.add_argument('-logg', '-log', help='location to logg actions')
    parser.add_argument('-c','--connect', help='connect to host with specified port', nargs='+')
    args=parser.parse_args()
    logg=lambda x: open(args.logg, 'a').write(x) if args.logg else lambda x: None
    if args.connect:
        if len(args.connect)==2: interact_dflt(args.connect[0],int(args.connect[1]))
        else: interact_dflt(args.connect[0])
    if args.listen: tcp_server(applogic=Applogic,port=args.listen)

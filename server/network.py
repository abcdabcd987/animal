# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 16:19:21 2014

@author: Juda
"""

import socket
import record
import random

class server:
    '''
    network communication by using socket
    '''
    def __init__(self,log):
        host=socket.gethostbyname(socket.gethostname())
        port=12345
        self.log=log
        self.spy=socket.socket()
        self.spy.bind((str(host),port))
        self.spy.listen(2)        
        
        self.log.logging("waiting to connect ...",'SHOWALL')
        self.log.logging("The PC's host is %s"%host,'SHOWALL')
        
        self.AI=[None,None]
        self.AIname=[None,None]        
        
        #determine which player is first player
        first=0
        if random.random()<0.5:
            first=1
        self.first_player = first

        self.AI[0],addr=self.spy.accept()
        self.log.logging("%s connected"%addr[0],'SHOWALL')
        self.AI[1],addr=self.spy.accept()
        self.log.logging("%s connected"%addr[0],'SHOWALL')

        self.AI[0].settimeout(2)
        self.AI[1].settimeout(2)

        self.send(self.AI[0],str(first))
        self.AIname[0]=self.recieve(self.AI[0]).strip()
        self.send(self.AI[1],str(1-first))
        self.AIname[1]=self.recieve(self.AI[1]).strip()
        self.log.logging("%s is the first player"%self.AIname[first],'SHOWALL')
        self.log.logging("%s is the second player"%self.AIname[1-first],'SHOWALL')

        self.log.addJsonUser(self.AIname[0],self.AIname[1])
        
    def send(self,client,message):
        client.send('%s\n'%message)
        
    def recieve(self,client):
        res=''
        for i in xrange(100):        
            ch=client.recv(1)
            res+=ch
            if ch=='\n':
                break
        return res.strip()
        
    def __del__(self):
        self.AI[0].close()
        self.AI[1].close()

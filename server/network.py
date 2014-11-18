# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 16:19:21 2014

@author: Juda
"""

import sys
import socket
import record
import random
import thread
import time
import select

class server:
    '''
    network communication by using socket
    '''
    def __init__(self,log):
        if len(sys.argv) >= 2 and sys.argv[1] == 'p2dv':
            host = '127.0.0.1'
        else:
            host=socket.gethostbyname(socket.gethostname())
        port=random.randint(1234,12345)
        self.log=log
        self.spy=socket.socket()
        self.spy.bind((str(host),port))
        self.spy.listen(2)        
        
        self.log.logging("waiting to connect ...",'SHOWALL')
        self.log.logging("The PC's host is %s, the port is %d"%(host,port),'SHOWALL')
        
        self.AI=[None,None]
        self.AIname=['unknown0','unknown1']        
        
        #determine which player is first player
        first=0
        if random.random()<0.5:
            first=1
        self.first_player = first

        connectSuccessful=[0,0]
        
        infds,outfds,errfds=select.select([self.spy],[],[],5)
        if len(infds)==1 and (infds[0] is self.spy):
        	try:
        		self.AI[0],addr=infds[0].accept()
        		self.send(self.AI[0],'0')
        		self.AIname[0]=self.recieve(self.AI[0]).strip()
        		self.log.addJsonUser(self.AIname[0],'unknown')
        		self.log.logging("player 0 wins",'SHOWALL')
        		self.log.addJsonNumber('result',0)
        		exit(0)
        	except Exception:
        		self.log.logging('both AI error, game tie!','SHOWALL')
        		self.log.addJsonNumber('result',2)
        		exit(0)
        elif len(infds)==2:
        	if infds[0] is self.spy:
        		try:
        			self.AI[0],addr=infds[0].accept()
        			self.send(self.AI[0],str(first))
        			self.AIname[0]=self.recieve(self.AI[0]).strip()
        			connectSuccessful[0]=1
        		except Exception,e:        			
        			self.log.logging(e)
        			self.log.logging("player 0 error",'SHOWALL')

        	if infds[1] is self.spy:
        		try:
        			self.AI[1],addr=infds[1].accept()
        			self.send(self.AI[1],str(1-first))
        			self.AIname[1]=self.recieve(self.AI[1]).strip()
        			connectSuccessful[1]=1
        		except Exception,e:
        			self.log.logging(e)
        			self.log.logging("player 1 error",'SHOWALL')

        self.log.addJsonUser(self.AIname[0],self.AIname[1])
        self.log.logging('2 players: %s VS %s'%(self.AIname[0],self.AIname[1]),'SHOWALL')
        if connectSuccessful!=[1,1]:
        	if connectSuccessful==[0,0]:
        		self.log.logging('both AI error, game tie!','SHOWALL')
        		self.log.addJsonNumber('result',2)
        	elif connectSuccessful==[1,0]:
        		self.log.logging('player 0 [%s] wins'%self.AIname[0],'SHOWALL')
        		self.log.addJsonNumber('result',0)
        	elif connectSuccessful==[0,1]:
        		self.log.logging('player 1 [%s] wins'%self.AIname[1],'SHOWALL')
        		self.log.addJsonNumber('result',1)
        	exit(0)

        self.AI[0].settimeout(2)
        self.AI[1].settimeout(2)

        self.log.logging("%s is the first player"%self.AIname[first],'SHOWALL')
        self.log.logging("%s is the second player"%self.AIname[1-first],'SHOWALL')

        
        
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
        if self.AI[0]:
        	self.AI[0].close()
        if self.AI[1]:
        	self.AI[1].close()
        if self.spy:
        	self.spy.close()

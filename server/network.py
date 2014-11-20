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
        self.log=log
        self.log.logging('Initialization:', 'SHOWALL')
        if len(sys.argv) >= 2 and sys.argv[1] == 'p2dv':
            self.isp2dv = True
            self.log.logging('    p2dv.in mode', 'SHOWALL')
        else:
            self.isp2dv = False

        if self.isp2dv:
            host = 'localhost'
        else:
            host=socket.gethostbyname(socket.gethostname())

        # Find a unused port
        while True:
            try:
                port=random.randint(1024,65535)
                self.spy=socket.socket()
                self.spy.bind((str(host),port))
                self.spy.listen(2)
                if self.isp2dv:
                    self.spy.settimeout(1)
                break
            except:
                self.log.logging('    Port %d is used. Trying another.' % (port), 'SHOWALL')
        
        self.log.logging("    Waiting to connect ...",'SHOWALL')
        self.log.logging("    The PC's host is %s, the port is %d"%(host,port),'SHOWALL')
        
        # Determine which player is first player  
        first = 0 if random.random()<0.5 else 1
        self.first_player = first

        # Wait for AIs to connect
        self.AI=[None,None]
        self.AIname=[None,None]
        ## Wait AI0
        try:
            self.AI[0],addr=self.spy.accept()
            self.AI[0].settimeout(2)
            self.send(0,str(first))
            self.AIname[0]=self.receive(0, '[Unknown]')
            self.log.logging("    AI0: %s from %s connected"%(self.AIname[0],addr[0]),'SHOWALL')
        except:
            if not self.isp2dv:
                exit(1)
            self.log.logging('    AI0 timeout', 'SHOWALL')
            self.AI[0] = None
        ## Wait AI1
        try:
            self.AI[1],addr=self.spy.accept()
            self.AI[1].settimeout(2)
            self.send(1,str(1-first))
            self.AIname[1]=self.receive(1, '[Unknown]')
            self.log.logging("    AI1: %s from %s connected"%(self.AIname[1],addr[0]),'SHOWALL')
        except:
            if not self.isp2dv:
                exit(1)
            self.log.logging('    AI1 timeout', 'SHOWALL')
            self.AI[0] = None

        self.log.addJsonUser(self.AIname[0],self.AIname[1])

        # Check if AIs timeout
        if not self.AI[0] and not self.AI[1]:
            self.log.logging('    Both AI timeout. Tie!', 'SHOWALL')
            self.log.addJsonNumber('result', 2)
            exit(0)
        elif self.AI[0] and not self.AI[1]:
            self.log.logging('    AI1 timeout. AI0 wins.', 'SHOWALL')
            self.log.addJsonNumber('result', 0)
            exit(0)
        elif self.AI[1] and not self.AI[0]:
            self.log.logging('    AI0 timeout. AI1 wins.', 'SHOWALL')
            self.log.addJsonNumber('result', 1)
            exit(0)


        self.log.logging("    %s is the first player"%self.AIname[first],'SHOWALL')
        self.log.logging("    %s is the second player"%self.AIname[1-first],'SHOWALL')
        
        
    def send(self,clientID,message):
        try:
            self.AI[clientID].send('%s\n'%message)
        except:
            self.log.logging('    Send message to AI%d timeout. AI%d wins.'%(clientID, 1-clientID), 'SHOWALL')
            self.log.addJsonNumber('result', 1-clientID)
            exit(0)
        
    def receive(self,clientID,fbvalue=None):
        try:
            res = self.AI[clientID].recv(128)
            return res.strip()
        except:
            if not fbvalue:
                self.log.logging('    Receive message from AI%d timeout. AI%d wins.'%(clientID, 1-clientID), 'SHOWALL')
                self.log.addJsonNumber('result', 1-clientID)
                exit(0)
            else:
                return fbvalue
        
    def __del__(self):
        if self.AI[0]:
        	self.AI[0].close()
        if self.AI[1]:
        	self.AI[1].close()
        if self.spy:
        	self.spy.close()

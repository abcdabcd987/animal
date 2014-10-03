# -*- coding: utf-8 -*-
"""
Created on Fri Oct 03 11:24:31 2014

@author: juda
"""

import time

class record:
    '''
    record all infomation during the match.
    '''
    def __init__(self):
        self.file=open("%s.log"%self.__nowTime__(),'w')
    
    def __nowTime__(self):
        temp=time.asctime().split()
        return temp[1]+temp[2]+'_'+''.join(temp[3].split(':'))+'_'+temp[4]
    
    def logging(self,message,mode="FILE"):
        self.file.write("%s\n"%message)
        self.file.flush()
        if mode!="FILE":
            print message
            
    def __del__(self):
        print "log closed"
        self.file.close()
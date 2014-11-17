#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 22:43:57 2014

@author: Juda
@email: judaplus@sjtu.edu.cn
"""

import network
import record
import chess

log=record.record()
server=network.server(log)
board=chess.chess(log)

log.logging("Game Begin",'SHOWALL')

now_player=1-server.first_player
player_limit=[3,3]

steps=0
while True:
    if step == 5000:
        log.logging('Draw!','SHOWALL')
        log.addJsonNumber('result',2)
    break

    steps+=1
    now_player=1-now_player;
    server.send(server.AI[now_player],'action')
    log.logging("Send to player %d [name: %s] a signal: ACTION"%(now_player,server.AIname[now_player]))
    try:
        message=server.recieve(server.AI[now_player])
    except socket.timeout:
        log.logging("Recieve message form player %d [name: %s]: TIME EXCEEDED LIMIT"%(now_player,server.AIname[now_player]),'SHOWALL')
        log.logging("the player %d (name %s) win the game"%(1-now_player,server.AIname[1-now_player]),'SHOWALL')
        log.addJsonNumber('result',1-now_player)
        break
    log.logging("Recieve message form player %d [name: %s]: %s"%(now_player,server.AIname[now_player],message))
    if not (message=="None"):        
        message=chess.transMessage(now_player,message)
        log.logging("transform message form [number: %d] [name: %s]: %s"%(now_player,server.AIname[now_player],message))
        feedback=board.check(now_player,message)
        if feedback!=False:
            log.logging("player %d [name %s] choose (%d,%d) move to (%d %d)"%(now_player,server.AIname[now_player],feedback[0],feedback[1],feedback[2],feedback[3]),"SHOWALL")
            server.send(server.AI[0],'%d %d %d %d %d'%(now_player,feedback[0],feedback[1],feedback[2],feedback[3]))
            log.logging("Send to player 0 [name: %s] infomation : (%d %d %d %d %d)"%(server.AIname[0],now_player,feedback[0],feedback[1],feedback[2],feedback[3]))
            server.send(server.AI[1],'%d %d %d %d %d'%(now_player,8-feedback[0],6-feedback[1],8-feedback[2],6-feedback[3]))
            log.logging("Send to player 1 [name: %s] infomation : (%d %d %d %d %d)"%(server.AIname[1],now_player,8-feedback[0],6-feedback[1],8-feedback[2],6-feedback[3]))
            log.addJsonStep(player=now_player,valid=True,source=[feedback[0],feedback[1]],target=[feedback[2],feedback[3]])
            if (feedback[2],feedback[3]) in ((0,3),(8,3)):
                log.logging("the player %d (name %s) win the game"%(now_player,server.AIname[now_player]),'SHOWALL')
                log.addJsonNumber('result',now_player)
                break
        else:
            log.logging("invalid action",'SHOWALL')
            player_limit[now_player]-=1
            log.logging("the limit of invalid action of player %d (name %s) is %d"%(now_player,server.AIname[now_player],player_limit[now_player]),'SHOWALL')
            log.addJsonStep(player=now_player,valid=False)
    else:
        player_limit[now_player]-=1
        log.logging("the limit of invalid action of player %d (name %s) is %d"%(now_player,server.AIname[now_player],player_limit[now_player]),'SHOWALL')
        log.addJsonStep(player=now_player,valid=False)
    if player_limit[now_player]==0:
        log.logging("the player %d (name %s) win the game"%(1-now_player,server.AIname[1-now_player]),'SHOWALL')
        log.addJsonNumber('result',1-now_player)
        break
        
try:
    server.send(server.AI[0],"game end")
    log.logging("player %d [name: %s] connection closed succueefully"%(0,server.AIname[0]))
except Exception, e:
    log.logging("player %d [name: %s] connection closed failed"%(0,server.AIname[0]))

try:
    server.send(server.AI[1],"game end")
    log.logging("player %d [name: %s] connection closed succueefully"%(1,server.AIname[1]))
except Exception, e:
    log.logging("player %d [name: %s] connection closed failed"%(1,server.AIname[1]))

log.logging("total steps : %d"%steps,'SHOWALL')
log.addJsonNumber('total',steps)


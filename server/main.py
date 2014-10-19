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

now_player=0
player_limit=[3,3]

while True:
    server.send(server.AI[now_player],'action')
    log.logging("Send to player %d [name: %s] a signal: ACTION"%(now_player,server.AIname[now_player]))
    message=server.recieve(server.AI[now_player])
    log.logging("Recieve message form player %d [name: %s]: %s"%(now_player,server.AIname[now_player],message))
    if not message=="None":        
        message=chess.chess.transMessage(now_player,message)
        log.logging("transform message form [number: %d] [name: %s]: %s"%(now_player,server.AIname[now_player],message))
        feedback=board.check(now_player,message)
        if feedback!=False:
            log.logging("player %d [name %s] choose (%d,%d) move to (%d %d)"%(now_player,server.AIname[now_player],feedback[0],feedback[1],feedback[2],feedback[3]),"SHOWALL")
            server.send(server.AI[0],'%d %d %d %d %d'%(now_player,feedback[0],feedback[1],feedback[2],feedback[3]))
            log.logging("Send to player 0 [name: %s] infomation : (%d %d %d %d %d)"%(server.AIname[0],now_player,feedback[0],feedback[1],feedback[2],feedback[3]))
            server.send(server.AI[1],'%d %d %d %d %d'%(now_player,8-feedback[0],6-feedback[1],8-feedback[2],6-feedback[3]))
            log.logging("Send to player 1 [name: %s] infomation : (%d %d %d %d %d)"%(server.AIname[1],now_player,8-feedback[0],6-feedback[1],8-feedback[2],6-feedback[3]))
            if (feedback[2],feedback[3]) in ((0,3),(8,3)):
                log.logging("the player %d (name %s) win the game"%(now_player,server.AIname[now_player],message))
                break
        else:
            log.logging("invaild action",'SHOWALL')
            player_limit[now_player]-=1
            log.logging("the limit of invaild action of player %d (name %s) is %d"%(now_player,server.AIname[now_player],player_limit[now_player]),'SHOWALL')
    else:
        player_limit[now_player]-=1
        log.logging("the limit of invaild action of player %d (name %s) is %d"%(now_player,server.AIname[now_player],player_limit[now_player]),'SHOWALL')
    if player_limit[now_player]==0:
        log.logging("the player %d (name %s) win the game"%(1-now_player,server.AIname[1-now_player],message))
        break
        
        

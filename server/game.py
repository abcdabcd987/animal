# -*- coding: utf-8 -*-
from threading import Thread

class Game(Thread):
    """docstring fo(Thread)"""
    def __init__(self, queue):
        super(Game, self).__init__()
        self.queue = queue       

    def run(self):
        while True:
            time.sleep(2)
            temp=self.queue.get()
            if temp=='End':
                break
            
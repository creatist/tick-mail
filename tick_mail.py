#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from threading import Timer
from mail import Mail
import time
import os
import scratch_ip

def send_mail(usr='1459032556@qq.com', pwd='tnyoawashxvfheic', smtp = 'smtp.qq.com', smtp_port = 587,to_addr = ['1459032556@qq.com'],text='Hello'):
    mail = Mail(usr,pwd,smtp,smtp_port)
    text_type_dict_list=[{'text':'Hello,dear!','type':'plain'}]
    text_type_dict_list[0]['text'] = text
    mail.send(to_addr,text_type_dict_list=text_type_dict_list)
class TickMail():
    def __init__(self,orig_ip='',interval = 3,tick_times=5):
        self.orig_ip = orig_ip
        self.ticks = 0
        self.interval = interval
        self.tick_times = tick_times

    def tick(self):
        if_send = 0
        ip = scratch_ip.get_ip()
        if self.orig_ip == ip:
            #print ip + " not changed"
            if self.ticks == self.tick_times :
                if_send = 1
            else:
                if_send = 0
        else:
            if_send = 1

        if if_send == 1:
            send_mail(text = ip)
            self.orig_ip = ip
            self.ticks = 0
            if_send = 0
        self.ticks = self.ticks + 1
        t = Timer(self.interval,self.tick)
        t.start()


if __name__ == '__main__':
    tick_mail = TickMail(interval = 10 * 60, tick_times = 6)
    tick_mail.tick()

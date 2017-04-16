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


def send_mail(usr='xxxxxxxxxx@xx.com', pwd='xxxxxxxxxxxxxxxx', smtp = 'smtp.qq.com', smtp_port = 587,to_addr = ['xxxxxxxxxxxxxxxxx'],text='Hello'):
    mail = Mail(usr,pwd,smtp,smtp_port)
    text_type_dict_list=[{'text':'Hello,dear!','type':'plain'}]
    text_type_dict_list[0]['text'] = text
    mail.send(to_addr,text_type_dict_list=text_type_dict_list)
    

def tick():
    ip = scratch_ip.get_ip()
    send_mail(text = ip)
    t = Timer(3,tick)
    t.start()


if __name__ == '__main__':
    tick()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from  email.mime.base import MIMEBase
import smtplib
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

class Mail():
    def __init__(self,usr,pwd,smtp=None,smtp_port=None,pop3=None,pop3_port=None,debug_level=1):

        self.usr = usr
        self.pwd = pwd 
        self.to = usr
        self.smtp = smtp
        self.smtp_port = smtp_port
        self.pop3 = pop3
        self.pop3_port = pop3_port
        self.server = smtplib.SMTP(self.smtp,self.smtp_port)
        if self.smtp_port == 25:
            self.crypt = False
        else:
            self.crypt = True  #port maybe 587
        if self.crypt:
            self.server.starttls()
        self.server.set_debuglevel(debug_level)

        #self.server.login(self.usr,self.pwd)

    def add_text(self,text_type_dict_list,encode='utf-8'):
        if not isinstance(text_type_dict_list,list):
            print 'argument text_type_dict should be a dict list'
            return
        if len(text_type_dict_list)>0 and not isinstance(text_type_dict_list[0],dict):
            print 'argument text_type_dict[0] should be a dict '
            return
        for text_type_dict in text_type_dict_list:
            if 'text' in text_type_dict and 'type' in text_type_dict:
                self.msg.attach( MIMEText(text_type_dict['text'],text_type_dict['type'],encode) )

    def do_add_attachment(self,filepath,filetype_list,filename):
        if not filetype_list:
            print 'argument filetype_list is empty'
            return

        with open(filepath,'rb') as f:
            mime = MIMEBase(filetype_list[0],filetype_list[1],filename=filename)
            mime.add_header('Content-Disposition','attachment',filename = filename)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            self.msg.attach(mime)

    def add_attachment(self,attachment_dict_list):
        if not isinstance(attachment_dict_list,list):
            print 'attachment_dict_list should be a dict list'
            return
        if len(attachment_dict_list)>0 and not isinstance(attachment_dict_list[0],dict):
            print 'attachment_dict_list should be a dict'
            return 
        for attachment_dict in attachment_dict_list:
            if 'filepath' in attachment_dict and 'filetype_list' in attachment_dict and 'filename' in attachment_dict:
                self.do_add_attachment(attachment_dict['filepath'],attachment_dict['filetype_list'],attachment_dict['filename'])
            

    def send(self,to_list,text_type_dict_list=None,attachment_dict_list=None,from_to_subject='',encode='utf-8'):

        self.msg = MIMEMultipart('alternative')
        self.add_text(text_type_dict_list,encode)
        self.add_attachment(attachment_dict_list)
        
        if 'From' in from_to_subject:
            self.msg['From'] = _format_addr(from_to_subject['From'])
        else: 
            self.msg['From'] = _format_addr(self.usr)
        if 'To' in from_to_subject:
            self.msg['To'] = _format_addr(from_to_subject['To'])
        else:
            self.msg['To'] = _format_addr(self.to)
        if 'Subject' in from_to_subject:
            self.msg['Subject'] = Header(from_to_subject['Subject'],encode).encode()
        else:
            pass
        
        self.server.login(self.usr,self.pwd)
        self.server.sendmail(self.usr,to_list,self.msg.as_string())
        self.server.quit()

if __name__ == '__main__':

    usr = raw_input('input from address: ')
    pwd =raw_input('input password: ')
    smtp = 'smtp.qq.com'
    smtp_port = 465
    smtp_port = 587
    
    to = raw_input('input target address: ')
    text_type_dict_list=[{'text':'Hello,dear!','type':'plain'},{'text':'<html><body><h1>Hello</h1></body></html>','type':'html'}]
    from_to_subject={'From':'kingsting','To':'青青子衿','Subject':'无题'}
    attatchment_list=[{'filepath':'./qrcode.png','filename':'pic1.png','filetype_list':['image','png']},{'filepath':'./qrcode1.png','filename':'pic2.png','filetype_list':['image','png']}]
    mail = Mail(usr,pwd,smtp,smtp_port) 
    mail.send(to,text_type_dict_list=text_type_dict_list,attachment_dict_list=attatchment_list,from_to_subject=from_to_subject)

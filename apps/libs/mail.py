#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import smtplib
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.header import Header
 
sender = '2917071792@qq.com'
receivers = ['yfsoftcom_4440ea@kindle.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
attachment = '深入react+技术栈.mobi'
 
#创建一个带附件的实例
message = MIMEMultipart()
message['From'] = Header("2917071792@qq.com", 'utf-8')
message['To'] =  "yfsoftcom_4440ea@kindle.cn"
subject = '深入react+技术栈'
message['Subject'] = Header(subject, 'utf-8')
 
#邮件正文内容
message.attach(MIMEText('This is a e-book~', 'plain', 'utf-8'))

# 二进制方式模式文件
with open(attachment, 'rb') as f:
    # MIMEBase表示附件的对象
    mime = MIMEBase('application', 'octet-stream', filename=attachment)
    # filename是显示附件名字
    mime.add_header('Content-Disposition', 'attachment', filename=attachment)
    # 获取附件内容
    mime.set_payload(f.read())
    encoders.encode_base64(mime)
    # 作为附件添加到邮件
    message.attach(mime)
 
try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect('smtp.qq.com')
    smtpObj.login('2917071792@qq.com', 'apzndkhyethwdefa')
    smtpObj.sendmail(sender, receivers, message.as_string())
    smtpObj.close()
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print("Error: 无法发送邮件", e)
#-*- coding:UTF-8 -*-
import smtplib
import os
import time
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def send_mail(msg):
    date = time.strftime('%y%m%d')
    dirpath = "D:\Work\Security\inspection\pictures\\" + date + '\\'
    dirpics = os.listdir(dirpath)
    mail_host = 'smtp.chinaamc.com'
    mail_user = 'lic'
    mail_pass = 'KGB@8806'
    sender = 'lic@chinaamc.com'
    receivers = ['lic@chinaamc.com','zhaolei@chinaamc.com']
    message = MIMEMultipart('related')
    message['From'] = Header('lic', 'utf-8')
    message['To'] = Header('设备巡检', 'utf-8')
    subject = '巡检内容'
    message['Subject'] = Header(subject, 'utf-8')
    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
    mail_msg = """
    <p>巡检报告</p>
    <p>图片演示</p>
    """
    mail_msg += '<p>' + msg + '</p>'
    cid = 1
    for pic in dirpics:
        mail_msg += "<p><img src=cid:pos" + str(cid) + "></p>" + '\n'
        cid += 1
    print 'Email:', mail_msg
    msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
    pos = 1
    for pic in dirpics:
        with open(dirpath + pic, 'rb') as fp:
            msgImage = MIMEImage(fp.read())
            msgImage.add_header('content-ID', 'pos' + str(pos))
            pos += 1
            message.attach(msgImage)
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 587)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('Good Job')
    except smtplib.SMTPException:
        print('Fail')

#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import config


def html_table(content):
    cont_start = '''<table border="1" class="dataframe">'''
    content_end = '''</table>'''

    return cont_start + content + content_end


def send_email(subject, content):
    # 第三方 SMTP 服务
    mail_host = config.mail['host']  # 设置服务器
    mail_user = config.mail['user']  # 用户名
    mail_pass = config.mail['pass']  # 口令
    mail_port = config.mail['port']  # 端口

    sender = config.mail['sender']
    receivers = config.mail['receivers']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = sender

    message['Subject'] = Header(subject, 'utf-8')
    print("发送邮件")
    try:
        smtp = smtplib.SMTP(mail_host, mail_port)
        smtp.ehlo()
        if mail_host == 'smtp.gmail.com':
            smtp.starttls()
        smtp.login(mail_user, mail_pass)
        for to_addr in receivers:
            message['To'] = to_addr
            smtp.sendmail(sender, to_addr, message.as_string())
            print('send mail :', to_addr)
        smtp.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: ", e)

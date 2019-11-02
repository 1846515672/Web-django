from __future__ import absolute_import
from email.mime.text import MIMEText #用于发送邮件
from email.header import Header
import smtplib #用于发送邮件
from Qshop.celery import app


@app.task
def add(x, y):
    x, y = 1, 2
    print(x+y)
    return x+y

@app.task
def sendMial(content, email):
    from Qshop.settings import MAIL_SENDER,MATL_PASSWORD,MAIL_SERVER,MAIL_PORT

    content = """请确认是否是本人,请点击下方链接进行修改密码
    <a href="%s">点击确认</a>"""%content
    print(content)
    #构建邮件格式
    message = MIMEText(content, "html" "utf-8")

    message["To"] = Header(email, 'utf-8')
    message["From"] = Header(MAIL_SERVER, 'utf-8')
    message["Subject"] = Header("密码修改",'utf-8')

    #发送邮件
    smtp = smtplib.SMTP_SSL(MAIL_SENDER, MAIL_PORT)
    smtp.login(MAIL_SENDER, MATL_PASSWORD)
    smtp.sendmail(MAIL_SENDER, [email], message.as_string())
    smtp.close()
    return '邮件已发送'

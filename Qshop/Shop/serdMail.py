import smtplib
from email.mime.text import MIMEText

content = """啊哈,我来了"""#如果将plain改为html,则可以在这里添加html网址
sender = "2719929303@qq.com"#自己的qq号
recver = """
794067332@qq.com,
876911388@qq.com,
329844268@qq.com,
1985054961@qq.com,
1502377018@qq.com,
1339566602@qq.com,
15733129082@163.com,
1693580010@qq.com,
1015174363@qq.com,
1320629993@qq.com,
2816474335@qq.com,
"""#对方的QQ号
password = "bveikvhxwpeodgji"
#构建邮件格式
message = MIMEText(content, "plain" "utf-8")#可以将plain改为html

message["To"] = recver
message["From"] = sender
message["Subject"] = "你猜"

#发送邮件
smtp = smtplib.SMTP_SSL("smtp.qq.com",465)
smtp.login(sender, password)
smtp.sendmail(sender, recver.split(",\n"), message.as_string())
smtp.close()

#------------------------------------------------------------------------
# def sendMail(content,email):
    # 第三方 SMTP 服务

    # receivers = email  # 接收邮件，可设置为自己的邮箱或者其他邮箱
#     subject = 'Python SMTP 邮件测试'
#     content = """
#             如果确认是本人修改密码，请点击下方链接进行修改密码，
#             <a href="%s">点击链接确认</a>
#         """ % content
#
#     message = MIMEText(content, 'plain', 'utf-8')
#     message['From'] = Header(MAIL_SENDER, 'utf-8')
#     message['To'] = Header(email, 'utf-8')
#     message['Subject'] = Header(subject, 'utf-8')
#
#     try:
#         smtpObj = smtplib.SMTP()
#         smtpObj.connect(MAIL_SERVER, 25)  # 25 为 SMTP 端口号
#         smtpObj.login(MAIL_USER, MAIL_PASSWORD)
#         smtpObj.sendmail(MAIL_SENDER,email, message.as_string())
#         print("邮件发送成功")
#     except smtplib.SMTPException  as e:
#         print(e)
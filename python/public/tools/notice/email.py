# -*-encoding: utf-8 -*-
#发送邮件
 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from public.logger import Logger
from public.config import getEmailConfig

emailConfig = getEmailConfig()
#image包可以发送图片形式的附件
# from email.mime.image import MIMEImage
 
# 可以查询文件对应的'Content-Type'
# import mimetypes
# mimetypes.guess_type('c:\\users\\adminstrator\\desktop\\ceshi.xls')
 
 
#多个收件人用逗号隔开
subject = '系统通知'
 
#邮箱的smtp服务器
smtpserver = emailConfig['server']
username = emailConfig['account']
password = emailConfig['password']
 
def sendTextEmail(receiver,text,title=subject):
    # MIMEText有三个参数，第一个对应文本内容，第二个对应文本的格式，第三个对应文本编码
    thebody = MIMEText(text, 'plain', 'utf-8')
    return loginAndSend(receiver,thebody,title)

def sendFile(receiver,text,filePath,title=subject):
    # 读取xlsx文件作为附件，open()要带参数'rb'，使文件变成二进制格式,从而使'base64'编码产生作用，否则附件打开乱码
    att = MIMEText(open(filePath, 'rb').read(), 'base64', 'utf-8')
    att['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    #下面的filename 等号(=)后面好像不能有空格
    attname ='attachment; filename ="123.xlsx"'
    att['Content-Disposition'] = attname
    loginAndSend(receiver,att,title)
 

def loginAndSend(receiver,content,title):
  #下面的to\cc\from最好写上，不然只在sendmail中，可以发送成功，但看不到发件人、收件人信息
    msgroot = MIMEMultipart('related')
    msgroot['Subject'] = title
    msgroot['To'] = ";".join(receiver)  if isinstance(receiver,list) else receiver
    # msgroot['Cc'] = acc
    msgroot['From']	= '管理员'
    msgroot.attach(content)
    
    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    # smtp.connect(smtpserver)
    smtp.login(username, password)
    #发送给多人时，收件人应该以列表形式，areceiver.split把上面的字符串转换成列表
    #只要在sendmail中写好发件人、收件人，就可以发送成功
    # smtp.sendmail(asender, areceiver.split(','), msgroot.as_string())
    #发送给多人、同时抄送给多人，发送人和抄送人放在同一个列表中
    receiverStr = receiver.split(',') if isinstance(receiver,list) else receiver
    try:
      result = smtp.sendmail(username, receiverStr, msgroot.as_string())
      return True if result == {} else False
    except Exception as e:
        Logger.e('发送邮件失败', e)
        return False
    finally:
      smtp.quit()


if __name__ == '__main__':
   sendTextEmail('你好','406827469@qq.com')
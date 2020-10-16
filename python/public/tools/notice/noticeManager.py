from Blinker import Blinker
from config import getGeneralConfig, getManagerInfo
from .email import sendTextEmail
from .wechat import sendWechatMsg
from logger import Logger

noticeWays = getGeneralConfig()['notice_ways']

manager = getManagerInfo()


def sendNotice(text):
    if 'email' in noticeWays:
        result =  sendTextEmail(manager['email'], text)
        Logger.v('发送邮件通知结果:'+str(result))
    if 'wechat' in noticeWays:
        result =  sendWechatMsg('系统通知',text)
        Logger.v('发送微信通知结果:'+str(result))

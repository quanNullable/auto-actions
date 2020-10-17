from public.fetch import post
from public.config import getGeneralConfig
from public.logger import Logger

PUSH_KEY = getGeneralConfig()['serverj_key']


def sendWechatMsg(text, desp):
    api = 'https://sc.ftqq.com/' + PUSH_KEY + '.send'
    data = {'text': text, 'desp': desp}
    response = post(api, data=data)
    errmsg = response.get('errmsg')
    if errmsg == 'success':
        return True
    else:
        Logger.e('发送微信消息失败', errmsg)
        return False

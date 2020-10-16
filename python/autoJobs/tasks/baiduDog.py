import time
from tools.path import addParentDir
addParentDir()
from public.fetch import post
from public.logger import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST='https://pet-chain.duxiaoman.com'

def autoCollect():
    try:
        getVigorList()
        lottery()
    except Exception as e:
        Logger.e('百度莱茨狗一键收取元气失败',e)

def getHeader(timestamp):
    return {
        'Host':	'pet-chain.duxiaoman.com',
        'Connection':	'keep-alive',
        'Content-Length':	'112',
        'Accept':'application/json',
        'Origin':	'https://pet-chain.duxiaoman.com',
        'User-Agent':'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.112 Mobile Safari/537.36 BaiduWallet-8.2.0.8-Android-walletapp_1080_1920_Mi-Note-3-jason_27_8.1.0_4.0.5_405',
        'Content-Type':	'application/json',
        'Referer':	'https://pet-chain.duxiaoman.com/',
        'Accept-Encoding':	'gzip, deflate',
        'Accept-Language':	'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie':'BDUSS=pgElm1Xf5gIBxZZDPwI4Yw==; OPENBDUSS=QAAAAEAAACwpweJJhvbBde9EywgavSCK6am_GnfC2RAp3fpzq4BzWHdyG9lSbH7FGN0mxA0qC4cX2eoT97c7-NVWrQu7V5pziZMVjD_7LxuhJZO_B95gaoXeKIu_jOHivRVkNwsS_oe6rTG7HUwUKj5vQPv8J0CjTEGL3ogVLPZHObfAonZZgA; STOKEN=c5eb0c605a44961d0f3b8533e9de8cd3b1f93338f122b75b82a2e60bddb3ad8d; Hm_lvt_2a9b55018981a1911dd3914ca3f9bcf6={},{}; Hm_lpvt_2a9b55018981a1911dd3914ca3f9bcf6={}'.format(int(timestamp/1000)-3600,int(timestamp/1000),int(timestamp/1000)),
        'DNT':'1',
    }

def getVigorList():
    api = HOST+'/data/vigor/generate'
    timestamp = time.time()*1000
    data = '{"requestId":%d,"appId":1,"tpl":"","timeStamp":null,"nounce":null,"token":null,"phoneType":"android"}' %timestamp
    response = post(
        api,
        headers=getHeader(timestamp),
        data=data,
        verify=False)
    if response['errorNo'] != '00':
       Logger.n('百度莱茨狗收取元气失败','错误代码'+response['errorNo'])
       return
    vigorList = response['data']['amounts']
    if len(vigorList) == 0:
        Logger.v('百度莱茨狗当前没有元气可收取')
    else:
        Logger.v('共有{}个元气可收取'.format(len(vigorList)))
        # count = 0.0
        # for vigor in vigorList:
        #     count += collectVigor(vigor)
        # Logger.v('百度莱茨狗收取元气完毕,本次收取{}个元气'.format(count))
        collectAllVigor()

def collectVigor(id):
    time.sleep(1)
    api = HOST+'/data/vigor/get'
    timestamp = time.time()*1000
    data = '{"amount":%s,"requestId":%d,"appId":1,"tpl":"","timeStamp":null,"nounce":null,"token":null,"phoneType":"android"}' %(id ,timestamp)
    response = post(
        api,
        headers=getHeader(timestamp),
        data=data,
        verify=False)
    count = float(response['data']['amount'])
    return count

def collectAllVigor():
    time.sleep(1)
    api = HOST+'/data/vigor/getall'
    timestamp = time.time()*1000
    data = '{"requestId":%d,"appId":1,"tpl":"","timeStamp":null,"nounce":null,"token":null,"phoneType":"android"}' %timestamp
    response = post(
        api,
        headers=getHeader(timestamp),
        data=data,
        verify=False)
    amounts = response['data']['amounts']
    if len(amounts) > 0:
        count = 0.0
        for amount in amounts:
            count += float(amount)
    Logger.v('百度莱茨狗一键收取元气完毕,本次收取{}个元气'.format(count))
        
def lottery():
    time.sleep(2)
    api = HOST+'/data/lottery/draw'
    timestamp = time.time()*1000
    data = '{"requestId":%d,"appId":1,"tpl":"","timeStamp":null,"nounce":null,"token":null,"phoneType":"android"}' %timestamp
    response = post(
        api,
        headers=getHeader(timestamp),
        data=data,
        verify=False)
    errorMsg = response['errorMsg']
    if errorMsg == 'success':
        Logger.v('百度莱茨狗抽奖成功')
    else:
        Logger.e('百度莱茨狗抽奖失败',errorMsg)


if __name__ == "__main__":
    getVigorList()

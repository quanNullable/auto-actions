import time
from tools.path import addParentDir
addParentDir()
from public.fetch import post, get
from public.logger import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from tasks.wechatLottery2 import joinWechatLottery2

HOST = 'https://lucky.nocode.com/v2/lottery/'
SESSION_IDS = [
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0MDcwNjYzODEsImlhdCI6MTYwMjQ5OTU5MiwiZXhwIjoxNjAzMTA0MzkyfQ.osH0aBIiprbrEmAqk7aZDskso0Mf-8HL1n3zdlpbEgg',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMzM4MDczNTIsImlhdCI6MTYwMjUxMzQzMCwiZXhwIjoxNjAzMTE4MjMwfQ.J8AOaT-DKVZ4XuG13B5tQH6VcSVLu9OIRZtZzbnsouk'
]

global SESSION_ID
SESSION_ID = ''


def getHeaders():
    timestamp = time.time() * 1000
    global SESSION_ID
    return {
        'Host':
        'lucky.nocode.com',
        'Connection':
        'keep-alive',
        'x-request-id':
        '07553790-0c7e-11eb-b83a-bbf70a32c378',
        'authorization':
        'Bearer ' + SESSION_ID,
        'charset':
        'utf-8',
        'sign':
        '4c4d24005f0532a3b11f496e428be98bf9ada9e7',
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 9; Mi Note 3 Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2691 MMWEBSDK/200901 Mobile Safari/537.36 MMWEBID/722 MicroMessenger/7.0.19.1760(0x27001335) Process/appbrand0 WeChat/arm64 NetType/WIFI Language/zh_CN ABI/arm64',
        'content-type':
        'application/json',
        'client-version':
        '7.0.19',
        'Accept-Encoding':
        'gzip,compress,br,deflate',
        'version':
        '1.2.65',
        'platform':
        'wechat',
        'timestamp':
        str(timestamp),
        'Referer':
        'https://servicewechat.com/wx01bb1ef166cd3f4e/744/page-frame.html'
    }


global joinedCount
joinedCount = 0


def getLotteryListAndJoin():
    api = HOST + 'public'
    response = get(api, headers=getHeaders(), verify=False)
    pubicList = response['public']
    if pubicList is None:
        Logger.e('微信抽奖助手抽奖失败', '未获取到大抽奖列表')
    else:
        joinLoterryOneByOne(pubicList)
    squareList = response['square']
    if squareList is None:
        Logger.e('微信抽奖助手抽奖失败', '未获取到小抽奖列表')
    else:
        joinLoterryOneByOne(squareList)
    next = response['links']['next']
    if not next is None:
        getMoreAndJoin(next)
    global joinedCount
    Logger.v('微信抽奖助手抽奖完毕:共成功参与{}次抽奖'.format(joinedCount))
    joinedCount = 0


def getMoreAndJoin(next):
    Logger.v('微信抽奖助手获取下一页:' + next)
    api = HOST.replace('lottery/', next)
    response = get(api, headers=getHeaders(), verify=False)
    squareList = response.get('square')
    if squareList is None:
        Logger.e('微信抽奖助手抽奖失败', '未获取到小抽奖列表')
    else:
        joinLoterryOneByOne(squareList)
    next = response.get('links', {}).get('next')
    if not next is None:
        getMoreAndJoin(next)


def joinLoterryOneByOne(lotteryList):
    if not lotteryList is None:
        unJoinList = list(
            filter(lambda lottery: lottery['joined'] != True,
                   lotteryList)) or []
        if len(unJoinList) != 0:
            global joinedCount
            for item in unJoinList:
                time.sleep(3)
                id = item['id']
                if joinLotery(item['id']):
                    joinedCount += 1


def joinLotery(productId):
    api = HOST + productId + '/join'
    data = '{"form_id":"subscribe_message","subscribe_message":["join_lottery"]}'
    response = post(api, headers=getHeaders(), data=data, verify=False)
    result = response.get('result')
    if result is None:
        Logger.e('微信抽奖助手抽奖' + productId + '失败',
                 response.get('error', {}).get('message'))
        return False
    else:
        return result


def joinWechatLottery1():
    global SESSION_ID
    for session in SESSION_IDS:
        SESSION_ID = session
        Logger.v('微信抽奖助手抽奖开始:' + session)
        getLotteryListAndJoin()


def joinWechatLottery():
    try:
        joinWechatLottery1()
        time.sleep(10)
    except Exception as e:
        Logger.e('微信抽奖第一个失败', e)
    try:
        joinWechatLottery2()
        time.sleep(10)
    except Exception as e:
        Logger.e('微信抽奖第二个失败', e)


if __name__ == "__main__":
    joinWechatLottery()

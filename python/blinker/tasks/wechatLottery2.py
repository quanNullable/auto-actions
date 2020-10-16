import time
from tools.path import addParentDir
addParentDir()
from public.fetch import post, get
from public.logger import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HOST = 'https://api-hdcj.9w9.com/v5/'
USER_INFOS = [{
    'uid': '5WQHFMZ',
    'token': '0365e6e32dccb1b8bcbfce935ca10b33',
}, {
    'uid': 'ZAUJR29',
    'token': '410c703c1e597f92726b91923698c3ff',
}]
global USER_INFO
USER_INFO = {}


def getHeaders():
    timestamp = time.time() * 1000
    USER_INFO.update({
        'Host':
        'api-hdcj.9w9.com',
        'Connection':
        'keep-alive',
        'charset':
        'utf-8',
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 9; Mi Note 3 Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.62 XWEB/2691 MMWEBSDK/200901 Mobile Safari/537.36 MMWEBID/722 MicroMessenger/7.0.19.1760(0x27001335) Process/appbrand2 WeChat/arm64 NetType/WIFI Language/zh_CN ABI/arm64',
        'content-type':
        'application/json',
        'Accept-Encoding':
        'gzip,compress,br,deflate',
        'accept':
        'application/json',
        'app-version':
        '4.6.31',
        'timestamp':
        str(timestamp),
        'scene':
        '1106',
        'Referer':
        'https://servicewechat.com/wx4692f08fa6ad3bc2/371/page-frame.html'
    })
    return USER_INFO


global joinedCount
joinedCount = 0


def getBigLotteryListAndJoin():
    api = HOST + 'index?gzh_number=&type=0'
    response = get(api, headers=getHeaders(), verify=False)
    lotteryList = response.get('data', {}).get('recommend_welfare')
    if lotteryList is None:
        Logger.e('微信活动抽奖失败', '未获取到大抽奖列表')
    else:
        joinLoterryOneByOne(lotteryList)


def getSmallLotteryListAndJoin():
    api = HOST + 'index?gzh_number=&type=1'
    response = get(api, headers=getHeaders(), verify=False)
    lotteryList = response.get('data', {}).get('self_help_welfare')
    if lotteryList is None:
        Logger.e('微信活动抽奖失败', '未获取到大抽奖列表')
    else:
        joinLoterryOneByOne(lotteryList)


def joinLoterryOneByOne(lotteryList):
    unJoinList = list(
        filter(lambda lottery: lottery.get('joinStatus', True) != True,
               lotteryList)) or []
    if len(unJoinList) != 0:
        global joinedCount
        for item in unJoinList:
            time.sleep(3)
            id = item['id']
            if joinLotery(item['id']):
                joinedCount += 1


def joinLotery(productId):
    api = HOST + 'lotteries/' + productId + '/join'
    data = '{"template": "lGOfpVZAzg5VaoX761nwQAmtQ94-UssmZ4ARrnUXegY"}'
    response = post(api, headers=getHeaders(), data=data, verify=False)
    result = response.get('success', False)
    if result:
        return result
    else:
        Logger.e('微信活动抽奖抽奖' + productId + '失败',
                 response.get('message', {}).get('error'))
        return False


def joinWechatLottery2():
    global USER_INFO
    for user in USER_INFOS:
        USER_INFO = user
        Logger.v('微信活动抽奖抽奖开始:' + user['uid'])
        getBigLotteryListAndJoin()
        time.sleep(5)
        getSmallLotteryListAndJoin()
        global joinedCount
        Logger.v('微信活动抽奖' + user['uid'] +
                 '抽奖完毕:共成功参与{}次抽奖'.format(joinedCount))
        joinedCount = 0


if __name__ == "__main__":
    joinWechatLottery2()

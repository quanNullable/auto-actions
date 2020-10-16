from tools.path import addParentDir
addParentDir()
from public.fetch import post
from public.logger import Logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

global cookie
cookie = 'o3KV7W81C4e3mrG98jYPWrU8ZJKUyaqey1APSqHe6AqCceKDcQzbiWKtCK4X6BxbhaG96JYkPtPUBUCSieqAt3Y_0VlwKQyYAL58BSh7.LWyaBUdsFkXooBCFQjlqKJeBDw95grr0RzBhStFw7qw5ZMa3A18ERlrD_skDsdbQzUf.7F464wI_muCr0ROsB.jyHUHIAsRG9kcUFE0Er51C1thp7LJlZLLpxfasMHVE2j8L'


def getCookies():
    return {
        'NTES_YD_SESS':
        'TYAM.QOaEKLc36wgIzNf3629f7Y1JCiZu8kECjGYnH69DJLIDjktuVik3_h7dJJM1h4.I8gSIzOvdTVbPBHVxDfWWEfWp84xVtycq3hZTnvmlcA57cV0WfasmJnsgKRmj_CHsXWhQgerAbxRjua4gZmF5gpzlwkrVEr0YicUYm9yE0iA2puQcm14Ad1GGrsMelTa9QeG8SiLNJ_B3q4ZCv0x1',
        '_ga':
        'GA1.2.782529179.1519958400',
        'STAREIG':
        'bc2ed0e57a1b0c7d0cc78d549c34356c4d53a45f',
        'S_INFO':
        '1519958788|0|1&65##|m18671717521',
        'P_INFO':
        'm18671717521@163.com|1519958788|1|study|00&99|sxi&1517133016&mail163#hub&420100#10#0#0|186521&1||18671717521@163.com',
        '_ntes_nnid':
        '294f702b0d1891af8c6ada01e7d2c90f,1521071927517',
        '_ntes_nuid':
        '294f702b0d1891af8c6ada01e7d2c90f',
        '_ngd_tid':
        'vrizyq4tESdsyKLGHRtAxIeMncgN5bDI',
        'mail_psc_fingerprint':
        'd7004ec5777c97e999d8f57cb0a8813e',
        'UM_distinctid':
        '1658e273979387-0c28e0368534d7-56513d62-43113-1658e27397b231',
        'NTES_YD_SESS':
        cookie,
        'STAR_YD_SESS':
        cookie,
    }


headers = {
    'Host':
    'star.8.163.com',
    'Origin':
    'https://star.8.163.com',
    'Accept':
    'application/json, text/plain, */*',
    'User-Agent':
    'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 hybrid/1.0.0 star_client_info_begin {hybridVersion: "1.0.0",clientVersion: "1.9.0",accountId: "024ed4d78de15bc2cf623972b6dc77d26a752f5977eadbbcb91c9a4bff23c604",channel: "e01170023"}star_client_info_end',
    'Referer':
    'https://star.8.163.com/m',
    'Accept-Language':
    'zh-CN,en-US;q=0.9',
    'X-Requested-With':
    'XMLHttpRequest',
}


# 请求领取coin接口
def collectCoins(coinId):
    headers = {
        'Host':
        'star.8.163.com',
        'Accept':
        'application/json, text/plain, */*',
        'X-Requested-With':
        'XMLHttpRequest',
        'Accept-Language':
        'zh-cn',
        'Cache-Control':
        'max-age=0',
        'Content-Type':
        'application/json;charset=UTF-8',
        'Origin':
        'https://star.8.163.com',
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.91 Mobile Safari/537.36 hybrid/1.0.0 star_client_info_begin {hybridVersion: "1.0.0",clientVersion: "1.9.0",accountId: "024ed4d78de15bc2cf623972b6dc77d26a752f5977eadbbcb91c9a4bff23c604",channel: "e01170023"}star_client_info_end',
        'Referer':
        'https://star.8.163.com/m',
    }
    data = '{"id":%s}' % coinId
    response = post(
        'https://star.8.163.com/api/starUserCoin/collectUserCoin',
        headers=headers,
        cookies=getCookies(),
        data=data,
        verify=False)
    result = response['msg']
    if not '成功' in result:
        Logger.e('网易星球收取黑钻失败', result)
        return False
    return True


global retryTimes
retryTimes = 0


def autoCollectCoins():
    try:
        cheackToCollectCoins()
    except Exception as e:
        Logger.e('网易星球收取黑钻失败', e)


def cheackToCollectCoins():
    # 1、请求首页数据，检查是否有coin可以收集。有则将coin保存到列表容器
    response = post(
        'https://star.8.163.com/api/home/index',
        headers=headers,
        cookies=getCookies(),
        verify=False)
    if response['data'] is None:
        Logger.e('网易星球收取黑钻失败', response['msg'])
        if '登录失败' in response['msg']:
            Logger.n('网易星球登录失败', '可能为session过期')
            global retryTimes
            if retryTimes < 1:
                retryTimes += 1
                updateCookie()
                autoCollectCoins()
            else:
                retryTimes = 0
        return
    collectCoinsList = response['data']['collectCoins']
    if len(collectCoinsList) == 0:
        Logger.v('网易星球当前没有黑钻可收取')
    else:
        # 2、检查coin列表容器是否有值，遍历请求领取coin接口
        Logger.v('共有{}个黑钻可收取'.format(len(collectCoinsList)))
        count = 0.0
        for collectCoinsItem in collectCoinsList:
            if collectCoins(collectCoinsItem['id']):
                count += float(collectCoinsItem['virCount'])
        Logger.v('网易星球收取黑钻完毕,本次收取{}颗黑钻'.format(count))


def updateCookie():
    Logger.v('尝试自动更新网易星球cookie')
    data = '{"p":"WObwO2HPjFkkaaEjWgRG1EHmrIP/SOaQT+GMoThH609UM47CRGDYhD4YKQ5p6Gy4PvmcJwPszmWv8S/NerKjNI7ELqmlu5IlnxqGhyPjIHxe6LVMKe4EbJD2da8vRaR/E9Wrxqvrto6qCZsDDjWoH4Ul7Uqg/YP9gCmFJE2lnYmqNxLaRZ4s6i7m3EEt8Ew2vIc85P3XGVTT3hwV4ZMNylket04jcCCEXWJM5zZMJL2Y9Jg+TFu71C0vFMDu637L2ruD2zALKxs4tGdHC9EtT3e5Miwq+0GaJd+v0xL5bGInKW8QOSrQzrQOENeYRO7NF80xtlLu9bmyYtqpr6wS835BUxrn3hn6MV4EtR6NNNI\u003d","k":"Zoqzg9mEAOr3bo6N/Qp5T8+mBUZB5mv7iUzon1J0VcyvWAmCVWOh3/x6FCHNo/qIjV5qlTFnWJL7Fw8zynmevfGTdsIGmzrAD8QAQ5SySNJHujWvpQo51eEk4d5EyI/WWaGrUqx2VzswCQikqEER/UcG4Qo8A053HP8zHkVYu70\u003d"}'
    headers = {
        'user-agent':
        'Mozilla/5.0 (Linux; Android 8.1.0; Mi Note 3 Build/OPM1.171019.019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.112 Mobile Safari/537.36',
        'appmeta':
        'eyJhcHBWZXJzaW9uIjoiMS45LjYiLCJPUyI6IkFuZHJvaWRfMjkiLCJhcHBOYW1lIjoi5pif55CDIiwiY2hhbm5lbCI6ImUwMTE3MDAwNCIsImFudGlTcGFtSW5mbyI6IntcImRhdGF0eXBlXCI6XCJhaW10X2RhdGFzXCIsXCJpZF92ZXJcIjpcIkFuZHJvaWRfMS4wLjFcIixcInJkYXRhXCI6XCJqSkRHLzhFNmtWb0lZRjJ0UXJCajdBVHlHaFEvYVhON3RtdU9mUW16ek5SeUdyT2JPQVBLU0lwZUFpdFQwbXFaYURxcWtKck5GSmtmQmpaY3ZwZklGSjlmV1NaYThnVVBvaWhhZzVtSndTVXBvTkEwZWtqT0EwbVRKSEw0ZFZ2enBUd0RZT0FjU05oNThHWG9NaFVwOXVuODl1TGh1YytRS1gzWU41R1hxNW43bWR2aXVJRklhTVlGUzdoSXVnWFF5d3lZSFh2OXp1VEM0WG1mVzUvVHNIRUYwVlltd0hlNjY1SGxVaFZUdzhxaU4xRWU1ZmhoWG9xSC9MTm9ncTRVWk1TeFdkT3RacnFkOXB3SGN2bmZPazZ0TDdwUUhBV096L3VVNnk2VldVV2RCQjlwQUZRUUpIV3d6TGliVEpiOHpmS1ozb0VUOEIyTXU2enhBdUpMSTNIS1U5UEZzb2JhcUNXV2l3R1RKOFNmN1ZsekpWb0hvTkpreHMvSGU4ODdWMHRobFRXdzRzblBwT1B3SGtPdlN2Y3AvUzFVUEh5c1EyZmx1aEpGelV0S0F3dmJNL2IvbEpKcUM3ZVloeVdKN0VRQjRZS3lYVU5IQ2wwQmhHV2hEN04zb3p4Wm1yYkxXMjFZMEtaNTZSakw1YW8vd1ZIV0huTzQveGtDaUVZY3h5eW1DU2JXLzhEOTNYU2ZReVFMcXJDMGRKd1NGRTZHR1ByU3FucmlRcC93Z0dYT2lOWWhlTWlQZ2pubXV2eXFKOTRPSVZGYStTZTRuL3RJeVhaQlhRXHUwMDNkXHUwMDNkXCIsXCJya1wiOlwicDQ4U1AxankwY2RlWm4zYlFnSWJ0STBBa3IxQjVnU2c2NDlGWU5KNjR4YWRPSDZnNWxhS0NFQU9FSk5LZ25EZVNGMFUyNTI4NlhuZnJ5b3hyT2l6cVZQM1U5Ui9xcUxXakRUSnRJV3dXVjBiQnQwMFRpeG84dDZuQWJIaU5HaTBRL2lvQjRoQTdTaWhrMzB6NXVlN2VuMVYvNXZKajhZTWppa1FWcVcyM3lBXHUwMDNkXCJ9XG4iLCJtb2RlbCI6IlRBUy1BTjAwIiwicGFja2FnZU5hbWUiOiJjb20ubmV0ZWFzZS5ibG9ja2NoYWluIiwiYXBwVmVyc2lvbkNvZGUiOiIyNzkiLCJtYW51ZmFjdHVyZXIiOiJIVUFXRUkifQ==',
        'content-type':
        'application/json; charset=utf-8',
        'content-length':
        '610',
        'accept-encoding':
        'gzip'
    }
    response = post(
        'https://star.8.163.com/api/starUser/getCookie',
        data=data,
        headers=headers,
        verify=False)
    newCookie = response['data']['cookie']
    if not newCookie is None:
        global cookie
        cookie = newCookie
        Logger.v('已自动更新网易星球cookie:' + cookie)


if __name__ == "__main__":
    autoCollectCoins()

# -*- coding: utf-8 -*-
# 定时任务
import random,time
from tools.path import addParentDir
addParentDir()
from public.logger import Logger
from tasks.wangyiPlanet import autoCollectCoins
from tasks.baiduDog import autoCollect
from tasks.toutiaoLottery import autoLottery
from tasks.wechatLottery import joinWechatLottery

def startAllTasks():
    Logger.v('开始执行网易星球自动收取钻石')
    autoCollectCoins()
    return
    Logger.v('开始执行微信抽奖')
    joinWechatLottery()
    Logger.v('开始执行百度自动收元气')
    autoCollect()
    Logger.v('开始执行头条全民抽奖')
    autoLottery()

def startRun():
    Logger.v('准备运行定时任务')
    delay = random.randint(1, 600)
    Logger.v('{}秒后开始运行定时任务'.format(delay))
    # time.sleep(delay)
    startAllTasks()
    Logger.v('所有定时任务均已执行完毕')

if __name__ == '__main__':
    startRun()
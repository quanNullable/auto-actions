# -*- coding: utf-8 -*-
# 定时任务
import random
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
    Logger.v('开始执行微信抽奖')
    joinWechatLottery()
    Logger.v('开始执行百度自动收元气')
    autoCollect()
    Logger.v('开始执行头条全民抽奖')
    autoLottery()

if __name__ == '__main__':
    startAllTasks()
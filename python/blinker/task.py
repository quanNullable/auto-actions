# -*- coding: utf-8 -*-
# 定时任务
import random
from tools.path import addParentDir
addParentDir()
from public.config import getGeneralConfig
from public.logger import Logger
from apscheduler.schedulers.background import BackgroundScheduler
from tasks.wangyiPlanet import autoCollectCoins
from tasks.baiduDog import autoCollect
from tasks.toutiaoLottery import autoLottery
from tasks.wechatLottery import joinWechatLottery

config = getGeneralConfig()

scheduler = BackgroundScheduler()

job_ids = {}

def _startWangyiCollet(fromUser=False):  #网易星球自动收钻
    Logger.v('开始执行网易星球自动收取钻石')
    autoCollectCoins()
    if not fromUser:
        scheduler.remove_job(job_ids['_startWangyiCollet'])
        _addWangyiJob()

def _startBaiduCollet(fromUser=False):  #百度莱茨狗自动收元气
    Logger.v('开始执行百度自动收元气')
    autoCollect()
    if not fromUser:
        scheduler.remove_job(job_ids['_startBaiduCollet'])
        _addBaiduJob()

def _startToutiaoLottery(fromUser=False):  #头条全民抽奖
    Logger.v('开始执行头条全民抽奖')
    autoLottery()
    if not fromUser:
        scheduler.remove_job(job_ids['_startToutiaoLottery'])
        _addTouTiaoJob()

def _startWechatLottery(fromUser=False):  #微信各种小程序抽奖
    Logger.v('开始执行微信抽奖')
    joinWechatLottery()
    if not fromUser:
        scheduler.remove_job(job_ids['_startWechatLottery'])
        _addWechatJob()

def _startLotteries(fromUser=False):
    _startWangyiCollet(fromUser)
    _startBaiduCollet(fromUser)
    _startToutiaoLottery(fromUser)
    _startWechatLottery(fromUser)


def _addWangyiJob():
    job_ids['_startWangyiCollet'] = scheduler.add_job(
        func=_startWangyiCollet,
        trigger='cron',
        day_of_week='0-6',
        hour=random.randint(8, 22),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)  #每天8-22点随机时刻收取网易星球黑钻
    ).id

def _addBaiduJob():
    job_ids['_startBaiduCollet'] = scheduler.add_job(
        func=_startBaiduCollet,
        trigger='cron',
        day_of_week='0-6',
        hour=random.randint(8, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)  #每天8-23点随机时刻收取百度元气
    ).id

def _addTouTiaoJob():
    job_ids['_startToutiaoLottery'] = scheduler.add_job(
        func=_startToutiaoLottery,
        trigger='cron',
        day_of_week='0-6',
        hour=random.randint(10, 22),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)  #每天8-23点随机时刻参与头条抽奖
    ).id

def _addWechatJob():
    job_ids['_startWechatLottery'] = scheduler.add_job(
        func=_startWechatLottery,
        trigger='cron',
        day_of_week='0-6',
        hour=random.randint(8, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)  #每天8-22点随机时刻参与微信抽奖
    ).id

def startTasks():
    _addWangyiJob()
    _addBaiduJob()
    _addTouTiaoJob()
    _addWechatJob()
    
    scheduler.start()


def getJobs():
    # scheduler.print_jobs()
    jobs = scheduler.get_jobs()
    text = ''
    if len(jobs):
        text = '共{}个任务:\n'.format(len(jobs))
        for job in jobs:
            text += str(job) + '\n\n'
    else:
        text = '暂无任务'
    return text

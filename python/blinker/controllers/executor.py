# -*- coding: utf-8 -*-
# 命令执行器 具体命令执行

import time, threading, shutil, subprocess, os
from comands import ALL_COMANDS
from tools.path import addParentDir
addParentDir()
from public.logger import Logger
from tools.ip import getIPs
from tools.notice import sendTextMsg
import task

def executCommand(command):
    if command.Name == ALL_COMANDS[0].Name: #获取ip
        result = getIPs()
    elif command.Name == ALL_COMANDS[1].Name: #执行代码
        threading.Thread(
            target=_executeShell,
            args=(command.Parmas,)).start()
        result = '已开始执行'
    elif command.Name == ALL_COMANDS[2].Name:  #命令帮助
        result = _getCommandsHelp()
    elif command.Name == ALL_COMANDS[3].Name:  #任务详情
        result = task.getJobs()
    elif command.Name == ALL_COMANDS[4].Name:  #立即执行任务
        result = _runTaskRightNow()
    else:
        result = '暂未完成'
    Logger.v('命令<' + command.Name + '>执行结果<' + str(result) + '>')
    return result


def _executeShell(command):
    status, output = subprocess.getstatusoutput(command)
    result = ('执行成功:\n' if status == 0 else '执行失败:\n') + output
    sendTextMsg(result)


def _runTaskRightNow(funcName):
    func = getattr(task, funcName,None)
    if func is None:
        sendTextMsg('未找到指定任务')
    else:
        if callable(func):
            Logger.v('开始执行' + funcName)
            func(True)
        else:
            Logger.e(func + '无法执行','not callable')

def _getCommandsHelp():
    def formatCommands(commands):
        descs = []
        for comand in commands:
            desc = '命令:'+comand.Name+'\n'+\
            '作用:'+comand.Func+'\n'+\
            '用法:'+comand.Usage+'\n'
            descs.append(desc)
        return '\n'.join(descs)  
    commandsCount = len(ALL_COMANDS)
    if commandsCount == 0:
        return '暂无可用命令'
    else:
        return formatCommands(ALL_COMANDS)

def _runTaskRightNow(user, funcName):
    func = getattr(task, funcName,None)
    if func is None:
        sendTextMsg(user.Id, '未找到指定任务')
    else:
        if callable(func):
            Logger.v('开始执行' + funcName)
            func(True)
        else:
            Logger.e(func + '无法执行','not callable')

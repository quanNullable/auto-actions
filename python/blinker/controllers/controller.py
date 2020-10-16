# -*- coding: utf-8 -*-
# 主控制器,所有的命令经由这里分发 做执行前的判断和拦截(用法及权限判断)

import time
from comands import findComandByStr
from controllers.executor import executCommand
from tools.path import addParentDir
addParentDir()
from public.logger import Logger


def handText(text):
    # print('命令:',text)
    Logger.v('收到文本消息<' + text + '>')
    command = findComandByStr(text.strip())
    if command is None:
        result = '未找到命令:<' + text + '>'
    elif isinstance(command, str):
        result = '<' + text + '>' + command
    else:
        # print('找到命令:',command)
        Logger.v('执行命令<' + command.Name + '>,参数<' +
                 (str(command.Parmas) or '无') + '>')
        result = '<' + text + '>' + str(executCommand(command))
    return result



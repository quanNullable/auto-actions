# -*- coding: utf-8 -*-
# 所有的命令

import copy,time
from tools.path import addParentDir
addParentDir()
from public.logger import Logger
from public.baseObject import BaseObject

class Command(BaseObject):
      def __init__(self, **info):
          if 'name' in info:#命令名
             self.Name = info['name']
          if 'func' in info:#命令作用
             self.Func = info['func']
          if 'usage' in info:#命令用法
             self.Usage = info['usage']
          if 'parmas' in info:#命令参数,None 无参数  STR 字符串参数  DIC 字典类参数 含有NONE字段的为参数可空
             self.Parmas = info['parmas']
          if 'default' in info:#默认参数
             self.Default = info['default']
          else:
             self.Default = None


global ALL_COMANDS
ALL_COMANDS = [
   Command(name='获取ip',func='获取服务器的IP地址',usage='获取ip',parmas=None),
   Command(name='执行代码',func='在命令终端中执行相应的代码',usage='执行代码:XXX',parmas='STR'),
   Command(name='帮助',func='获取命令帮助及用法',usage='帮助',parmas=None),
   Command(name='任务详情',func='获取定时任务的详细情况',usage='任务详情',parmas=None),
   Command(name='执行任务',func='立即执行指定的定时任务',usage='执行任务:name=xxx',parmas='DIC'),
]

def findComandByStr(text):#根据用户输入尝试解析出对应命令
    args = text.split(":",1)  # 参数以:为分割符
    if len(args) == 1:
       args = text.split("：",1)  # 再尝试参数以：为分割符
    comandName = args[0].strip()#命令名
    global ALL_COMANDS
    commandList = list(filter(lambda com:com.Name == comandName, ALL_COMANDS))
    result = None
    if len(commandList) != 0:#找到了该命令
       comand = copy.deepcopy(commandList[0])
       if comand.Parmas == None:
          result = comand
       elif "STR" in comand.Parmas:#字符串型参数
          if len(args) > 1:#有参数命令,需解码参数
             comand.Parmas = args[1].strip()
             result = comand
          elif not comand.Default is None:
             comand.Parmas = comand.Default
             result = comand
       elif "DIC" in comand.Parmas:#字典型参数
            if len(args) > 1:#有参数命令,需解码参数
               try:
                  parmasList = args[1].split(",")
                  data={}
                  for parma in parmasList:
                     keyValue = parma.split("=")
                     key = keyValue[0].strip() 
                     value = keyValue[1].strip() 
                     data[key]=value
                  comand.Parmas = data
                  result = comand
               except Exception as e:
                  Logger.e('命令参数解析失败', e)
            elif not comand.Default is None:
               comand.Parmas = comand.Default
               result = comand
       else:
          result = comand
       if result is None:
          if "NONE" in comand.Parmas:
             comand.Parmas = None
             result = comand
          else:
             result = '参数错误,用法:\n'+comand.Usage
       return result
    else:
      #   print('未找到指定命令')
        return None



if __name__ == "__main__":
    comand = findComandByStr('a:(abc123,bcd456)')
    if comand is None:
       print('未找到命令')
    elif isinstance(comand, str):
       print('参数错误:',comand)
    else:
       print('找到命令:',comand)


       
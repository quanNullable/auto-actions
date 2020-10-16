# -*- coding: utf-8 -*-
# 主入口

import os
import controllers.controller as controllers
import task


if __name__ == '__main__':
    # os.system(
    # 			"""
    # 				osascript -e 'display notification "{0}" with title "{1}"'
    # 			""".format('你好啊', '测试下')
    # 		  )
    #    text = input('请输入命令\n')
    #    result = controllers.handImage("http://yun.itheima.com/Upload/Images/20170614/594106ee6ace5.jpg",MANAGER)
      #  result = controllers.handVoice("帮助",MANAGER)
      #  result = controllers.handText("发微信:to=老板,text=啊哈",MANAGER)
      #  result = controllers.handText("小爱同学：叫爸爸",MANAGER)
      #  print('result:',result)
      #  result = controllers.handText("执行任务:name=_startLotteries")
       result = controllers.handText("查看日志")
       print('result',result)
      # autoFollow()
    # task.startTasks()
    # print(task.getJobs())
# -*- coding: utf-8 -*-
# 日志系统

import traceback, time

def _getTime():
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    
class Logger:
    def __init__(self):
        pass

    @staticmethod
    def e(title, detail):
        if isinstance(detail, str):
            print(_getTime(),'ERROR!!!',"<" + title + '>:' + detail)
        elif isinstance(detail, Exception):
            print(_getTime(),'ERROR!!!',"<" + title + '>', traceback.format_exc())
        else:
            print(_getTime(),'ERROR!!!',"<" + title + '>:' + str(detail))

    @staticmethod
    def v(detail):
        print(_getTime(),detail)

    @staticmethod
    def n(title, content):
        """
        此方式为最高级别警告,将触发系统通知
        """
        if isinstance(content, str):
            content=content
        elif isinstance(content, Exception):
            content = content.__str__()
        else:
            content = str(content)
        print(_getTime(),'IMPORTANT!!!',"<" + title + '>:' + content)
        import tools.notice.noticeManager as noticeManager
        noticeManager.sendNotice(title + ':' + content)


if __name__ == '__main__':
    Logger.n('警告', '程序停止运行')

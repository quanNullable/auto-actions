# -*- coding: utf-8 -*-
# 日志系统

import os, logging, time, datetime
try:
   from config import getGeneralConfig
except Exception:
   from .config import getGeneralConfig
import Blinker

LOG_LEVEL = {
    'verbose': 0,  #都记录
    'error': 1,  #只记录错误
    'off': 2,  #关闭日志记录
}
config = getGeneralConfig()
logLevel = LOG_LEVEL[config['log_level'] or 'verbose']
path = config['log_path']

logFormatter = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO, format=logFormatter, datefmt="[%Y-%m-%d %H:%M:%S]")


def _GetLogPath():
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def getLogger(saveToFile=False):
    logger = logging.getLogger('{}'.format(int(time.time())))
    if saveToFile and not logger.handlers:
        logName = _GetLogPath() + time.strftime("%Y-%m-%d") + '.log'
        handler = logging.FileHandler(logName)
        handler.setFormatter(logging.Formatter(logFormatter))
        logger.addHandler(handler)
    return logger

class Logger:
    def __init__(self):
        pass

    @staticmethod
    def e(command, detail):
        logger = getLogger(LOG_LEVEL['error'] >= logLevel)
        if isinstance(detail, str):
            logger.error("<" + command + '>:' + detail)
        elif isinstance(detail, Exception):
            logger.error("<" + command + '>', exc_info=True)
        else:
            logger.error("<" + command + '>:' + str(detail))
        blinker('ERROR:'+str(detail))

    @staticmethod
    def v(detail):
        logger = getLogger(LOG_LEVEL['verbose'] >= logLevel)
        logger.info(detail)
        blinker(detail)

    @staticmethod
    def n(title, content):
        """
        此方式为最高级别警告,将触发系统通知
        """
        logger = getLogger(True)
        if isinstance(content, str):
            content=content
        elif isinstance(content, Exception):
            content = content.__str__()
        else:
            content = str(content)
        logger.warning('\n!!!重要!!!\n' + title + ':' + content,exc_info=True)
        import tools.notice.noticeManager as noticeManager
        noticeManager.sendNotice(title + ':' + content)
        blinker('NOTICE:'+title + ':' + content)

def blinker(text):
    try:
        Blinker.print(text)
    except Exception as e:
        pass

if __name__ == '__main__':
    Logger.n('警告', '程序停止运行')

#encoding:utf-8
#解析配置文件
import configparser
try:
   from baseObject import BaseObject
except Exception:
   from .baseObject import BaseObject

global config
config = None

class Config(BaseObject):
    def __init__(self):
        conf = configparser.RawConfigParser()
        conf.read('python/public/config.conf')
        sections = conf.sections()
        self.configs = {}
        for section in sections:
            self.configs[section]={}
            items = conf.items(section)
            for item in items:
                self.configs[section][item[0]] = item[1]

def getManagerInfo():
    return getConfig().configs['manager']

def getGeneralConfig():
    return getConfig().configs['general']

def getEmailConfig():
    return getConfig().configs['email']

def getSmsConfig():
    return getConfig().configs['sms']

def getVoiceConfig():
    return getConfig().configs['voice']

def getCosConfig():
    return getConfig().configs['cos']
    
def getConfig():
    global config
    if config is None:
       config = Config()
    return config

if __name__ == "__main__":
    print(getSmsConfig())

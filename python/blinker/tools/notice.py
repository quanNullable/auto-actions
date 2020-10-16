from Blinker import Blinker

def sendTextMsg(text):
    Blinker.push(text)
    Blinker.print(text)

def sendNotice(text): 
    Blinker.wechat(text)


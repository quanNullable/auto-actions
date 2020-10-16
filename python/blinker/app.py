from Blinker import Blinker, BlinkerButton
from tools.path import addParentDir
addParentDir()
from public.config import getGeneralConfig
from public.logger import Logger
import controllers.controller as controllers

blinkerId = getGeneralConfig()['blinker_id']
Blinker.mode("BLINKER_WIFI")
Blinker.begin(blinkerId)

buttonRestart = BlinkerButton("btn-restart")


def restart_callback(state):
    buttonRestart.print(state)
    Blinker.print('result:' + state)


def data_callback(data):
    if isinstance(data, str):
        result = controllers.handText(data)
    elif isinstance(data, dict):
        result = str(data)
    else:
        result = "无法识别命令"
    Blinker.print(result)


buttonRestart.attach(restart_callback)
Blinker.attachData(data_callback)
Logger.v("Blinker启动成功!")

if __name__ == '__main__':
    while True:
        Blinker.run()
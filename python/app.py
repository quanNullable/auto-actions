from Blinker import Blinker, BlinkerButton
import os

blinkerId = os.environ["BLINKER_ID"]
Blinker.mode("BLINKER_WIFI")
Blinker.begin(blinkerId)

buttonRestart = BlinkerButton("btn-restart")

def restart_callback(state):
    buttonRestart.print(state)
    Blinker.print('result:'+state)
    

def data_callback(data):
    Blinker.print('收到:'+data)

buttonRestart.attach(restart_callback)
Blinker.attachData(data_callback)

if __name__ == '__main__':
    while True:
        Blinker.run()
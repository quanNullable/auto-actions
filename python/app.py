from Blinker import Blinker, BlinkerButton
import os

blinkerId = 'a1903d20dcb6'
Blinker.mode("BLINKER_WIFI")
Blinker.begin(blinkerId)
print(os.environ["BLINKER_ID"])
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
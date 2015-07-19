from arduino_host import ArduinoHost
from time import sleep

rotobot = ArduinoHost('COM7')
rotobot.servo(30)
sleep(1)
rotobot.servo(130)
sleep(1)
rotobot.servo(30)
rotobot.step(1000)
rotobot.step(-1000)

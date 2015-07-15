#!/cygdrive/c/Anaconda/python
import serial
import sys
import time
import io
class ArduinoHost:
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600)
        time.sleep(2);
        #line= self.ser.readline()
        #print line
        sys.stdout.flush()
    def servo(self, absolute_position):
        self.ser.write("v%d\n" % absolute_position)
        line = self.ser.readline()
        print line,
        sys.stdout.flush()
    def step(self, num_steps):
        self.ser.write("s%d\n" % num_steps)
        line = self.ser.readline()
        print line,

if (__name__ == '__main__'):
    import argparse
    parser = argparse.ArgumentParser("Control the rotobot")
    parser.add_argument("-v", help="go to servo position" , type=int, nargs='+')
    parser.add_argument("-s", help="step this many steps.", type=int, nargs='+')
    args = parser.parse_args()
    if (args.v or args.s):
        arduino = ArduinoHost("COM5")

    if (args.v):
        for v in args.v:
            arduino.servo(v)
            time.sleep(2)
    if (args.s):
        for s in args.s:
            arduino.step(s)
            time.sleep(10)


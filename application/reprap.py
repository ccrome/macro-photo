#!/cygdrive/c/Anaconda/python
import serial
import time
from sys import stdout
import threading
import Queue

def debug_message(message):
    print "DEBUG: %s" % message
    stdout.flush()
    pass

def chk(s):
    cs = 0
    l = len(s)
    for i in range(l):
        c = ord(s[i])
        cs = cs ^ c
    cs = cs & 0xFFf
    return cs

class RepRap:
    def __init__(self, port, baud=230400, feed_x = 100, feed_y = 100, feed_z = 100):
        self._ser = serial.Serial("COM4", 230400, timeout=1)
        time.sleep(2)
        self.slurp_lines()
        self.feed_x = float(feed_x)
        self.feed_y = float(feed_y)
        self.feed_z = float(feed_z)
        self.tx_queue = Queue.Queue()
        self.rx_queue = Queue.Queue()
        self.ack_received = threading.Event()
        self.tx_line_number = 1
        self.rx = threading.Thread(target=self.rxThreadWorker)
        self.tx = threading.Thread(target=self.txThreadWorker)
        self.keepalive = threading.Thread(target=self.keepalive_worker)
        
        self.request_quit = False
        debug_message("starting threads")
        self.rx.start()
        self.tx.start()
        debug_message("setup")
        self.setup()
        debug_message("setup complete")
        #self.keepalive.start()
        
    def send(self, command):
        debug_message("Enquing: %s" % command)
        self.tx_queue.put(command)
        
    def slurp_lines(self):
        while True:
            line = self._ser.readline()
            line = line.rstrip()
            if line == '':
                break
            else:
                print line
            stdout.flush()
        debug_message("slurp done")

    def keepalive_worker(self):
        while not self.request_quit:
            self.enable_steppers()
            time.sleep(1)
            
    def rxThreadWorker(self):
        try:
            while (not self.request_quit or
                   not self.tx_queue.empty()):
                rx = self._ser.readline()
                if (len(rx) > 0):
                    rx = rx.rstrip()
                    #print "rx = %s" % rx
                    print "%s" % rx
                    stdout.flush()
                    if (rx.lower() == 'ok'):
                        self.ack_received.set()
                        debug_message("received ok, setting ack")
                else:
                    pass
                    #debug_message("read timeout")
        except Exception as e:
            debug_message("Got an exception in rxThreadWorker" % e)
        self.ack_received.set() # Send it just in case the tx is waiting.
        debug_message("Rx Thread Complete")
    def txThreadWorker(self):
        try:
            while (not self.request_quit or
                   not self.tx_queue.empty()):
                stdout.flush()
                try:
                    item = self.tx_queue.get(block=True, timeout=1)
                    tosend = "N%d %s " % (self.tx_line_number, item)
                    cs = chk(tosend)
                    tosend = "%s*%d\n" % (tosend, cs)
                    print "sending %s" % tosend,
                    stdout.flush()
                    self.ack_received.clear()
                    self._ser.write(tosend)
                    debug_message("write:  waiting for ack.")
                    self.ack_received.wait() # Wait for 'ok' from rx thread.
                    self.tx_queue.task_done()
                    self.tx_line_number = self.tx_line_number + 1
                except Queue.Empty:
                    pass
        except Exception as e:
            debug_message("got and exception in txThreadWorkder %s", e)
        debug_message("Tx Thread Complete")
            
    def setup(self):
        self.send("G21")  # set to millimeters
        self.send("G91")  # relative 
        time.sleep(.5)

        
    def enable_steppers(self):
        self.send("M17")  # enable steppers
        
    def disable_steppers(self):
        self.send("M18")  # disable steppers
        
    def go_x_rel(self, distance):
        if distance == 0:
            return
        self.send("G1 X%f F%f" % (distance, self.feed_x))
        sleepytime = (float(distance) / self.feed_x ) * 60
        
        time.sleep(sleepytime)
        
    def go_y_rel(self, distance):
        if distance == 0:
            return
        self.send("G1 Y%f F%f" % (distance, self.feed_y))
        sleepytime = (float(distance) / self.feed_x ) * 60
        time.sleep(sleepytime)
        
    def go_z_rel(self, distance):
        if distance == 0:
            return
        self.send("G1 Z%f F%f" % (distance, self.feed_z))
        sleepytime = (float(distance) / self.feed_x ) * 60
        time.sleep(sleepytime)

    def quit(self):
        self.request_quit = True
        #self.keepalive.join()
        self.disable_steppers()
        self.rx.join()
        stdout.flush()
        self.tx.join()
        stdout.flush()

if (__name__ == '__main__'):
    import argparse
    parser = argparse.ArgumentParser("Send commands to your printer.")
    parser.add_argument("-x", type=float, nargs=1, help="Move in x (mm)")
    parser.add_argument("-y", type=float, nargs=1, help="Move in y (mm)")
    parser.add_argument("-z", type=float, nargs=1, help="Move in z (mm)")
    parser.add_argument("--port", type=str, default="COM4", nargs=1, help="Serial port.  Defaults to COM4")
    args = parser.parse_args()

    rr = RepRap(args.port[0])
    debug_message( repr(args))
    time.sleep(1)
    debug_message("x")
    if args.x:
        rr.go_x_rel(args.x[0])
    debug_message("y")
    if args.y:
        rr.go_y_rel(args.y[0])
    debug_message("z")
    if args.z:
        rr.go_z_rel(args.z[0])
    debut_message( "moves complete")
    rr.quit()

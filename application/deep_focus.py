#!/cygdrive/c/Anaconda/python
import time
import gphoto
import reprap
import sys
from sys import stdout

def debug_message(message):
    print "DEBUG: %s" % message
    stdout.flush()
    pass



class DeepFocusMacro:
    def __init__(self, reprap_com_port, gphoto_location, photo_directory, delay_after_moving = 0):
        self.rr = reprap.RepRap(reprap_com_port)
        self.gp = gphoto.Gphoto(gphoto_location, photo_directory)
        self.delay_after_moving = delay_after_moving
        
    def scan(self, x_stepsize=1, x_distance=0, y_stepsize=1, y_distance=0, z_stepsize=.1, z_distance=0):
        debug_message("starting scan")
        x = 0
        y = 0
        z = 0
        x_steps = int(round(float(x_distance) / x_stepsize))  +1
        y_steps = int(round(float(y_distance) / y_stepsize))  +1
        z_steps = int(round(float(z_distance) / z_stepsize))  +1
        #debug_message("%s % %s" % (x_steps, y_steps, z_steps))
        debug_message("scan start")
        for ys in range(y_steps):
            for xs in range(x_steps):
                for zs in range(z_steps):
                    id = "%05f_%05f_%05f" % (x, y, z)
                    time.sleep(self.delay_after_moving)
                    debug_message("taking photo %s" % id)
                    self.gp.take_photo(id)
                    self.rr.go_z_rel(z_stepsize)
                    z = z + z_stepsize
                    time.sleep(1)
                self.rr.go_z_rel(-z_stepsize*z_steps)
                self.rr.go_x_rel(x_stepsize)
                x = x + x_stepsize
            self.rr.go_x_rel(-x_stepsize*x_steps)
            self.rr.go_y_rel(y_stepsize)
            y = y + y_stepsize
        self.rr.go_y_rel(y_stepsize*y_steps)
        debug_message("scan complete")
    def quit(self):
        self.rr.quit()
        
df = DeepFocusMacro("COM4", "c:\\progs\\gphoto2", "photos_fly_3", delay_after_moving=4)
print "going to start scan."
try:
    df.scan(z_stepsize=.2, z_distance=6)
except Exception as e:
    print e
df.quit()


#gp.take_photo("%07d" % 1)
#gp.take_photo("%07d" % 2)
#gp.take_photo("%07d" % 3)
#gp.take_photo("%07d" % 4)
#rr.send("G1 Z-100")
#rr.send("G1 X10") 
#rr.send("G1 X-10")
#time.sleep(10)
#rr.quit()

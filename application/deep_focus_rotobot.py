#!/cygdrive/c/Anaconda/python
import time
import gphoto
import arduino_host
import sys
from sys import stdout

def debug_message(message):
    print "DEBUG: %s" % message
    stdout.flush()
    pass



class DeepFocusMacro:
    def __init__(self, rotobot_com_port, gphoto_location, photo_directory, delay_after_moving = 0):
        self.rb = arduino_host.ArduinoHost(rotobot_com_port)
        self.gp = gphoto.Gphoto(gphoto_location, photo_directory)
        self.delay_after_moving = delay_after_moving
        
    def scan(self,
             servo_steps,     # Count of steps to take on the servo
             servo_start,     # Servo start position
             servo_stepsize,  # angle of servo step.
             stepper_steps,   # number of steps to send to the stepper on each angle change
             stepper_angles   # the number of angles to photograph
    ):
        current_angle = 0
        debug_message("starting scan")
        for angle in range(stepper_angles):
            for step in range(servo_steps):
                id = "%03d/nef/%03d_%03d" % (angle, angle, step)
                time.sleep(self.delay_after_moving)
                debug_message("taking photo %s" % id)
                self.rb.servo(servo_start+(step*servo_stepsize))
                self.gp.take_photo(id)
                debug_message("next step")
            self.rb.step(stepper_steps)
            current_angle = current_angle+stepper_steps
            debug_message("next angle")
        debug_message("scan complete")
        self.rb.servo(30)
        self.rb.step(-current_angle)
    def quit(self):
        pass


if __name__ == '__main__':

    import argparse
    import sys
    def get_args():
        parser = argparse.ArgumentParser("Run the deep focusing rotobot.")
        parser.add_argument("angles", help="the number of angles to capture in the specified rotation angle", type=int)
        parser.add_argument("output_dir", help="output directory")
        parser.add_argument("--arduino-com-port", help="Arduino com port.  Defaults to COM5", type=str, default='COM5')
        parser.add_argument("--gphoto-location", help="Gphoto location.  defaults to c:\\progs\\gphoto2", default="c:\\progs\\gphoto2")
        parser.add_argument("--servo-start", help="servo start angle.  default is 30.", type=int, default=30)
        parser.add_argument("--servo-end", help="servo stop angle.  Default 130.", type=int, default=130)
        parser.add_argument("--servo-steps", help="Number of steps for the servo to take between servo_start and servo_end, default=10", default=25, type=int)
        parser.add_argument("-d", "--stepper-total-degrees", help="Number of degrees to take the photos over.  default is 360.", default=360, type=float)
        parser.add_argument("--delay-after-moving", help="Time (in seconds) to delay after moving the rotobot to let things settle.  Default is 1.0", type=float, default=1.0)
        return parser.parse_args()

    args          = get_args()
    angles        = args.angles 
    servo_start   = args.servo_start
    servo_end     = args.servo_end
    servo_steps   = args.servo_steps

    df = DeepFocusMacro(rotobot_com_port   = args.arduino_com_port,
                        gphoto_location    = args.gphoto_location,
                        photo_directory    = args.output_dir,
                        delay_after_moving = args.delay_after_moving)

    servo_dist    = servo_end-servo_start
    steps_per_rev = 64*32
    servo_stepsize = int(servo_dist/servo_steps)
    stepper_steps = int(2048.0 * args.stepper_total_degrees / 360 / angles)
    print "going to start scan, hit ENTER when ready."
    try:
        df.rb.servo(30)
        df.scan(servo_steps    = servo_steps,
                servo_start    = servo_start,
                servo_stepsize = servo_stepsize,
                stepper_steps  = stepper_steps,
                stepper_angles = angles,
        )
    except Exception as e:
        print e

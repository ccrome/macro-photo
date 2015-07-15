#!/cygdrive/c/Anaconda/python
import subprocess
import os
import shutil

class Gphoto:
    def __init__(self, gphoto_dir, photo_dir):
        self.gphoto_dir = gphoto_dir
        self.photo_dir = photo_dir
        self.gphoto = "%s\\%s" % (gphoto_dir, "gphoto2.exe")
        self.env = {"CAMLIBS" : "%s\\camlibs" % self.gphoto_dir,
                    "IOLIBS"  : "%s\\iolibs"  % self.gphoto_dir,
                    "CYGWIN"  : "nodosfilewarning",
        }
        
    def take_photo(self, photo_identifier_string, tries = 10):
        while tries > 0:
            cmd = [self.gphoto, "--capture-image-and-download", "--force-overwrite"]
            env = self.env
            sub =  subprocess.Popen(cmd, env=env, shell=False)
            sub.wait()
            err = sub.returncode
            tries = tries - 1
            if err:
                print "RETRY PHOTO"
            else:
                #Move the photo into the right place, with the right name
                fname = "%s/%s.nef" % (self.photo_dir, photo_identifier_string)
                pathname=os.path.dirname(fname)
                try:
                    os.makedirs(pathname)
                except WindowsError:
                    pass # okay if it already exists.
                
                shutil.copy("capt0000.nef", fname)
                break

if (__name__ == '__main__'):
    import argparse
    parser = argparse.ArgumentParser("Take photos from camera.")
    parser.add_argument("FILENAME", nargs='?', help="Output file name")
    args = parser.parse_args()
    if (args.FILENAME == None):
        filename="test_photo"
    else:
        filename=args.FILENAME
    gp = Gphoto("c:\\progs\\gphoto2", ".")
    gp.take_photo(filename)

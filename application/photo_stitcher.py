#!/cygdrive/c/Anaconda/python
import glob
import subprocess
import sys
class PhotoStitcher:
    def __init__(self, hugin_dir):
        self.directory = hugin_dir
    def align(self, file_list, output_prefix, threads=2, gpu=False):
        cmd = [
            "%s/align_image_stack.exe" % self.directory,
            "-m",
            "--threads=%d" % threads,
            "-a", output_prefix]
        if gpu:
            cmd.append("--gpu")
        cmd.extend(file_list)
        subprocess.call(cmd)

    def stitch(self, file_list, output_file):
        cmd = [
            "%s/enfuse.exe" % self.directory,
            "--exposure-weight=0",
            "--saturation-weight=0",
            "--contrast-weight=1",
            "--hard-mask",
            "--output=%s" % output_file,
            ]
        cmd.extend(file_list)
        print cmd
        sys.stdout.flush()
        subprocess.call(cmd)


if (__name__=='__main__'):
    import argparse
    ps = PhotoStitcher('c:/Program Files/Hugin/bin')

    parser = argparse.ArgumentParser("Align and stitch photos")
    parser.add_argument("-a", "--align", action='store_true', help="Align a set of photos.")
    parser.add_argument("-s", "--stack", action='store_true', help="stack a set of aligned photos")
    parser.add_argument("-o", "--output", type=str, required=True, nargs=1, help="output file or directory.  Since align produces a bunch of photos, give a directory name.  Stack outputs a single file, so specify the file name.")
    parser.add_argument("input_files", nargs='+', type=str, help="List of input files")
    args = parser.parse_args()

    if args.align:
        print "Aligning photos... This can take a while."
        sys.stdout.flush()
        ps.align(file_list = args.input_files, output_prefix=args.output[0])
    elif args.stack:
        print "Stacking photos... This can take a while, but less time than aligning"
        ps.stitch(file_list = args.input_files, output_file = args.output[0])
    else:
        print "You must specify either the --stack or the --align argument"
        exit(-1)
        
#ps.align(file_list = glob.glob("photos/*.jpg"),
#         output_prefix =      "workdir/0.000000_0.000000_")
#ps.stitch(file_list = glob.glob("workdir/*.tif"), output_file = "the_fly.tif")




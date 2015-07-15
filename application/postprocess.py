#!/cygdrive/c/Anaconda/python
import fnmatch, os, glob
import argparse
import subprocess
import sys
def convert(input_dir, output_dir):
    input_files = fnmatch("%s/*.nef", input_dir)
    print input_files


def get_args():
    parser = argparse.ArgumentParser("Post process the .nef files taken in a sequence")
    parser.add_argument("-i", "--input-dir", type=str, help="input dir of .nef files. defaults to ./nef", default="./nef")
    parser.add_argument("-o", "--output-dir", type=str, help="output dir of .tif files, defaults to ./tif", default="./tif")
    args = parser.parse_args()
    return args


args = get_args()
nefs = glob.glob("%s/*.nef" % args.input_dir)
tifs = list()
for nef in nefs:
    root, ext = os.path.splitext(nef)
    d, basename = os.path.split(root)
    dd, nefdir = os.path.split(d)
    newdir = "%s/%s" % (dd, args.output_dir)
    newname="%s/%s.tif" % (newdir, basename)
    try:
        os.makedirs(newdir)
    except WindowsError:
        pass # ignor error about making already extant dir.

    in_f = os.path.relpath(os.path.realpath(nef))    .replace("\\", "/")
    out_f =os.path.relpath(os.path.realpath(newname)).replace("\\", "/")
    if not os.path.isfile(out_f):
        cmd = ["convert", in_f, out_f]
        try:
            os.makedirs(args.output_dir)
        except WindowsError:
            pass
        print "%s -> %s" % (in_f, out_f)
        sys.stdout.flush()
        subprocess.call(cmd, shell=True)
    tifs.append(out_f)


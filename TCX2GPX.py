from modules.TCXFile import TCXFile
import argparse
from termcolor import colored
import os
from modules.TCX2GPXConverter import convert_to_gpx_file

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--inpath", type=str, help="Path to the file or files. Can be a single file ending in .tcx or directory")
    parser.add_argument("-op", "--outpath", type=str, help="Output directory path")

    args = parser.parse_args()

    inpath = args.inpath
    outpath = args.outpath
    singlefile = inpath.endswith(".tcx")

    if singlefile:
        print(colored(f'Converting: {inpath}', 'green'))
        tcx = TCXFile(inpath)
        filename = os.path.normpath(inpath)
        filename = inpath.split(os.sep)[-1]
        filename = filename.replace('.tcx', '.gpx')
        convert_to_gpx_file(tcx, os.path.join(outpath, filename))
    else:
        files = os.listdir(inpath)
        if not os.path.exists(outpath):
            os.mkdir(outpath)
        for file in files:
            print(colored(f'Converting: {file}', 'green'))
            tcx = TCXFile(os.path.join(inpath, file))
            filename = file.replace('.tcx', '.gpx')
            convert_to_gpx_file(tcx, os.path.join(outpath, filename))
import os
import re
import argparse
import sys
import warnings
from os.path import join
from signal import signal, SIGINT, SIG_DFL

from detect_fake_videos import test_full_image_network

def warn(*args, **kwargs):
    pass

warnings.warn = warn

def banner():
    print("[FVD : Fake Video Detector]")




def main():
    signal(SIGINT, SIG_DFL)

    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('--model_path', '-mi',dest='model', type=str, default='./models/final_model.p')
    p.add_argument('--output_path', '-o',dest='videoOut', type=str, default='/path')
    p.add_argument('--start_frame', type=int, default=0)
    p.add_argument('--end_frame', type=int, default=None)
    p.add_argument('--cuda', action='store_true')
    p.add_argument('--fast', action='store_true')
    requiredNamed = p.add_argument_group('required arguments')
    requiredNamed.add_argument('--video_path', '-i', dest='videoIn', type=str, required=True)
    args = p.parse_args()

    video_path = args.videoIn

    prediction = None

    if video_path.endswith('.mp4') or video_path.endswith('.avi'):
        prediction = test_full_image_network(args.videoIn,args.model,args.videoOut,args.fast)
    else:
        print("Not valid input format")
        sys.exit(-1)


    print("The Fake Score is: " + str(prediction["score"]))
    print("Output video in: " + prediction["file"])

if __name__ == '__main__':
    #banner()
    main()

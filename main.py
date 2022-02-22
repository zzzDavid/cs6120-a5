import argparse
import json
import copy
import sys

def main():
    # read from file because it's easier to debug this way
    if file is not None:
        with open(file, "r") as infile:
           prog = json.load(infile)
    else: 
        prog = json.load(sys.stdin)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-reach', dest='reach_definitions',
                        default=False, action='store_true',
                        help='reach definitions')
    parser.add_argument('-live', dest='live_variable',
                        default=False, action='store_true',
                        help='live_variable')
    parser.add_argument('-const_prop', dest='const_prop',
                        default=False, action='store_true',
                        help='Constant propagation')
    parser.add_argument('-cse', dest='cse',
                        default=False, action='store_true',
                        help='CSE')
    parser.add_argument('-cf', dest='cf',
                        default=False, action='store_true',
                        help='constant folding')
    parser.add_argument('-f', dest='filename', 
                        action='store', type=str, help='json file')
    args = parser.parse_args()
    reach = args.reach_definitions
    live = args.live_variable
    const_prop = args.const_prop
    cse = args.cse
    cf = args.cf
    file = args.filename
    main(reach, live, const_prop, cse, cf, file)
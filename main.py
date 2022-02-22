import argparse
import json
import copy
import sys

from basic_block import form_basic_blocks
from control_flow_graph import *

def find_dominators(cfg):
    """
    - cfg: dict(str, BasicBlock)
    """
    dom = dict() # str -> set(str)
    while True:
        changed = False
        for vertex, bb in cfg.items():
            if vertex not in dom:
                dom[vertex] = list()
            # find all predecessors' dominators
            pred_doms = [dom[p] for p in bb.pred if p in dom]
            common_doms = set.intersection(*pred_doms) if len(pred_doms) > 0 else set()
            common_doms.add(vertex) # reflexive
            if not common_doms == dom[vertex]:
                dom[vertex] = common_doms
                changed = True
        if not changed: break
    return dom

def main(file=None):
    # read from file because it's easier to debug this way
    if file is not None:
        with open(file, "r") as infile:
           prog = json.load(infile)
    else: 
        prog = json.load(sys.stdin)

    for func in prog['functions']:
        blocks = form_basic_blocks(func['instrs'])
        blocks = [b for b in blocks if len(b) > 0]
        cfg = CFG(blocks).cfg
        dom = find_dominators(cfg)
        print(dom)
        


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
    main(file)
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

class Node():
    def __init__(self, name) -> None:
        self.name = name
        self.preds = []
        self.succs = []

def find_dom_tree(dom, cfg):
    """
    A dominator tree is a tree where each node's children are 
    those nodes it immediately dominates. Because the immediate 
    dominator is unique, it is a tree. The start node is the 
    root of the tree.
    
    - dom: dict(str, set(str))
    - cfg: dict(str, BasicBlock)
    - return: dict(str, Node)
    """
    dom_tree = dict()
    for vertex in cfg.keys():
        # find immediate dominators
        dominators = copy.deepcopy(dom[vertex])
        dominators.remove(vertex)
        idom = list()
        for d in dominators:
            # if the dominator's strict dominator is also in the set dominator
            # then it's not immediate dominator
            d_strict_doms = copy.deepcopy(dom[d])
            d_strict_doms.remove(d)
            if any([dd in dominators for dd in d_strict_doms]):
                continue
            idom.append(d)
            
        for parent in idom:
            if vertex not in dom_tree:
                dom_tree[vertex] = Node(vertex)
            if parent not in dom_tree:
                dom_tree[parent] = Node(parent)
            dom_tree[parent].succs.append(vertex)
            dom_tree[vertex].preds.append(parent)
    return dom_tree

def find_dom_frontier(dom, cfg):
    """
    The dominance frontier of a node d is the set of all 
    nodes ni such that d dominates an immediate predecessor
    of ni, but d does not strictly dominate ni. It is the
    set of nodes where d's dominance stops.
    """
    dom_frontier = dict()
    for vertex in cfg.keys():
        dom_frontier[vertex] = set()
        # find all nodes that are dominated by vertex
        domed = list()
        for v, dominators in dom.items():
            if vertex in dominators:
                domed.append(v)
        for d in domed:
            # if d's successor is not dominated by vertex
            # it's on the frontier
            for successor in cfg[d].succ:
                if successor not in domed:
                    dom_frontier[vertex].add(successor)
    return dom_frontier

def main(file=None):
    if file is not None:
        with open(file, "r") as infile:
           prog = json.load(infile)
    else: 
        prog = json.load(sys.stdin)

    for func in prog['functions']:
        blocks = form_basic_blocks(func['instrs'])
        blocks = [b for b in blocks if len(b) > 0]
        cfg = CFG(blocks).cfg
        from visualizer import CFGVisualizer
        cfg_visualizer = CFGVisualizer(cfg)
        cfg_visualizer.show()
        dom = find_dominators(cfg)
        dom_tree = find_dom_tree(dom, cfg)
        dom_frontier = find_dom_frontier(dom, cfg)
        print(dom)
        print(dom_tree)
        print(dom_frontier)


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
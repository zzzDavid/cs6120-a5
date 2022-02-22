TERMINATORS = ['jmp', 'ret', 'br']

class BasicBlock(object):
    def __init__(self, block):
        self.instrs = block
        self.pred = []
        self.succ = []

class CFG(object):
    """
    Give each block succ and pred 
    """
    def __init__(self, blocks, reverse=False):
        self.labels = list()
        self.blocks = blocks
        self.cfg = dict()
        self.reverse = reverse
        self.build_cfg()
    
    def build_cfg(self):
        # convert blocks from a list to a dictionary
        for block in self.blocks:
            # go through all blocks
            # build a list of Blocks
            bb = BasicBlock(block)
            label = "start"
            if "label" in block[0]:
                label = block[0]['label']
            self.cfg[label] = bb
            self.labels.append(label)

        # add succ and pred to the basic blocks
        for label, bb in self.cfg.items():
            # check the ternimator instr
            op = bb.instrs[-1]['op']
            if op not in TERMINATORS: continue
            if op == "jmp":
                jmp_target = bb.instrs[-1]['labels'][0]
                if self.reverse:
                    self.cfg[label].pred.append(jmp_target)
                    self.cfg[jmp_target].succ.append(label)
                else:
                    self.cfg[label].succ.append(jmp_target)
                    self.cfg[jmp_target].pred.append(label)
            elif op == "br":
                br_targets = bb.instrs[-1]['labels']
                for target in br_targets:
                    if self.reverse:
                        self.cfg[label].pred.append(target)
                        self.cfg[target].succ.append(label)
                    else:
                        self.cfg[label].succ.append(target)
                        self.cfg[target].pred.append(label)

    def gen_instrs(self):
        instrs = list()
        for label in self.labels:
            instrs.append({'label' : label})
            instrs.extend(self.cfg[label].instrs)
        return instrs
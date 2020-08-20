#!/usr/bin/env python

import glob
import os

dirs = sorted(glob.glob("psweep_num_*"))

for d in dirs:
    cmd = "./stats.py d"
    print(cmd)
    #os.system(cmd)

cmd = "./stats_fig.py"
print(cmd)
os.system(cmd)

#!/usr/bin/env python

import glob
import os

#dirs = sorted(glob.glob("output_data/psweep_num_*/dist_*"))
dirs = sorted(glob.glob("output_data/psweep_num_010/dist_025"))

for d in dirs:
	#cmd = '(cd ./%s/ ; slurm_run_mcell_range.py "1:1000" 24 Scene.main.mdl)' % d
    cmd = '(cd ./%s/ ; slurm_run_mcell_range.py "1:10" 24 Scene.main.mdl)' % d
    print(cmd)
    os.system(cmd)


#!/usr/bin/env python

import glob
import os

dirs = sorted(glob.glob("psweep_num_*/dist_*"))

for d in dirs:
	cmd = '(cd ./%s/ ; slurm_run_mcell_range.py "1:1000" 16 Scene.main.mdl)' % d
	print(cmd)
	os.system(cmd)


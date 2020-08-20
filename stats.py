##!/usr/bin/python3
import pandas as pd
import numpy as np
import os
from statistics import mean
import glob
import sys

def vdcc_stats(path, num_dir):
    # Data indexes
    N_FNAME_IDX = 0
    LOC_FNAME_IDX = 1
    SEED_FNAME_IDX = 3
    LAST_ELEM_IDX = -1
    CA_IDX = 1
    REL_IDX = 1
    NO_REL = 0
    
    os.chdir(path)
    peak_ca = []
    num_dist = []
    print(os.getcwd())

    for dist_dir in os.listdir(num_dir):
        print(num_dir, dist_dir)
        # all the peak cal vals for a given num/dist
        nd_peak = []

        # Data location for num and dist
        data_path = os.path.join(num_dir, dist_dir, 'react_data')

        # initialize number of releases for num/dist condition
        n_nd_rel = 0

        # For each seed
        for seed in os.listdir(data_path):
            # Open mcell ca file
            seed_path = os.path.join(data_path, seed)
            file = os.path.join(seed_path, 'ca.a001.dat')

            # Specify info in data list
            # num, loc, seed
            N_COL_PEAK = 0 # add to number of columns for each append
            peak_ca.append(num_dir.split('_')[LAST_ELEM_IDX])
            N_COL_PEAK += 1
            peak_ca.append(dist_dir.split('_')[LAST_ELEM_IDX])
            N_COL_PEAK += 1
            seed_num = seed.split('_')[LAST_ELEM_IDX]
            if int(seed_num) % 100 == 0:
                print(seed_num)
            peak_ca.append(seed_num)
            N_COL_PEAK += 1

            # ca max info
            ca_df = pd.read_csv(file, header=None, names=['time', 'count'],
                                delim_whitespace=True)
            peak_ca.append(ca_df.max()[CA_IDX]);
            N_COL_PEAK += 1

            # max
            nd_peak.append(ca_df.max()[CA_IDX])

            # release probabilities
            for f_rel in glob.glob(os.path.join(seed_path, '*_rel_*')):
                rel_df = pd.read_csv(f_rel, header=None,
                                     names=['time', 'count'],
                                     delim_whitespace=True)

                # if there is a release, increment counter and exit
                if rel_df.max()[REL_IDX] > NO_REL:
                    n_nd_rel += 1
                    break

        # Min, Avg, and Max for all seeds for num & dist
        N_COL_ND = 0
        num_dist.append(num_dir.split('_')[LAST_ELEM_IDX]);
        N_COL_ND += 1
        num_dist.append(dist_dir.split('_')[LAST_ELEM_IDX]);
        N_COL_ND += 1

        num_dist.append(min(nd_peak));
        N_COL_ND += 1
        num_dist.append(mean(nd_peak));
        N_COL_ND += 1
        num_dist.append(max(nd_peak));
        N_COL_ND += 1

        # Number of total releases per num/dist condition
        # print(n_nd_rel)

        # Divide number of seed which releases occur by total number of seeds
        # for num/dist condition
        p_rel = n_nd_rel / len(os.listdir(data_path))
        # print("Probability of release was: {:.3f}".format(p_rel))
        num_dist.append(p_rel);
        N_COL_ND += 1

    # Reshape peak to trial x conditions
    # n_vdccs, dist, seed, max_ca
    peak_ca = np.asarray(peak_ca).reshape((int(len(peak_ca)/N_COL_PEAK),
                                           N_COL_PEAK))

    # Reshape average peak ca to trial x condition
    # num, dist, min, avg, max
    num_dist = np.asarray(num_dist).reshape((int(len(num_dist)/N_COL_ND),
                                             N_COL_ND))

    return peak_ca, num_dist

# Set data path
path = '.'
# number dir is input arg
if len(sys.argv)==2:
    num_dir = sys.argv[1]

    # Call function for given number
    peak_ca, num_dist = vdcc_stats(path, num_dir)

    # Save output
    # create stats directory
    stats_dir = os.path.join(path, 'stats')
    if not os.path.exists(stats_dir):
        os.mkdir(stats_dir)

    peak_file = 'peak_ca_n_{}.csv'.format(num_dir.split('_')[-1])
    stats_file = 'n_{}_stats.csv'.format(num_dir.split('_')[-1])

    np.savetxt(os.path.join(stats_dir, peak_file), peak_ca, delimiter=",", fmt='%s',
           header='N_VDCCS, DIST, SEED_#, MAX_CA')
    print(peak_file, 'saved.')

    np.savetxt(os.path.join(stats_dir, stats_file), num_dist, delimiter=",", fmt='%s',
           header='N_VDCCS, DIST, MIN_PEAK_CA, AVG_PEAK_CA, MAX_PEAK_CA, P_REL')
    print(stats_file, 'saved.')

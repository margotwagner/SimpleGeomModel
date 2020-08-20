#!/usr/bin/python3
import pandas as pd
import numpy as np
import os
from statistics import mean
import glob
def vdcc_stats(path, plot=False):
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
    # Get maximum calcium for each sweep condition
    for num in glob.glob(os.path.join(path, 'psweep_num_200')): 
        for dist in os.listdir(num):
            print(num, dist)
            # all the max vals for a given num/dist
            nd_max = []

            # Data location for num and dist 
            data_path = os.path.join(num, dist, 'react_data')
            
            # initialize number of releases for num/dist condition
            n_nd_rel = 0
            
            # For each seed
            for seed in os.listdir(data_path):
                # Open mcell ca file
                seed_path = os.path.join(data_path, seed)
                file = os.path.join(seed_path, 'vdcc_pre_ca_flux.World.dat')
                
                # num, loc, seed #
                N_COL_PEAK = 0
                peak_ca.append(num.split('_')[LAST_ELEM_IDX]); N_COL_PEAK+=1
                peak_ca.append(dist.split('_')[LAST_ELEM_IDX]); N_COL_PEAK+=1
                seed_num = seed.split('_')[LAST_ELEM_IDX];
                if int(seed_num)%100 == 0:
                    print(seed_num)
                peak_ca.append(seed_num); N_COL_PEAK+=1
                
                # ca max info
                ca_df = pd.read_csv(file, header=None, names=['time','count'], delim_whitespace=True)
                peak_ca.append(ca_df.max()[CA_IDX]); N_COL_PEAK+=1 
                
                # max
                nd_max.append(ca_df.max()[CA_IDX])
                
                # release probabilities
                for f_rel in glob.glob(os.path.join(seed_path, '*_rel_*')):
                    rel_df = pd.read_csv(f_rel, header=None, names=['time','count'],delim_whitespace=True)
                    
                    # if there is a release, increment counter and exit
                    if rel_df.max()[REL_IDX] > NO_REL:
                        n_nd_rel += 1
                        break
                
            # Min, Avg, and Max for all seeds for num & dist
            N_COL_ND = 0
            num_dist.append(num.split('_')[LAST_ELEM_IDX]); N_COL_ND+=1
            num_dist.append(dist.split('_')[LAST_ELEM_IDX]); N_COL_ND+=1
            
            num_dist.append(min(nd_max)); N_COL_ND+=1
            num_dist.append(mean(nd_max)); N_COL_ND+=1
            num_dist.append(max(nd_max)); N_COL_ND+=1
            
            # Number of total releases per num/dist condition
            #print(n_nd_rel)
            
            # Divide number of seed which releases occur by total number of seeds for num/dist condition 
            p_rel = n_nd_rel/len(os.listdir(data_path))
            #print("Probability of release was: {:.3f}".format(p_rel))
            num_dist.append(p_rel); N_COL_ND+=1
    
    # Reshape peak to trial x conditions
    # n_vdccs, dist, seed, max_ca
    peak_ca = np.asarray(peak_ca).reshape((int(len(peak_ca)/N_COL_PEAK), N_COL_PEAK))
    
    # Reshape average peak ca to trialxcondition
    # num, dist, min, avg, max
    num_dist = np.asarray(num_dist).reshape((int(len(num_dist)/N_COL_ND), N_COL_ND))
    
    if plot==True:
        x = 1
    
    return peak_ca, num_dist

# Set data path
#os.chdir('/Users/margotwagner/projects/mcell/simple_geom/vdcc_psweep/')
path = '.'

# Call function
peak_ca, num_dist = vdcc_stats(path)

# Save output
np.savetxt('peak_ca_200.csv', peak_ca, delimiter=",", fmt='%s', 
           header='N_VDCCS, DIST, SEED_#, MAX_CA')
np.savetxt('vdcc_psweep_stats_200.csv', num_dist, delimiter=",", fmt='%s', 
           header='N_VDCCS, DIST, MIN_PEAK_CA, AVG_PEAK_CA, MAX_PEAK_CA, P_REL')

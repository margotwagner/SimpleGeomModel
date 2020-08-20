#!/usr/bin/python3
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

def vdcc_psweep_fig(path):
    '''
    Program that creates a figures for the vdcc psweep stats and saves to path loc.
            
    path: path where stats are kept
    '''
    os.chdir(path)
    fig, ax = plt.subplots(1, 2, figsize = (18, 6))
    
    # Open vdcc stats files
    for file in glob.glob('vdcc*.csv'):
        stats = pd.read_csv(file)
        stats.columns = stats.columns.str.replace(' ', '')
        stats.columns = stats.columns.str.replace('#', '')
        
        # Plot peak ca and p_rel
        ax[0].plot(stats['DIST'], stats['AVG_PEAK_CA'], label ='N = {}'.format(stats['N_VDCCS'][0]))
        
        ax[1].plot(stats['DIST'], stats['P_REL'], label ='N = {}'.format(stats['N_VDCCS'][0]))
        
    # Add titles and axes labels
    for i in range(2):
        ax[i].set_xlabel('VDCC Distance (nm)')
        ax[i].legend()
        if i == 0:
            ax[i].set_ylabel('Peak total Calcium (number)')
            ax[i].set_title('Peak total Calcium for various VDCC numbers and distances')
        else:
            ax[i].set_ylabel('Release probability')
            ax[i].set_title('Release probability for various VDCC numbers and distances')
    
    print('Figure creation complete.')
    plt.savefig('vdcc_psweep.png')

vdcc_psweep_fig('.')

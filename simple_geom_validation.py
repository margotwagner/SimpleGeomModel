#!/opt/python/bin/python3
import os
import numpy as np

number_vdcc_pre = np.arange(10, 210, 10)
vdcc_pre_lc = np.arange(0.025, 0.425, 0.025)
n_seeds = 1000

parent_dir = './output_data'

instant_file = 'Scene.instantiation.mdl'
par_file = 'Scene.parameters.mdl'

loc_file = 'vdcc_loc_instantiation.mdl'
num_file = 'vdcc_num_param.mdl'

with open(os.path.join(parent_dir, instant_file),'a+') as file:
    if not 'INCLUDE_FILE = "%s"' % loc_file in file.read():
        file.write('\nINCLUDE_FILE = "%s"\n' % loc_file)
        print('%s appended to Scene.parameters.mdl' % loc_file)
    else:
        print('%s found in Scene.parameters.mdl' % loc_file)


# Initialize Scene.parameters.mdl
with open(os.path.join(parent_dir, par_file),'a+') as file:
    if not 'INCLUDE_FILE = "%s"' % num_file in file.read():
        file.write('\nINCLUDE_FILE = "%s"\n' % num_file)
        print('%s appended to Scene.instantiation.mdl' % num_file)
    else:
        print('%s found in Scene.instantiation.mdl' % num_file)


for num_vdcc in number_vdcc_pre:
    for dist_vdcc in vdcc_pre_lc:
        path = os.path.join(parent_dir, 'psweep_num_{0:03d}/dist_{1:03d}'.format(num_vdcc, int(dist_vdcc*1000)))
        if not os.path.exists(path):
            os.makedirs(path)

        for seed in range(n_seeds):
            seed_path = os.path.join(path, 'react_data', 'seed_{:05d}'.format(seed+1))
            if not os.path.exists(seed_path):
                os.makedirs(seed_path)

        sceneList = [i for i in os.listdir(parent_dir) if 'Scene' in i]
        for scene in sceneList:
            os.symlink('../../%s' % scene, path + '/%s' % scene)

        num_dir = os.path.join(path, num_file)
        loc_dir = os.path.join(path, loc_file)

        if not os.path.exists(num_dir):
            with open(num_dir, 'w') as file:
                file.write('\nextra = %d \n\n' % num_vdcc)
                file.close()

        if not os.path.exists(loc_dir):
            #   Create arrays of vdcc positions randomly placed
            # Specify vdcc positioning conditions
            vdcc_density = 5000       # surface grid density
            vdcc_pre_pos_x = dist_vdcc   #distance from center of VDCC cluster to active zone in microns
            vdcc_pre_pos_y = 0.0
            vdcc_pre_pos_z = -0.25  # on surface of axon

            # Calculate radius of cluster (from disk area A = #/density = pi*r^2)
            r = np.sqrt(num_vdcc/(vdcc_density*np.pi))

            # Create list of positions for vdcc's
            n = 0
            pos_list = []
            while n < num_vdcc:
              x, y  = np.random.uniform(0,r,2)      # Uniformly sample for r = [0, R], theta = [0, 2pi]
              if np.sqrt(x**2+y**2) <= r:
                 pos_list.append([x+vdcc_pre_pos_x, y+vdcc_pre_pos_y, vdcc_pre_pos_z])
                 n += 1

            loc_str = ''
            for pos in pos_list:
                loc_str = loc_str + "     vdcc_pre_c0' %s\n"  % pos

            #   Create extra instantiation file with vdcc locations
            with open(loc_dir, 'w') as file:
                instant_str = 'INSTANTIATE vdcc_locs OBJECT{\n  vdcc_pre_rel RELEASE_SITE\n  {\n   SHAPE = LIST\n'
                instant_str = instant_str + '   SITE_DIAMETER = 0.05\n   MOLECULE_POSITIONS\n   {\n'
                instant_str = instant_str + loc_str + '   }\n   RELEASE_PROBABILITY = 1\n  }\n}\n'
                file.write(instant_str)








import sys, os


import numpy as np



sim_folder = '../first_test/PyPARIS/004_multibunch_with_ecloud/'
tag = 'first_sim_20b'
n_rings = 8

sim_folder = '../test_40b/'
tag = 'sim_40b'
n_rings = 10

sim_folder = '../test_20b_8kicks_12.5ns/004_multibunch_with_ecloud'
tag = 'sim_20b_8kicks'
n_rings = 5

sim_folder = '../test_20b_8kicks/004_multibunch_with_ecloud'
tag = 'sim_20b_8kicks_correct'
n_rings = 5

sim_folder = '../test_20b_8kicks_onlyH/004_multibunch_with_ecloud'
tag = 'sim_20b_8kicks_onlyH'
n_rings = 5

sim_folder = '../test_on_HPC_cluster_speed/004_multibunch_with_ecloud'
tag = 'test_on_HPC_cluster_speed'
n_rings = 40

sim_folder = '../test3_on_HPC_25ns/004_multibunch_with_ecloud'
tag = 'test3_on_HPC_25ns'
n_rings = 45

sim_folder = '../test7_on_HPC_25ns_checksynch/004_multibunch_with_ecloud'
tag = 'test7_on_HPC_25ns_checksynch'
n_rings = 45

sim_folder = '../test8_on_HPC_25ns_swaporder/004_multibunch_with_ecloud'
tag = 'test8_on_HPC_25ns_swaporder'
n_rings = 45

list_files = [sim_folder+'/bunch_monitor_ring%03d.h5'%ii for ii in range(n_rings)]

import myfilemanager as mfm
dict_data = mfm.bunchh5list_to_dict(list_files)

print 'Data loaded!'

n_turns = int(np.max(dict_data['i_turn']))+1
n_bunches = int(np.max(dict_data['i_bunch']))+1

list_bunches = []
for i_bunch_obs in range(n_bunches):
    print('Bunch %d/%d'%(i_bunch_obs, n_bunches))
    dict_bunch = {kk:np.zeros(n_turns, dtype=np.float64)+np.nan for kk in dict_data.keys()}
    for ii in xrange(len(dict_data['i_bunch'])):
        if int(dict_data['i_bunch'][ii]) == int(i_bunch_obs):
            i_turn = int(dict_data['i_turn'][ii])
            for kk in dict_data.keys():
                dict_bunch[kk][i_turn] = dict_data[kk][ii]
                
    list_bunches.append(dict_bunch)


x_mat = np.zeros((n_turns, n_bunches))
y_mat = np.zeros((n_turns, n_bunches))
n_mat = np.zeros((n_turns, n_bunches))

for i_bunch_obs in range(n_bunches):
    n_turns_this = len(list_bunches[i_bunch_obs]['epsn_x'])
    mask_notnan = ~np.isnan(list_bunches[i_bunch_obs]['macroparticlenumber'])
    x_mat[:n_turns_this, i_bunch_obs][mask_notnan] = list_bunches[i_bunch_obs]['mean_x'][mask_notnan]
    y_mat[:n_turns_this, i_bunch_obs][mask_notnan] = list_bunches[i_bunch_obs]['mean_y'][mask_notnan]
    n_mat[:n_turns_this, i_bunch_obs][mask_notnan] = list_bunches[i_bunch_obs]['macroparticlenumber'][mask_notnan]


import scipy.io as sio
sio.savemat(tag+'_matrices.mat',
    {
   'x_mat':x_mat, 
   'y_mat':y_mat, 
   'n_mat':n_mat
    }, 
    oned_as='row')
    

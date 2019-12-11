import numpy as np

import PyPARIS.myfilemanager as mfm

sim_folder = '../HL-LHC_coupled_bunch_450GeV_1.1e11_144b'
tag = 'HL_1.1e11_144b'
n_rings = 100
n_parts = 2

sim_folder = '../HL-LHC_coupled_bunch_450GeV_1.1e11_144b_damper'
tag = 'HL_1.1e11_144b_fb'
n_rings = 100
n_parts = 1

sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b'
tag = 'HL_2.3e11_144b'
n_rings = 100
n_parts = 2

sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_damper'
tag = 'HL_2.3e11_144b_fb'
n_rings = 100
n_parts = 6

sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_damper_100turns'
tag = 'HL_2.3e11_144b_fb_100t'
n_rings = 100
n_parts = 6

sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_Qp15'
tag = 'HL_2.3e11_144b_Qp15'
n_rings = 100
n_parts = 2  #2nd part not finished 

sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_Qp15_damper'
tag = 'HL_2.3e11_144b_Qp15_fb'
n_rings = 100
n_parts = 2 #?

sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_Qp0_Koct-4.5'
tag = 'HL_2.3e11_144b_Koct-4.5'
n_rings = 100
n_parts = 3  #2nd part not finished 

sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_Qp0_Oct-4.5_damper'
tag = 'HL_2.3e11_144b_Koct-4.5_fb'
n_rings = 100
n_parts = 3 #?

sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_Qp15_Oct-4.5'
tag = 'HL_2.3e11_144b_Qp15_Koct-4.5'
n_rings = 100
n_parts = 3  #2nd part not finished 

sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_Qp15_Oct-4.5_damper'
tag = 'HL_2.3e11_144b_Qp15_Koct-4.5_fb'
n_rings = 100
n_parts = 3 #?

# sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_sey1.5'
# tag = 'HL_2.3e11_144b_sey1.5'
# n_rings = 100
# n_parts = 2

# sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_sey1.5_both_planes'
# tag = 'HL_2.3e11_144b_sey1.5_xy'
# n_rings = 100
# n_parts = 2

to_be_saved = [
 'epsn_x',
 'epsn_y',
 'epsn_z',
 'macroparticlenumber',
 'mean_dp',
 'mean_x',
 'mean_xp',
 'mean_y',
 'mean_yp',
 'mean_z',
 'sigma_dp',
 'sigma_x',
 'sigma_y',
 'sigma_z']


def make_part_matrices(list_files, to_be_saved):

    dict_data = mfm.monitorh5list_to_dict(list_files, permissive=True)

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
                if dict_data['macroparticlenumber'][ii] > 0:
                    for kk in dict_data.keys():
                        dict_bunch[kk][i_turn] = dict_data[kk][ii]

        list_bunches.append(dict_bunch)


    dict_matrices = {kk: np.zeros((n_turns, n_bunches)) for kk in to_be_saved}

    for i_bunch_obs in range(n_bunches):
        n_turns_this = len(list_bunches[i_bunch_obs]['epsn_x'])
        mask_notnan = ~np.isnan(list_bunches[i_bunch_obs]['macroparticlenumber'])

        for kk in to_be_saved:
            dict_matrices[kk][:n_turns_this, i_bunch_obs][mask_notnan] =\
                    list_bunches[i_bunch_obs][kk][mask_notnan]
    return dict_matrices

list_dicts = []
for i_part in range(n_parts):
    list_files = [sim_folder+'/bunch_monitor_part%03d_ring%03d.h5'%(i_part, ii) for ii in range(n_rings)]
    this_dict_matrices = make_part_matrices(list_files, to_be_saved)
    list_dicts.append(this_dict_matrices)

dict_matrices = {}
for kk in list_dicts[0].keys():
    dict_matrices[kk] = np.concatenate(
            [dd[kk] for dd in list_dicts], axis=0)

import scipy.io as sio
sio.savemat(tag+'_matrices.mat', dict_matrices, oned_as='row')

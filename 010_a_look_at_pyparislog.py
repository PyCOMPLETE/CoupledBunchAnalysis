import time
import numpy as np

sim_folder = '../test_20b_8kicks_onlyH/004_multibunch_with_ecloud'
sim_folder = '../test_on_HPC_cluster_evenlessspeed_nomultithreading/004_multibunch_with_ecloud' #25ns'
sim_folder = '../test_on_HPC_cluster_evenlessspeed/004_multibunch_with_ecloud' #25ns
#sim_folder = '../test_on_HPC_cluster_lessspeed/004_multibunch_with_ecloud' #12.5ns
#sim_folder = '../test_on_HPC_cluster_speed/004_multibunch_with_ecloud' #12.5ns/2
#sim_folder = '../test_on_HPC_cluster_morespeed/004_multibunch_with_ecloud' #12.5ns/4

sim_folder = '../test2_on_HPC_1slot_1cores/004_multibunch_with_ecloud'
sim_folder = '../test2_on_HPC_1slot_8cores/004_multibunch_with_ecloud'
sim_folder = '../test2_on_HPC_1slot/004_multibunch_with_ecloud'
#sim_folder = '../test2_on_HPC_2slot/004_multibunch_with_ecloud'
#sim_folder = '../test2_on_HPC_4slot/004_multibunch_with_ecloud'
#sim_folder = '../test2_on_HPC_4slot_240cores/004_multibunch_with_ecloud'
#sim_folder = '../test2_on_HPC_8slot/004_multibunch_with_ecloud'


with open(sim_folder+'/pyparislog.txt') as fid:
    pyploglns = fid.readlines()

#check that pyparislog is proper
flag_startsim = map(lambda s: 'PyPARIS simulation -- multiturn parallelization' in s, pyploglns)
if np.sum(flag_startsim)!=1:
    print('sum(flag_startsim) is %d'%np.sum(flag_startsim))
    raise ValueError('Problem in pyparislog! Did you start from an empty file')

dict_config = {}
config_params = 'N_cores N_pieces_per_transfer N_buffer_float_size N_buffer_int_size N_parellel_rings N_nodes_per_ring'.split()
for par in config_params:
    flag_par = map(lambda s: par+' = ' in s, pyploglns)
    assert np.sum(flag_par)==1
    i_par = np.where(flag_par)[0][0]
    dict_config[par] = int(pyploglns[i_par].split()[-1])

t_list = []
ibun_list = []
iturn_list = []
for ln in pyploglns:
    if 'iter' in ln and 'cpu' in ln and 'turn' in ln:
        t_string = ln.split(', ')[0]
        tt = time.mktime(time.strptime(t_string, "%d/%m/%Y %H:%M:%S"))
        
        if 'cpu 0.0 startin bunch' not in ln:
            raise ValueError('What?!')
            
        ibun = int(ln.split('cpu 0.0 startin bunch ')[-1].split('/')[0])
        iturn = int(ln.split('turn=')[-1])
        
        ibun_list.append(ibun)        
        t_list.append(tt)
        iturn_list.append(iturn)

ibun_arr = np.array(ibun_list)
t_arr = np.array(t_list)
iturn_arr = np.array(iturn_list)

iter_turn_steps = np.array([0] + list(np.where(np.diff(iturn_list))[0]+1))
iturn_steps = iturn_arr[iter_turn_steps]
tturn_steps = t_arr[iter_turn_steps] 

n_turns_steps = list(set(np.diff(iturn_steps)))
assert len(n_turns_steps)==1
n_turns_steps = n_turns_steps[0]

avgt_turn_steps = np.diff(tturn_steps)/n_turns_steps


import matplotlib.pyplot as plt
plt.close('all')
plt.figure(figsize=(8,1.5*6))
ax1=plt.subplot(4,1,1)
plt.plot(np.diff(t_list), '.-')
ax1.set_ylabel('Iteration time [s]')
ax1.set_ylim(bottom=0)
ax2=plt.subplot(4,1,2, sharex=ax1)
plt.plot(ibun_list, '.-')
ax2.set_ylabel('"Bunch" at CPU 0')
ax3=plt.subplot(4,1,3, sharex=ax1)
plt.plot(iturn_list, '.-')
ax3.plot(iter_turn_steps, iturn_steps, '.r')
ax3.set_ylabel('Turn at CPU 0')
ax4=plt.subplot(4,1,4, sharex=ax1)
plt.plot((np.array(t_list)-t_list[0])/3600., '.-')
ax4.set_ylabel('Accumulated time [h]')
for ax in [ax1, ax2, ax3, ax4]:
    ax.grid('on')
plt.show()

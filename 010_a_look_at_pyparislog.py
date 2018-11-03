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

sim_folder = '../test2_on_HPC_4slot_withHT/004_multibunch_with_ecloud'
# sim_folder = '../test2_on_HPC_4slot/004_multibunch_with_ecloud'

sim_folder = '../test3_on_HPC_25ns/004_multibunch_with_ecloud'

sim_folder = '../test4_on_HPC_8slot/004_multibunch_with_ecloud'
sim_folder = '../test6_on_HPC_8slot/004_multibunch_with_ecloud'

sim_folder = '../test9_on_HPC_25ns_correct/004_multibunch_with_ecloud'
#sim_folder = '../test11_on_HPC_25ns_more_slices/004_multibunch_with_ecloud'

#sim_folder = '../test9bis_on_HPC_25ns_correct_be_long/004_multibunch_with_ecloud'

sim_folder = '../test10_onHPC_144b/004_multibunch_with_ecloud'

import parse_pyparislog as ppl
dict_config, ibun_arr, t_arr, iturn_arr, iter_turn_steps, \
    iturn_steps, tturn_steps, n_turns_steps, avgt_turn_steps = ppl.parse_pyparislog(sim_folder+'/pyparislog.txt')

Dt_iter = np.diff(t_arr)
n_filter = 10
Dt_iter_filtered = np.convolve(Dt_iter, np.ones(n_filter)/float(n_filter), mode='same')


import matplotlib.pyplot as plt
# plt.close('all')
fig1 = plt.figure(figsize=(8,1.3*6))
ax1=plt.subplot(4,1,1)
plt.plot(Dt_iter, '.-')
plt.plot(Dt_iter_filtered, 'r-')
ax1.set_ylabel('Iteration time [s]')
ax1.set_ylim(bottom=0)
ax2=plt.subplot(4,1,2, sharex=ax1)
plt.plot(ibun_arr, '.-')
ax2.set_ylabel('"Bunch" at CPU 0')
ax3=plt.subplot(4,1,3, sharex=ax1)
plt.plot(iturn_arr, '.-')
ax3.plot(iter_turn_steps, iturn_steps, '.r')
ax3.set_ylabel('Turn at CPU 0')
ax4=plt.subplot(4,1,4, sharex=ax1)
plt.plot((np.array(t_arr)-t_arr[0])/3600., '.-')
ax4.set_ylabel('Accumulated time [h]')
for ax in [ax1, ax2, ax3, ax4]:
    ax.grid('on')
fig1.suptitle(sim_folder)
plt.show()

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



import matplotlib.pyplot as plt
#~ plt.close('all')
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
ax3.set_ylabel('Turn at CPU 0')
ax4=plt.subplot(4,1,4, sharex=ax1)
plt.plot((np.array(t_list)-t_list[0])/3600., '.-')
ax4.set_ylabel('Accumulated time [h]')
for ax in [ax1, ax2, ax3, ax4]:
    ax.grid('on')
plt.show()

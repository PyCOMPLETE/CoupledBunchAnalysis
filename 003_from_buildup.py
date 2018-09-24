import sys, os
import numpy as np
import matplotlib.pyplot as plt

import myfilemanager as mfm
import numpy as np
import matplotlib.pyplot as plt

sim_folder = '../test_on_HPC_cluster_speed/004_multibunch_with_ecloud'
tag = 'test_on_HPC_cluster_speed'
n_rings = 40
ring = 3
iterat = 7
b_spac = 25e-9

ob = mfm.myloadmat_to_obj(sim_folder+'/cloud_evol_ring%d__iter%d.mat'%(ring, iterat))

t_ref = ob.t[0]

plt.close('all')
plt.figure(1)
ax1 = plt.subplot(2,1,1)
ax1.plot((ob.t-t_ref)/1e-9, ob.Nel_timep)
ax2 = plt.subplot(2,1,2, sharex=ax1)
ax2.plot((ob.t-t_ref), ob.lam_t_array)

plt.figure(2)
plt.pcolormesh(ob.xg_hist, (ob.t_hist-t_ref)/b_spac, ob.nel_hist)

# #down sample nel_hist
# avg_pos = []
# for ii in range(len(ob.t_hist)):


plt.show()
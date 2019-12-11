import sys, os
import numpy as np
import matplotlib.pyplot as plt

import PyPARIS.myfilemanager as mfm

tag = 'HL_1.1e11_144b'
# tag = 'HL_1.1e11_144b_fb'

# tag = 'HL_2.3e11_144b'
# tag = 'HL_2.3e11_144b_fb'
# tag = 'HL_2.3e11_144b_fb_100t'

tag = 'HL_2.3e11_144b_Qp15'
# tag = 'HL_2.3e11_144b_Qp15_fb'

# tag = 'HL_2.3e11_144b_Koct-4.5'
# tag = 'HL_2.3e11_144b_Koct-4.5_fb'

# tag = 'HL_2.3e11_144b_Qp15_Koct-4.5'
# tag = 'HL_2.3e11_144b_Qp15_Koct-4.5_fb'

# tag = 'HL_2.3e11_144b_sey1.5'
# tag = 'HL_2.3e11_144b_sey1.5_xy'

N_slots_bsp = 5

i_bunch = 35
i_turn_start = 150
n_turns = 50

ob_slice = mfm.object_with_arrays_and_scalar_from_h5(tag + '_matrices_slices.h5')
ob_bunch = mfm.myloadmat_to_obj(tag+'_matrices.mat')

x_slice = ob_slice.mean_x
y_slice = ob_slice.mean_y
z_slice = ob_slice.mean_z
n_slice = ob_slice.n_macroparticles_per_slice

x_bunch = ob_bunch.mean_x 
y_bunch = ob_bunch.mean_y
n_bunch = ob_bunch.macroparticlenumber

n_turns_tot = x_slice.shape[1]

i_bunch_slot = (i_bunch -1) * N_slots_bsp
mask_slice = n_slice[:, 1, i_bunch_slot] > 0
mask_bunch = n_bunch[1, :] > 0

from matplotlib import rc
rc('font', **{'family': 'sans-serif', 'sans-serif': ['arial'], 'size': 13})

plt.close('all')

colors = plt.cm.GnBu(np.linspace(0, 1, n_turns))
colors = plt.cm.PuBu(np.linspace(0, 1, n_turns))
colors = plt.cm.YlGnBu(np.linspace(0, 1, n_turns))

figm = plt.figure(10, figsize=(8,6*1.5))
axm1 = figm.add_subplot(3,1,1)
axm2 = figm.add_subplot(3,1,2)
axm3 = figm.add_subplot(3,1,3)

for i_turn in xrange(n_turns):

    axm1.plot(x_bunch[i_turn_start + i_turn, :][mask_bunch], color=colors[i_turn], alpha=0.6)
    if i_turn == n_turns - 1:
        axm1.plot(x_bunch[i_turn_start + i_turn, :][mask_bunch], '.', color='darkblue')

    axm2.plot(x_bunch[:, i_bunch_slot], color='darkblue', linewidth=0.7, alpha=0.4)

    n_tot = np.sum(n_slice[:, i_turn_start + i_turn, i_bunch_slot])
    axm3.plot(z_slice[:, i_turn_start + i_turn, i_bunch_slot][mask_slice], 
              (x_slice[:, i_turn_start + i_turn, i_bunch_slot][mask_slice]
              * n_slice[:, i_turn_start + i_turn, i_bunch_slot][mask_slice])
              / n_tot, color=colors[i_turn])
    

axm1.axvline(i_bunch, linestyle=':', color='crimson', linewidth=2.5)
axm2.axvspan(i_turn_start, i_turn_start + n_turns, alpha=0.5, color='crimson')

# for ibef in xrange(10):
#     if i_turn-ibef-1>=0:
#         axm1.plot(x_mat[i_turn-ibef-1, :][mask_bunch], '--', color='k', alpha=0.5)
#         axm2.plot(y_mat[i_turn-ibef-1, :][mask_bunch], '--', color='k', alpha=0.5)

# axm1.set_ylim(np.array([-1., 1.])*np.max(np.abs(x_mat)))
# axm2.set_ylim(np.array([-1., 1.])*np.max(np.abs(y_mat)))

# axm3.set_ylim(np.array([0, 1.1])*np.max(np.abs(n_mat)))


axm1.grid('on')
axm2.grid('on')
axm3.grid('on')

axm1.set_xlabel('Bunch')
axm1.set_ylabel('x [m]')
axm1.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

axm2.set_xlabel('Turn')
axm2.set_ylabel('x [m]')
axm2.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

axm3.set_xlabel('z [m]')
axm3.set_ylabel('P.U. signal')
axm3.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

figm.subplots_adjust(hspace=0.3)
# figm.suptitle('Turn %d'%i_turn)




plt.show()

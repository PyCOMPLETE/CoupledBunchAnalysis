import sys, os
import numpy as np
import matplotlib.pyplot as plt

import myfilemanager as mfm

# tag = 'HL_1.1e11_144b'
# tag = 'HL_1.1e11_144b_fb'

# tag = 'HL_2.3e11_144b'
# tag = 'HL_2.3e11_144b_fb'
# tag = 'HL_2.3e11_144b_fb_100t'

# tag = 'HL_2.3e11_144b_Qp15'
# tag = 'HL_2.3e11_144b_Qp15_fb'

tag = 'HL_2.3e11_144b_Koct-4.5'
tag = 'HL_2.3e11_144b_Koct-4.5_fb'

tag = 'HL_2.3e11_144b_Qp15_Koct-4.5'
tag = 'HL_2.3e11_144b_Qp15_Koct-4.5_fb'

# tag = 'HL_2.3e11_144b_sey1.5'
# tag = 'HL_2.3e11_144b_sey1.5_xy'

ob = mfm.myloadmat_to_obj(tag+'_matrices.mat')

x_mat = ob.mean_x
y_mat = ob.mean_y
ex_mat = ob.epsn_x
ey_mat = ob.epsn_y
n_mat = ob.macroparticlenumber

n_turns = x_mat.shape[0]

mask_bunch = n_mat[1, :]>0

plt.close('all')

fig1 = plt.figure(1, figsize=(8*1.5, 6*1.3))
axx = plt.subplot(3,2,1)
axx.plot(x_mat[:,mask_bunch])
axy = plt.subplot(3,2,3, sharex=axx)
axy.plot(y_mat[:,mask_bunch])
axn = plt.subplot(3,2,5, sharex=axx)
axn.plot(n_mat[:,mask_bunch])

mask_e = np.logical_and(ex_mat[:,mask_bunch] > 0, ey_mat[:,mask_bunch] > 0)

axex = plt.subplot(3,2,2)
axex.plot(ex_mat[:,mask_bunch])
# axex.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
axey = plt.subplot(3,2,4, sharex=axx)
axey.plot(ey_mat[:,mask_bunch])
# axey.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
axen = plt.subplot(3,2,6, sharex=axx)
axen.plot(n_mat[:,mask_bunch])

for ax in [axex, axey]:
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.set_ylim(bottom=2.4e-6)
plt.savefig('Overview_%s.png'%(tag), dpi=200)


i_turn = 800

figm = plt.figure(10, figsize=(8,6*1.3))
axm1 = figm.add_subplot(3,1,1)
axm2 = figm.add_subplot(3,1,2, sharex=axm1)
axm3 = figm.add_subplot(3,1,3, sharex=axm1)

mask_bunch = n_mat[1, :]>0

axm1.plot(x_mat[i_turn, :][mask_bunch], '.-')
axm2.plot(y_mat[i_turn, :][mask_bunch], '.-')
axm3.plot(n_mat[i_turn, :][mask_bunch], '.-')

for ibef in xrange(10):
    if i_turn-ibef-1>=0:
        axm1.plot(x_mat[i_turn-ibef-1, :][mask_bunch], '--', color='k', alpha=0.5)
        axm2.plot(y_mat[i_turn-ibef-1, :][mask_bunch], '--', color='k', alpha=0.5)

axm1.set_ylim(np.array([-1., 1.])*np.max(np.abs(x_mat)))
axm2.set_ylim(np.array([-1., 1.])*np.max(np.abs(y_mat)))

axm3.set_ylim(np.array([0, 1.1])*np.max(np.abs(n_mat)))


axm1.grid('on')
axm2.grid('on')
axm3.grid('on')


figm.suptitle('Turn %d'%i_turn)




plt.show()

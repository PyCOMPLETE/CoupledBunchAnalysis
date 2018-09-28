import sys, os
import numpy as np
import matplotlib.pyplot as plt

import myfilemanager as mfm

tag = 'test3_on_HPC_25ns'

ob = mfm.myloadmat_to_obj(tag+'_matrices.mat')

x_mat = ob.x_mat
y_mat = ob.y_mat
n_mat = ob.n_mat

n_turns = x_mat.shape[0]

mask_bunch = n_mat[1, :]>0

plt.close('all')

fig1 = plt.figure(1)
axx = plt.subplot(3,1,1)
axx.plot(x_mat[:,mask_bunch])
axy = plt.subplot(3,1,2, sharex=axx)
axy.plot(y_mat[:,mask_bunch])
axn = plt.subplot(3,1,3, sharex=axx)
axn.plot(n_mat[:,mask_bunch])


i_turn = 420

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

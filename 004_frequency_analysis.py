from __future__ import print_function
import sys
sys.path.append('../NAFFlib')

import matplotlib.pyplot as plt
import numpy as np

import nafflib as NAFF
import myfilemanager as mfm

tag = 'test9_on_HPC_25ns_correct'

ob = mfm.myloadmat_to_obj(tag+'_matrices.mat')


mask_bunch = ob.n_mat[1, :]>0
N_bunches = np.sum(mask_bunch)


x_mat = ob.x_mat[:,mask_bunch]
y_mat = ob.y_mat[:,mask_bunch]
n_mat = ob.n_mat[:,mask_bunch]


plt.close('all')

fig1 = plt.figure(1)
axx = plt.subplot(3,1,1)
axx.plot(x_mat)
axy = plt.subplot(3,1,2, sharex=axx)
axy.plot(y_mat)
axn = plt.subplot(3,1,3, sharex=axx)
axn.plot(n_mat)

tune_list = []
i_start = 0+50+50+50+50
i_stop = 50+50+50+50+50
for ii in range(N_bunches):
    tune_list.append(NAFF.get_tune(x_mat[i_start:i_stop, ii]))


plt.show()


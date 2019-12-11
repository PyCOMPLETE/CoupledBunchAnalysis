from __future__ import print_function
import sys
sys.path.append('../NAFFlib')

import matplotlib.pyplot as plt
import numpy as np

import NAFFlib as NAFF
import myfilemanager as mfm

tag = 'HL_1.1e11_144b'

ob = mfm.myloadmat_to_obj(tag+'_matrices.mat')

x_mat = ob.mean_x
y_mat = ob.mean_y
n_mat = ob.macroparticlenumber

mask_bunch = n_mat[1, :]>0
N_bunches = np.sum(mask_bunch)

x_mat_m = x_mat[:,mask_bunch]
y_mat_m = y_mat[:,mask_bunch]
n_mat_m = n_mat[:,mask_bunch]


plt.close('all')

fig1 = plt.figure(1)
axx = plt.subplot(3,1,1)
axx.plot(x_mat_m)
axy = plt.subplot(3,1,2, sharex=axx)
axy.plot(y_mat_m)
axn = plt.subplot(3,1,3, sharex=axx)
axn.plot(n_mat_m)

i_start = 0
i_stop = 50
plt.figure(2)
axt = plt.subplot(1,1,1)
for n_win in range(7):
    tune_list = []
    for ii in range(N_bunches):
        i_0 = i_start+n_win*i_stop
        i_1 = (n_win+1)*i_stop
        tune_list.append(NAFF.get_tune(x_mat_m[i_0:i_1, ii]))
    axt.plot(tune_list, label='%d-%d'%(i_0, i_1))
axt.legend()

plt.show()


import sys, os
import numpy as np
import matplotlib.pyplot as plt

import PyPARIS.myfilemanager as mfm

tag = 'HL_1.1e11_144b'
# tag = 'HL_1.1e11_144b_fb'

tag = 'HL_2.3e11_144b'
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
b_per_train = 72
movie_range = (0, 475)
n_traces = 25

loss_lim = 0.1

folder_movie = './movieslices_' + tag
try:
    os.mkdir(folder_movie)
except:
    pass

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

mask_bunch = n_bunch[1, :] > 0

bslots = np.where(mask_bunch)[0]/N_slots_bsp
i_start_trains = [np.min(bslots)]
i_start_trains.extend(np.where(np.diff(bslots) > 1)[0] + 1)
n_trains = len(i_start_trains)

# identify turn where losses reach limit
n_bunch_loss = 1 - n_bunch[:, mask_bunch] / n_bunch[0, mask_bunch]
try:
    i_turn_loss = np.where(n_bunch_loss > loss_lim)[0][0]
except IndexError:
    i_turn_loss = -1

print('%d %% losses occurred after %d turns'%(loss_lim*100, i_turn_loss))

# find most unstable bunch until loss limit
max_offset = np.max(np.abs(x_bunch[:i_turn_loss, :]))
i_bunch_max = np.where(np.abs(x_bunch[:i_turn_loss, :]) == max_offset)[1]
i_slot_max = i_bunch_max / N_slots_bsp

print('Most unstable bunch %d'%(i_slot_max))

mask_slice = n_slice[:, 1, i_bunch_max] > 0

if movie_range[1] == -1:
    movie_range = (movie_range[0], n_turns_tot)
turn_list = range(movie_range[0], movie_range[1])
n_turns = len(turn_list)

from matplotlib import rc
rc('font', **{'family': 'sans-serif', 'sans-serif': ['arial'], 'size': 13})

colors = plt.cm.YlGnBu(np.linspace(0, 1, n_traces))

plt.close('all')

figm = plt.figure(10, figsize=(8,6*1.5))

for i_frame, i_turn in enumerate(turn_list):
    print('Turn %d/%d'%(i_turn, n_turns_tot))
    
    figm.clf()
    axm1 = figm.add_subplot(3,1,1)
    axm2 = figm.add_subplot(3,1,2)
    axm3 = figm.add_subplot(3,1,3)
    axm11 = axm1.twinx()

    for i_trace in range(n_traces+1)[::-1]:
        if i_turn - i_trace >= 0:
            for i_train, i_start in enumerate(i_start_trains):
                i_stop = i_start + b_per_train
                axm1.plot(bslots[i_start:i_stop], x_bunch[i_turn-i_trace, :][mask_bunch][i_start:i_stop],
                          color=colors[n_traces-i_trace-1], alpha=0.8) #, alpha=1-float(i_trace)/(2*n_traces))
            axm3.plot(z_slice[:, i_turn-i_trace, i_bunch_max][mask_slice], 
                      (x_slice[:, i_turn-i_trace, i_bunch_max][mask_slice] *
                       n_slice[:, i_turn-i_trace, i_bunch_max][mask_slice]),
                      color=colors[n_traces-i_trace-1])#, alpha=1-float(i_trace)/n_traces)

    axm1.plot(bslots, x_bunch[i_turn, :][mask_bunch], '.', color='darkblue')

    axm11.plot(bslots, n_bunch_loss[i_turn, :] * 100, '.', color='darkgray')

    axm2.plot(x_bunch[:i_turn, i_bunch_max], color='darkblue')

    axm3.plot(z_slice[:, i_turn, i_bunch_max][mask_slice], 
              (x_slice[:, i_turn, i_bunch_max][mask_slice] *
               n_slice[:, i_turn, i_bunch_max][mask_slice]),
              color=colors[-1], linewidth=2.5)#, alpha=1-float(i_trace)/n_traces)
              # color='midnightblue', linewidth=2.3)#, alpha=1-float(i_trace)/n_traces)

    axm1.axvline(i_slot_max, linestyle=':', color='crimson', linewidth=2.5)
    axm2.axvspan(np.max([i_turn - n_traces, 0]), i_turn, alpha=0.5, color='crimson')

    for ax in [axm1, axm2, axm3]:
        ax.grid('True', linestyle=':')

    axm1.set_xlabel('Bunch')
    axm1.set_ylabel('x [m]')
    ymax = 1.05 * np.max(x_bunch[movie_range[0]: movie_range[1], :])
    axm1.set_ylim(-ymax, ymax)
    axm1.set_xlim(bslots[0]-2, bslots[-1]+2)
    axm1.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

    axm11.set_ylabel('Losses [%]')
    axm11.set_ylim(0, 100)

    axm2.set_xlabel('Turn')
    axm2.set_ylabel('x [m]')
    ymax = 1.05 * np.max(x_bunch[movie_range[0]: movie_range[1], i_bunch_max])
    axm2.set_ylim(-ymax, ymax)
    axm2.set_xlim(-2, movie_range[-1]+2)
    axm2.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

    axm3.set_xlabel('z [m]')
    axm3.set_ylabel('P.U. signal')
    ymax = 1.05 * np.max(x_slice[:, movie_range[0]: movie_range[1], i_bunch_max] *
                       n_slice[:, movie_range[0]: movie_range[1], i_bunch_max])
    axm3.set_ylim(-ymax, ymax)
    axm3.ticklabel_format(axis='y', style='sci', scilimits=(0,0))

    figm.subplots_adjust(hspace=0.3, bottom=0.07, top=0.94)
    figm.suptitle('Turn %d'%i_turn)
    figm.savefig(folder_movie+'/frame_%05d.png'%i_frame, dpi=200)

plt.show()

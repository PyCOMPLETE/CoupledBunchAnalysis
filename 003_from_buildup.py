import sys, os
import numpy as np
import matplotlib.pyplot as plt

import numpy as np

import parse_pyparislog as ppl
import mystyle as ms
import myfilemanager as mfm

sim_folder = '../test3_on_HPC_25ns/004_multibunch_with_ecloud'
tag = 'test3_on_HPC_25ns'

i_turn = 601
b_spac = 25e-9
N_slots_bsp = 5

flag_movie = True
movie_range = (0, 700)
vmax_movie = 2e11


obbea = mfm.myloadmat_to_obj(tag+'_matrices.mat')

dict_config, ibun_arr, t_arr, iturn_arr, iter_turn_steps, \
    iturn_steps, tturn_steps, n_turns_steps, avgt_turn_steps = ppl.parse_pyparislog(sim_folder+'/pyparislog.txt')





plt.close('all')
ms.mystyle_arial(fontsz=16, dist_tick_lab=5)

Dt_iter = np.diff(t_arr)
n_filter = 10
Dt_iter_filtered = np.convolve(Dt_iter, np.ones(n_filter)/float(n_filter), mode='same')


fig1 = plt.figure(100, figsize=(8,1.5*6))
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




x_mat = obbea.x_mat
y_mat = obbea.y_mat
n_mat = obbea.n_mat

n_turns = x_mat.shape[0]

mask_bunch = n_mat[1, :]>0
n_bunches = np.sum(mask_bunch)


figrt = plt.figure(2000)
axx = plt.subplot(3,1,1)
axx.plot(x_mat[:,mask_bunch])
axy = plt.subplot(3,1,2, sharex=axx)
axy.plot(y_mat[:,mask_bunch])
axn = plt.subplot(3,1,3, sharex=axx)
axn.plot(n_mat[:,mask_bunch])

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



if not flag_movie:
    figbup = plt.figure(1)
    axbup1 = plt.subplot(2,1,1)
    axbup2 = plt.subplot(2,1,2, sharex=axbup1)

figst = plt.figure(200)
figst.set_facecolor('w')

if flag_movie:
    folder_movie = './movieele_' + tag
    try:
        os.mkdir(folder_movie)
    except:
        pass

if flag_movie:
    turn_list = range(movie_range[0], movie_range[1])
else:
    turn_list = [i_turn]

for i_frame, i_turn_curr in enumerate(turn_list):
    
    print('movie turn %d'%i_turn_curr)


    N_rings = dict_config['N_parellel_rings']
    i_ring = int(np.mod(i_turn_curr, N_rings))
    i_iter_ring = i_turn_curr//N_rings


    ob = mfm.myloadmat_to_obj(sim_folder+'/cloud_evol_ring%d__iter%d.mat'%(i_ring, i_iter_ring))
    t_ref = ob.t[0]

    # axbup1.plot((ob.t-t_ref)/1e-9, ob.Nel_timep)
    # axbup2.plot((ob.t-t_ref), ob.lam_t_array)

    Dx = np.mean(np.diff(ob.xg_hist))

    figst.clf()
    axst = figst.add_subplot(1,1,1)
    mappable = axst.pcolormesh(ob.xg_hist*1e3, ((ob.t_hist-t_ref)/b_spac)[::N_slots_bsp], ob.nel_hist[::N_slots_bsp, :]/Dx, 
                    vmax=vmax_movie, cmap='jet', shading='gouraud')
    axst.plot(x_mat[i_turn_curr-1, :][mask_bunch]*1e3, np.arange(n_bunches), '.w', lw=2, markersize=5)
    cb=plt.colorbar(mappable, ax=axst)
    cb.set_label('Electron density [m^-3]')
    axst.set_xlim(ob.xg_hist[0]*1e3, ob.xg_hist[-1]*1e3)
    axst.set_ylim(0, n_bunches)
    axst.set_xlabel('x [mm]')
    axst.set_ylabel('Bunch passage')
    figst.subplots_adjust(bottom=.12)
    figst.suptitle('Turn %d'%i_turn_curr)


    if flag_movie:
        figst.savefig(folder_movie+'/frame_%05d.png'%i_frame, dpi=200)
    
if flag_movie:
    os.system(' '.join([
        'ffmpeg',
        '-i %s'%folder_movie+'/frame_%05d.png',
        '-c:v libx264 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,setpts=4.*PTS"',
        '-profile:v high -level:v 4.0 -pix_fmt yuv420p -crf 22 -codec:a aac movieele_%s.mp4'%tag])) 


# #down sample nel_hist
# avg_pos = []
# for ii in range(len(ob.t_hist)):


plt.show()

import sys, os
import numpy as np
import matplotlib.pyplot as plt

import numpy as np

import parse_pyparislog as ppl
import mystyle as ms
import myfilemanager as mfm

x_lim = 18e-3

sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_sey1.5'
tag = 'HL_sey1.5'
b_spac = 25e-9
N_slots_bsp = 5
flag_movie = True
movie_range = (0, 1000)
vmax_movie = 2e11
corr_turn = 1
N_turns_part = 500
N_rings = 100

# sim_folder = '../HL-LHC_coupled_bunch_450GeV_2.3e11_144b_sey1.5_both_planes'
# tag = 'HL_sey1.5_xy'
# b_spac = 25e-9
# N_slots_bsp = 5
# flag_movie = True
# movie_range = (0, 1000)
# vmax_movie = 2e11
# corr_turn = 1
# N_turns_part = 500
# N_rings = 100

i_turn = 300

obbea = mfm.myloadmat_to_obj(tag+'_matrices.mat')

x_mat = obbea.mean_x
y_mat = obbea.mean_y
n_mat = obbea.macroparticlenumber

n_turns = x_mat.shape[0]

mask_bunch = n_mat[1, :]>0
n_bunches = np.sum(mask_bunch)
bslots = np.where(mask_bunch)[0]/N_slots_bsp

plt.close('all')
ms.mystyle_arial(fontsz=16, dist_tick_lab=5)

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

axm1.plot(bslots, x_mat[i_turn, :][mask_bunch], '.-')
axm2.plot(bslots, y_mat[i_turn, :][mask_bunch], '.-')
axm3.plot(bslots, n_mat[i_turn, :][mask_bunch], '.-')

for ibef in xrange(10):
    if i_turn-ibef-1>=0:
        axm1.plot(bslots, x_mat[i_turn-ibef-1, :][mask_bunch], '--', color='k', alpha=0.5)
        axm2.plot(bslots, y_mat[i_turn-ibef-1, :][mask_bunch], '--', color='k', alpha=0.5)

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

figst = plt.figure(200, figsize=(8*1.5*1.1,6*1.1))
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
    

maxnel = None

for i_frame, i_turn_curr in enumerate(turn_list):
    
    print('movie turn %d'%i_turn_curr)


    i_part = i_turn_curr//N_turns_part
    i_ring = int(np.mod(i_turn_curr, N_rings))
    i_iter_ring = (i_turn_curr - N_turns_part * i_part)//N_rings

    try:
        ob = mfm.myloadmat_to_obj(sim_folder+'/cloud_evol_part%03d_ring%03d__iter%d.mat'%(i_part, i_ring, i_iter_ring))
    except TypeError:
        ob.nel_hist *= 0.
    t_ref = ob.t[0]

    if not flag_movie:
        axbup1.semilogy((ob.t-t_ref)/1e-9, ob.Nel_timep)
        axbup2.plot((ob.t-t_ref)/1e-9, ob.lam_t_array)

    Dx = np.mean(np.diff(ob.xg_hist))

    figst.clf()
    axst = figst.add_subplot(1,2,1)
    mappable = axst.pcolormesh(ob.xg_hist*1e3, ((ob.t_hist-t_ref)/b_spac)[::N_slots_bsp], ob.nel_hist[::N_slots_bsp, :]/Dx, 
                    vmax=vmax_movie, cmap='jet', shading='gouraud')
    axst.plot(x_mat[i_turn_curr-corr_turn, :][mask_bunch]*1e3, bslots, '.w', lw=2, markersize=5)
    cb=plt.colorbar(mappable, ax=axst)
    cb.set_label('Electron density [m^-3]')
    axst.set_xlim(-x_lim*1e3, x_lim*1e3)
    axst.set_ylim(0, np.max(bslots))
    axst.set_xlabel('x [mm]')
    axst.set_ylabel('Bunch passage')
    figst.subplots_adjust(bottom=.12, left=.07, right=0.93, wspace=.26, hspace=.34)
    figst.suptitle('Turn %d'%i_turn_curr)

    axst_xy = plt.subplot2grid(shape=(2,2), loc=(0,1), rowspan=1, colspan=1, fig=figst)
    axnel = plt.subplot2grid(shape=(2,2), loc=(1,1), rowspan=1, colspan=1, fig=figst, sharex=axst_xy)
    axst_n = axnel.twinx()

    axst_xy.plot(bslots, x_mat[i_turn_curr, :][mask_bunch]*1e3, '.-')
    
    axst_xy.grid('on')
    axnel.plot((ob.t-t_ref)/b_spac, ob.Nel_timep, 'g', lw=2)
    axst_n.plot(bslots, n_mat[i_turn_curr, :][mask_bunch], '.-r', lw=1.5, markersize=6)
    axnel.grid('on')
    
    if not maxnel:
        maxnel = np.max(ob.Nel_timep)

    for ibef in range(10):
        if i_turn_curr-ibef-1>=0:
            axst_xy.plot(bslots, x_mat[i_turn_curr-ibef-1, :][mask_bunch]*1e3, '--', color='k', alpha=0.5)

    axst_xy.set_ylim(1e3*np.array([-1., 1.])*np.max(np.abs(x_mat)))
    
    axst_n.set_ylim(np.array([0., 1.1])*np.max(np.abs(n_mat)))
    axst_n.ticklabel_format(style='sci', scilimits=(0,0),axis='y')

    axnel.set_ylim(0, maxnel*1.2)
    axnel.set_xlim(0, np.max(bslots))
    axst_xy.set_ylabel('x [mm]', color='b')
    axst_xy.tick_params(axis='y', colors='b')

    axnel.set_ylabel('N. electrons [m^-1]', color='g')
    axnel.tick_params(axis='y', colors='green')
    axst_n.set_ylabel('N. macropart.', color='r')
    axst_n.tick_params(axis='y', colors='r')
    axnel.set_xlabel('Bunch passage')
    # axnel.ticklabel_format(style='sci', scilimits=(0,0),axis='y')


    # axm3.set_ylim(np.array([0, 1.1])*np.max(np.abs(n_mat)))


    if flag_movie:
        figst.savefig(folder_movie+'/frame_%05d.png'%i_frame, dpi=200)
    
if flag_movie:
    os.system(' '.join([
        'avconv',
        '-r 10 -i %s'%folder_movie+'/frame_%05d.png',
        '-c:v libx264 -preset placebo -profile:v high -pix_fmt yuv420p -crf 22 -codec:a aac movieele_%s.mp4'%tag]))

    # os.system(' '.join([
    #     'ffmpeg',
    #     '-i %s'%folder_movie+'/frame_%05d.png',
    #     '-c:v libx264 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,setpts=4.*PTS"',
    #     '-profile:v high -level:v 4.0 -pix_fmt yuv420p -crf 22 -codec:a aac movieele_%s.mp4'%tag]))


# #down sample nel_hist
# avg_pos = []
# for ii in range(len(ob.t_hist)):


plt.show()

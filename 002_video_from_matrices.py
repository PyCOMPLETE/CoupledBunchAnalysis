import sys, os
import numpy as np
import matplotlib.pyplot as plt

import myfilemanager as mfm

tag = 'test9_on_HPC_25ns_correct'
tag = 'test11_on_HPC_25ns_more_slices'

ob = mfm.myloadmat_to_obj(tag+'_matrices.mat')

x_mat = ob.x_mat
y_mat = ob.y_mat
n_mat = ob.n_mat

n_turns = x_mat.shape[0]


folder_movie = './movie_' + tag
try:
    os.mkdir(folder_movie)
except:
    pass

plt.close('all')

figm = plt.figure(1000, figsize=(8,6*1.3))
for i_turn in xrange(n_turns):
    print('Turn %d/%d'%(i_turn,n_turns))
    
    figm.clf()
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
    
    figm.savefig(folder_movie+'/turn_%05d.png'%i_turn, dpi=200)

os.system(' '.join([
    'ffmpeg',
    '-i %s'%folder_movie+'/turn_%05d.png',
    '-c:v libx264 -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2,setpts=4.*PTS"',
    '-profile:v high -level:v 4.0 -pix_fmt yuv420p -crf 22 -codec:a aac movie_%s.mp4'%tag])) 
    
    


plt.show()

    

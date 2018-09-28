import sys, os


import numpy as np



flag_movie = True

sim_folder = '../first_test/PyPARIS/004_multibunch_with_ecloud/'
tag = 'first_sim_20b'
n_rings = 8

sim_folder = '../test_40b/'
tag = 'sim_40b'
n_rings = 10

sim_folder = '../test_20b_8kicks_12.5ns/004_multibunch_with_ecloud'
tag = 'sim_20b_8kicks'
n_rings = 5

sim_folder = '../test_20b_8kicks/004_multibunch_with_ecloud'
tag = 'sim_20b_8kicks_correct'
n_rings = 5

sim_folder = '../test_20b_8kicks_onlyH/004_multibunch_with_ecloud'
tag = 'sim_20b_8kicks_onlyH'
n_rings = 5

sim_folder = '../test_on_HPC_cluster_speed/004_multibunch_with_ecloud'
tag = 'test_on_HPC_cluster_speed'
n_rings = 40



list_files = [sim_folder+'/bunch_monitor_ring%03d.h5'%ii for ii in range(n_rings)]

import myfilemanager as mfm
dict_data = mfm.bunchh5list_to_dict(list_files)

print 'Data loaded!'

n_turns = int(np.max(dict_data['i_turn']))+1
n_bunches = int(np.max(dict_data['i_bunch']))+1

list_bunches = []
for i_bunch_obs in range(n_bunches):
    print('Bunch %d/%d'%(i_bunch_obs, n_bunches))
    dict_bunch = {kk:np.zeros(n_turns, dtype=np.float64)+np.nan for kk in dict_data.keys()}
    for ii in xrange(len(dict_data['i_bunch'])):
        if int(dict_data['i_bunch'][ii]) == int(i_bunch_obs):
            i_turn = int(dict_data['i_turn'][ii])
            for kk in dict_data.keys():
                dict_bunch[kk][i_turn] = dict_data[kk][ii]
                
    list_bunches.append(dict_bunch)

import matplotlib.pyplot as plt
plt.close('all')




plt.figure(1)
sp1 = plt.subplot(2,2,1)
sp2 = plt.subplot(2,2,2, sharex=sp1)
sp3 = plt.subplot(2,2,3, sharex=sp2)
sp4 = plt.subplot(2,2,4, sharex=sp2)

plt.figure(10)
spl = plt.subplot(1,1,1, sharex=sp2)
for i_bunch_obs in range(n_bunches):
    
    sp1.plot(list_bunches[i_bunch_obs]['mean_x'])
    sp2.plot(list_bunches[i_bunch_obs]['mean_y'])
    
    spl.plot(list_bunches[i_bunch_obs]['macroparticlenumber'])
    sp3.plot(list_bunches[i_bunch_obs]['epsn_x']*1e6, label='%d'%i_bunch_obs)
    sp4.plot(list_bunches[i_bunch_obs]['epsn_y']*1e6, label='%d'%i_bunch_obs)
    #sp4.plot(list_bunches[i_bunch_obs]['epsn_y']*1e6, '--')






sp4.legend()
sp3.legend()
#~ spf1 = plt.subplot(2,2,3)
#~ plt.plot(freq_ax, np.abs(spect_x))

#~ spf2 = plt.subplot(2,2,4, sharex=spf1)
#~ plt.plot(freq_ax, np.abs(spect_y))

plt.figure(2)
sp1 = plt.subplot(2,1,1)
plt.plot(dict_bunch['mean_z'])
sp2 = plt.subplot(2,1,2, sharex=sp1)
plt.plot(dict_bunch['sigma_z'])

x_mat = np.zeros((n_turns, n_bunches))
y_mat = np.zeros((n_turns, n_bunches))
n_mat = np.zeros((n_turns, n_bunches))

for i_bunch_obs in range(n_bunches):
    n_turns_this = len(list_bunches[i_bunch_obs]['epsn_x'])
    mask_notnan = ~np.isnan(list_bunches[i_bunch_obs]['macroparticlenumber'])
    x_mat[:n_turns_this, i_bunch_obs][mask_notnan] = list_bunches[i_bunch_obs]['mean_x'][mask_notnan]
    y_mat[:n_turns_this, i_bunch_obs][mask_notnan] = list_bunches[i_bunch_obs]['mean_y'][mask_notnan]
    n_mat[:n_turns_this, i_bunch_obs][mask_notnan] = list_bunches[i_bunch_obs]['macroparticlenumber'][mask_notnan]


plt.figure(100)
plt.pcolormesh(x_mat)

plt.figure(101)
plt.pcolormesh(y_mat)

plt.figure(102)
plt.pcolormesh(n_mat)

spect_x = np.fft.rfft(x_mat, axis=0)
spect_y = np.fft.rfft(y_mat, axis=0)
freq_ax = np.fft.rfftfreq(len(dict_bunch['mean_x']))

plt.figure(200)
plt.pcolormesh(np.arange(n_bunches),freq_ax,  np.abs(spect_x))

plt.figure(201)
plt.pcolormesh(np.arange(n_bunches),freq_ax,  np.abs(spect_y))






if flag_movie:
    folder_movie = './movie_' + tag
    try:
        os.mkdir(folder_movie)
    except:
        pass
    
    figm = plt.figure(1000, figsize=(8,6*1.3))
    for i_turn in xrange(n_turns):
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



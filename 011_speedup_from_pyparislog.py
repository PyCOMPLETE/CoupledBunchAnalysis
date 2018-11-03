import time
import numpy as np
import parse_pyparislog as ppl
import matplotlib.pyplot as plt
import mystyle as ms

na = np.array

groups = [
{
'list_folders' : [
    '../test2_on_HPC_1slot_1cores/004_multibunch_with_ecloud',
    '../test2_on_HPC_1slot_8cores/004_multibunch_with_ecloud',
    '../test2_on_HPC_1slot/004_multibunch_with_ecloud',
    '../test2_on_HPC_2slot/004_multibunch_with_ecloud',
    #'../test2_on_HPC_4slot_240cores/004_multibunch_with_ecloud',
    '../test2_on_HPC_4slot/004_multibunch_with_ecloud',
    '../test2_on_HPC_8slot/004_multibunch_with_ecloud',
    ], 'fact_HT' : 1., 'b_spac_ns':20, 'tag':'Hyper threading OFF', 'plt_vs_nreal':True,
}, 
{
'list_folders' : [
'../test4_on_HPC_1slot_1cores/004_multibunch_with_ecloud',
'../test4_on_HPC_1slot_8cores/004_multibunch_with_ecloud',
'../test4_on_HPC_1slot/004_multibunch_with_ecloud',
'../test4_on_HPC_2slot/004_multibunch_with_ecloud',
'../test4_on_HPC_4slot/004_multibunch_with_ecloud',
'../test4_on_HPC_8slot/004_multibunch_with_ecloud',
    ], 'fact_HT' : 2., 'b_spac_ns':20, 'tag':'Hyper threading ON', 'plt_vs_nreal':True,
},
#{
#'list_folders' : [
#'../test6_on_HPC_1slot_1cores/004_multibunch_with_ecloud',
#'../test6_on_HPC_1slot_8cores/004_multibunch_with_ecloud',
#'../test6_on_HPC_1slot/004_multibunch_with_ecloud',
#'../test6_on_HPC_2slot/004_multibunch_with_ecloud',
#'../test6_on_HPC_4slot/004_multibunch_with_ecloud',
#'../test6_on_HPC_8slot/004_multibunch_with_ecloud',
#    ], 'fact_HT' : 2., 'n_bunches':80, 'tag':'HT ON, no glob synch'
#},
] 


# groups = [
# {
# 'list_folders' : [
# '../test5_on_HPC_8bunches/004_multibunch_with_ecloud/',
# '../test5_on_HPC_16bunches/004_multibunch_with_ecloud/',
# '../test5_on_HPC_32bunches/004_multibunch_with_ecloud/',
# '../test5_on_HPC_64bunches/004_multibunch_with_ecloud/',
#     ],'fact_HT' :1., 'n_bunches':1, 'tag':'nbun_scan'
# },
# ] 

# groups = [
# {
# 'list_folders' : [
# '../test9bis_on_HPC_25ns_correct_be_long/004_multibunch_with_ecloud/',
# '../test10_onHPC_144b/004_multibunch_with_ecloud/',
# '../test12_onHPC_288b/004_multibunch_with_ecloud/',
#     ],'fact_HT' :1., 'n_bunches':1, 'tag':'nbun_scan', 'plt_vs_nreal':False,
# },
# ]



plt.close('all')
ms.mystyle_arial(fontsz=16, dist_tick_lab=5)
fig1 = plt.figure(1, figsize=(8,6*1.3))
fig1.set_facecolor('white')
ax1 = fig1.add_subplot(2,1,1)
ax2 = fig1.add_subplot(2,1,2, sharex=ax1)

fig10 = plt.figure(10)
fig10.set_facecolor('white')
ax10 = fig10.add_subplot(1,1,1)

fig20 = plt.figure(20)
fig20.set_facecolor('white')
ax20 = fig20.add_subplot(1,1,1)

for gg in groups:
    
    list_folders = gg['list_folders']
    fact_HT = gg['fact_HT']
    tag = gg['tag']
    #n_bunches = gg['n_bunches']
    b_spac_ns = gg['b_spac_ns']
    plt_vs_nreal = gg['plt_vs_nreal']
    
    n_cores_list = []
    avgt_turn_steps_list = []
    n_slots_list = []
    n_bunches_list = []
    for sim_folder in list_folders:

        dict_config, ibun_arr, t_arr, iturn_arr, iter_turn_steps, \
            iturn_steps, tturn_steps, n_turns_steps, avgt_turn_steps = ppl.parse_pyparislog(sim_folder+'/pyparislog.txt')

        # identify slot size
        with open(sim_folder + '/Simulation.py', 'r') as fid:
            lns = fid.readlines()
        found = True
        for ln in lns:
            if ln.startswith('b_spac_s'):
                slot_size_s = eval(ln.split('=')[-1]) 

        n_slots = np.max(ibun_arr)+1
        n_bun = n_slots*slot_size_s/(b_spac_ns*1e-9) 

        n_cores_list.append(dict_config['N_cores'])
        avgt_turn_steps_list.append(avgt_turn_steps[1])
        n_slots_list.append(n_slots)
        n_bunches_list.append(n_bun)

    speedup = 1/(np.array(avgt_turn_steps_list)/avgt_turn_steps_list[0])
    n_cores_list = np.array(n_cores_list)

    if plt_vs_nreal:
        n_cores_list[1:] = n_cores_list[1:]/fact_HT
    else:
        n_cores_list[0] = n_cores_list[0]*fact_HT
    
    gg['avgt_turn'] = na(avgt_turn_steps_list)
    

    ax1.plot(n_cores_list, speedup, '.-', label=tag, linewidth=2, markersize=10)
    ax1.set_ylabel('Speed-up')
    ax1.grid(True)
    ax2.plot(n_cores_list, na(n_slots_list)/na(n_bunches_list),'.-', label=tag, linewidth=2, markersize=10)
    ax2.grid(True)
    ax2.set_ylabel('N slots per bunch passage')

    ax10.plot(n_cores_list, np.array(avgt_turn_steps_list)/3600, '.-', label=tag, linewidth=2, markersize=10)
    ax10.set_ylabel('Time per turn [h]')
    ax10.grid(True)

    ax20.plot(n_cores_list, 1000*np.array(avgt_turn_steps_list)/3600/24, '.-', label=tag, linewidth=2, markersize=10)
    ax20.set_ylabel('Time per 1000 turns [days]')
    ax20.grid(True)
    
ax1.plot([1,max(n_cores_list)], [1,max(n_cores_list)], 'k')

for ax in [ax2, ax10, ax20]:
    ax.set_xlabel('N. CPU cores')

ax1.legend(loc='upper left', prop={'size':16}).draggable()
    
ax10.legend(loc='upper right', prop={'size':16}).draggable()
ax20.legend(loc='upper right', prop={'size':16}).draggable()

if  len(groups)>1:  
    figcomp = plt.figure(100)
    axcomp = figcomp.add_subplot(1,1,1)
    figcomp.set_facecolor('w')
    axcomp.plot(n_cores_list[1:], (groups[1]['avgt_turn']/groups[0]['avgt_turn'])[1:], '.-', linewidth=2, markersize=10)
    
    axcomp.grid(True)
    axcomp.set_ylim(1, 2)
    axcomp.set_xlabel('N. CPU cores')
    axcomp.set_ylabel('Performance ratio')

plt.show()





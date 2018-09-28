import time
import numpy as np
import parse_pyparislog as ppl

list_folders = [
'../test2_on_HPC_1slot_1cores/004_multibunch_with_ecloud',
'../test2_on_HPC_1slot_8cores/004_multibunch_with_ecloud',
'../test2_on_HPC_1slot/004_multibunch_with_ecloud',
'../test2_on_HPC_2slot/004_multibunch_with_ecloud',
#'../test2_on_HPC_4slot_240cores/004_multibunch_with_ecloud',
'../test2_on_HPC_4slot/004_multibunch_with_ecloud',
'../test2_on_HPC_8slot/004_multibunch_with_ecloud',
];fact_HT = 1.; n_bunches=80; tag='Hyper threading OFF'

# ~ list_folders = [
# ~ '../test4_on_HPC_1slot_1cores/004_multibunch_with_ecloud',
# ~ '../test4_on_HPC_1slot_8cores/004_multibunch_with_ecloud',
# ~ '../test4_on_HPC_1slot/004_multibunch_with_ecloud',
# ~ '../test4_on_HPC_2slot/004_multibunch_with_ecloud',
# ~ '../test4_on_HPC_4slot/004_multibunch_with_ecloud',
# ~ '../test4_on_HPC_8slot/004_multibunch_with_ecloud',
# ~ ]; fact_HT = 2.; n_bunches=80; tag='Hyper threading ON'

# list_folders = [
# '../test6_on_HPC_1slot_1cores/004_multibunch_with_ecloud',
# '../test6_on_HPC_1slot_8cores/004_multibunch_with_ecloud',
# '../test6_on_HPC_1slot/004_multibunch_with_ecloud',
# '../test6_on_HPC_2slot/004_multibunch_with_ecloud',
# '../test6_on_HPC_4slot/004_multibunch_with_ecloud',
# '../test6_on_HPC_8slot/004_multibunch_with_ecloud',
# ]; fact_HT = 2.

# list_folders = [
# '../test5_on_HPC_8bunches/004_multibunch_with_ecloud/',
# '../test5_on_HPC_16bunches/004_multibunch_with_ecloud/',
# '../test5_on_HPC_32bunches/004_multibunch_with_ecloud/',
# '../test5_on_HPC_64bunches/004_multibunch_with_ecloud/',
# ];fact_HT = 1.

n_cores_list = []
avgt_turn_steps_list = []
n_slots_list = []
for sim_folder in list_folders:

    dict_config, ibun_arr, t_arr, iturn_arr, iter_turn_steps, \
        iturn_steps, tturn_steps, n_turns_steps, avgt_turn_steps = ppl.parse_pyparislog(sim_folder+'/pyparislog.txt')

    n_cores_list.append(dict_config['N_cores'])
    avgt_turn_steps_list.append(avgt_turn_steps[1])
    n_slots_list.append(np.max(ibun_arr)+1)

speedup = 1/(np.array(avgt_turn_steps_list)/avgt_turn_steps_list[0])
n_cores_arr = np.array(n_cores_list)

import matplotlib.pyplot as plt

na = np.array

plt.close('all')
fig1 = plt.figure(1, figsize=(8,6*1.5))
ax1 = fig1.add_subplot(2,1,1)
ax2 = fig1.add_subplot(2,1,2, sharex=ax1)
ax1.plot(n_cores_list, speedup*fact_HT, '.-')
ax1.set_ylabel('Speed-up')
ax1.grid(True)
ax1.plot([0,640], [0,640])
ax2.plot(n_cores_list, na(n_slots_list)/n_bunches,'.-' )
ax2.grid(True)
ax2.set_ylabel('N slots per bunch passage')

fig10 = plt.figure(10)
plt.semilogy(n_cores_list, np.array(avgt_turn_steps_list)/3600, '.-')
plt.ylabel('Time per turn [h]')
plt.grid(True)

fig20 = plt.figure(20)
plt.semilogy(n_cores_list, 1000*np.array(avgt_turn_steps_list)/3600/24, '.-')
plt.ylabel('Time per 1000 turns [days]')
plt.grid(True)


fig2 = plt.figure(2)
plt.plot(n_cores_list, (speedup)/n_cores_arr, '.-')
plt.grid(True)

for fig in [fig1, fig10, fig20, fig2]:
    fig.suptitle(tag)


plt.show()





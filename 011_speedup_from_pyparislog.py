import time
import numpy as np
import parse_pyparislog as ppl

list_folders = [
'../test2_on_HPC_1slot_1cores/004_multibunch_with_ecloud',
'../test2_on_HPC_1slot_8cores/004_multibunch_with_ecloud',
'../test2_on_HPC_1slot/004_multibunch_with_ecloud',
'../test2_on_HPC_2slot/004_multibunch_with_ecloud',
'../test2_on_HPC_4slot_240cores/004_multibunch_with_ecloud',
'../test2_on_HPC_4slot/004_multibunch_with_ecloud',
'../test2_on_HPC_8slot/004_multibunch_with_ecloud',
];fact_HT = 1.

# list_folders = [
# '../test4_on_HPC_1slot_1cores/004_multibunch_with_ecloud',
# '../test4_on_HPC_1slot_8cores/004_multibunch_with_ecloud',
# '../test4_on_HPC_1slot/004_multibunch_with_ecloud',
# '../test4_on_HPC_2slot/004_multibunch_with_ecloud',
# '../test4_on_HPC_4slot/004_multibunch_with_ecloud',
# '../test4_on_HPC_8slot/004_multibunch_with_ecloud',
# ]; fact_HT = 2.

list_folders = [
'../test6_on_HPC_1slot_1cores/004_multibunch_with_ecloud',
'../test6_on_HPC_1slot_8cores/004_multibunch_with_ecloud',
'../test6_on_HPC_1slot/004_multibunch_with_ecloud',
'../test6_on_HPC_2slot/004_multibunch_with_ecloud',
'../test6_on_HPC_4slot/004_multibunch_with_ecloud',
'../test6_on_HPC_8slot/004_multibunch_with_ecloud',
]; fact_HT = 2.

# list_folders = [
# '../test5_on_HPC_8bunches/004_multibunch_with_ecloud/',
# '../test5_on_HPC_16bunches/004_multibunch_with_ecloud/',
# '../test5_on_HPC_32bunches/004_multibunch_with_ecloud/',
# '../test5_on_HPC_64bunches/004_multibunch_with_ecloud/',
# ];fact_HT = 1.

n_cores_list = []
avgt_turn_steps_list = []
for sim_folder in list_folders:

    dict_config, ibun_arr, t_arr, iturn_arr, iter_turn_steps, \
        iturn_steps, tturn_steps, n_turns_steps, avgt_turn_steps = ppl.parse_pyparislog(sim_folder+'/pyparislog.txt')

    n_cores_list.append(dict_config['N_cores'])
    avgt_turn_steps_list.append(avgt_turn_steps[1])

speedup = 1/(np.array(avgt_turn_steps_list)/avgt_turn_steps_list[0])
n_cores_arr = np.array(n_cores_list)

import matplotlib.pyplot as plt



plt.close('all')
plt.figure(1)
plt.plot(n_cores_list, speedup*fact_HT, '.-')
plt.plot([0,640], [0,640])
plt.grid(True)

plt.figure(2)
plt.plot(n_cores_list, (speedup)/n_cores_arr, '.-')
plt.grid(True)


plt.show()





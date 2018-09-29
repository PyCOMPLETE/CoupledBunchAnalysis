import numpy as np
import time

def parse_pyparislog(filename):

    with open(filename) as fid:
        pyploglns = fid.readlines()

    #check that pyparislog is proper
    flag_startsim = map(lambda s: 'PyPARIS simulation -- multiturn parallelization' in s, pyploglns)
    if np.sum(flag_startsim)!=1:
        print('sum(flag_startsim) is %d'%np.sum(flag_startsim))
        raise ValueError('Problem in pyparislog! Did you start from an empty file')

    dict_config = {}
    config_params = 'N_cores N_pieces_per_transfer N_buffer_float_size N_buffer_int_size N_parellel_rings N_nodes_per_ring'.split()
    for par in config_params:
        flag_par = map(lambda s: par+' = ' in s, pyploglns)
        assert np.sum(flag_par)==1
        i_par = np.where(flag_par)[0][0]
        dict_config[par] = int(pyploglns[i_par].split()[-1])

    t_list = []
    ibun_list = []
    iturn_list = []
    for ln in pyploglns:
        if 'iter' in ln and 'cpu' in ln and 'turn' in ln:
            t_string = ln.split(', ')[0]
            tt = time.mktime(time.strptime(t_string, "%d/%m/%Y %H:%M:%S"))
            
            if 'cpu 0.0 startin bunch' not in ln:
                raise ValueError('What?!')
                
            ibun = int(ln.split('cpu 0.0 startin bunch ')[-1].split('/')[0])
            iturn = int(ln.split('turn=')[-1])
            
            ibun_list.append(ibun)        
            t_list.append(tt)
            iturn_list.append(iturn)

    ibun_arr = np.array(ibun_list)
    t_arr = np.array(t_list)
    iturn_arr = np.array(iturn_list)

    iter_turn_steps = np.array([0] + list(np.where(np.diff(iturn_list))[0]+1))
    iturn_steps = iturn_arr[iter_turn_steps]
    tturn_steps = t_arr[iter_turn_steps] 

    n_turns_steps = list(set(np.diff(iturn_steps)))
    if len(n_turns_steps)==1:
        n_turns_steps = n_turns_steps[0]
        avgt_turn_steps = np.diff(tturn_steps)/n_turns_steps
    else:
        print('Warning: n_turns_steps is empty')
        n_turns_steps = np.nan
        avgt_turn_steps = np.nan

    return dict_config, ibun_arr, t_arr, iturn_arr, iter_turn_steps, iturn_steps, tturn_steps, n_turns_steps, avgt_turn_steps
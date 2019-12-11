import numpy as np
import matplotlib.pyplot as plt

import myfilemanager as mfm
import mystyle as ms

tags = ['HL_1.1e11_144b', 'HL_1.1e11_144b_fb']
i_bun_list = [750, 750]
labels = ['Feedback off', 'Feedback on']
fname = 'intensity_1.0e11ppb'
ylim = 7.
ylim_zoom = None

tags = ['HL_2.3e11_144b', 'HL_2.3e11_144b_fb']
i_bun_list = [175, 175]
labels = ['Feedback off', 'Feedback on']
fname = 'intensity_2.3e11ppb'
ylim = 6.
ylim_zoom = None

tags = ['HL_1.1e11_144b', 'HL_2.3e11_144b']
i_bun_list = [750, 185]
labels = ['1.1e11 ppb', '2.3e11 ppb']
fname = 'intensity_comparison'
ylim = 7.
ylim_zoom = None

tags = ['HL_2.3e11_144b', 'HL_2.3e11_144b_fb_100t', 'HL_2.3e11_144b_fb']
i_bun_list = [175, 175, 175]
labels = ['Feedback off', 'Feedback 100 turns', 'Feedback 20 turns']
fname = 'intensity_2.3e11ppb_fbturns'
ylim = 6.
ylim_zoom = 0.3

tags = ['HL_2.3e11_144b_Qp15', 'HL_2.3e11_144b_Qp15_fb']
i_bun_list = [185, 185]
labels = ['Feedback off', 'Feedback on']
fname = 'intensity_2.3e11ppb_Qp15'
ylim = 1.5
ylim_zoom = None

tags = ['HL_2.3e11_144b', 'HL_2.3e11_144b_Qp15']
i_bun_list = [185, 185]
labels = ['Q\' = 0', 'Q\' = 15']
fname = 'intensity_2.3e11ppb_Qp_comparison_nofeedback'
ylim = 6.
ylim_zoom = None

tags = ['HL_2.3e11_144b', 'HL_2.3e11_144b_Qp15', 'HL_2.3e11_144b_Qp15_fb', 'HL_2.3e11_144b_fb']
i_bun_list = [185, 185, 185, 185]
labels = ['Q\'=0, feedback off', 'Q\'=15, feedback off', 'Q\'=15, feedback on', 'Q\'=0, feedback on']
fname = 'intensity_2.3e11ppb_Qp_comparison'
ylim = 6.
ylim_zoom = 0.5

tags = ['HL_2.3e11_144b_Koct-4.5', 'HL_2.3e11_144b_Koct-4.5_fb']
i_bun_list = [185, 185]
labels = ['Feedback off', 'Feedback on']
fname = 'intensity_2.3e11ppb_Qp0_Koct-4.5'
ylim = .3
ylim_zoom = None

tags = ['HL_2.3e11_144b', 'HL_2.3e11_144b_Koct-4.5']
i_bun_list = [185, 185]
labels = ['Q\' = 0, Koct = 0', 'Q\' = 0, Koct = -4.5']
fname = 'intensity_2.3e11ppb_Qp0_Koct-4.5_comparison'
ylim = 6.
ylim_zoom = None

# tags = ['HL_2.3e11_144b', 'HL_2.3e11_144b_Qp15', 'HL_2.3e11_144b_Koct-4.5']
# i_bun_list = [185, 185, 185]
# labels = ['Q\' = 0, Koct = 0', 'Q\' = 15, Koct = 0', 'Q\' = 0, Koct = -4.5']
# fname = 'intensity_2.3e11ppb_Qp_Koct_comparison_nofeedback'
# ylim = 6.
# ylim_zoom = None

tags = ['HL_2.3e11_144b', 'HL_2.3e11_144b_Koct-4.5', 'HL_2.3e11_144b_Qp15_Koct-4.5']
i_bun_list = [185, 185, 185]
labels = ['Q\' = 0, Koct = 0', 'Q\' = 0, Koct = -4.5', 'Q\' = 15, Koct = -4.5']
fname = 'intensity_2.3e11ppb_Qp_Koct_comparison_nofeedback'
ylim = 6.
ylim_zoom = .3

tags = ['HL_2.3e11_144b', 'HL_2.3e11_144b_Koct-4.5', 'HL_2.3e11_144b_Qp15_Koct-4.5', 'HL_2.3e11_144b_Qp15_Koct-4.5_fb']
i_bun_list = [185, 185, 185, 185]
labels = ['Q\' = 0, Koct = 0', 'Q\' = 0, Koct = -4.5', 'Q\' = 15, Koct = -4.5', 'Q\' = 15, Koct = -4.5, FB on']
fname = 'intensity_2.3e11ppb_Qp_Koct_comparison'
ylim = 6.
ylim_zoom = .3

# tags = ['HL_2.3e11_144b', 'HL_2.3e11_144b_Qp15', 'HL_2.3e11_144b_Koct-4.5', 'HL_2.3e11_144b_fb']
# i_bun_list = [185, 185, 185, 185]
# labels = ['Q\' = 0, Koct = 0', 'Q\' = 15, Koct = 0', 'Q\' = 0, Koct = -4.5', 'Q\' = 0, Koct = 0, fedback on']
# fname = 'intensity_2.3e11ppb_Qp_Koct_comparison_feedback'
# ylim = 6.
# ylim_zoom = .3

# tag = 'HL_2.3e11_144b_Koct-4.5'
# tag = 'HL_2.3e11_144b_Koct-4.5_fb'

# tag = 'HL_2.3e11_144b_Qp15_Koct-4.5'
# tag = 'HL_2.3e11_144b_Qp15_Koct-4.5_fb'

# tag = 'HL_2.3e11_144b_sey1.5'
# tag = 'HL_2.3e11_144b_sey1.5_xy'

colorlist = ['#004488', '#BB5566', '#DDAA33', '#44AA99', '#AA4499', '#999933']

obs = [mfm.myloadmat_to_obj(tag+'_matrices.mat') for tag in tags]


plt.close('all')

from matplotlib import rc
rc('font', **{'family': 'sans-serif', 'sans-serif': ['arial'], 'size': 14})
# ms.mystyle_arial(fontsz=16)

fig = plt.figure(1)
ax1 = fig.add_subplot(111)

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)

fig3 = plt.figure(3)
fig3.set_facecolor('w')
ax3 = fig3.add_subplot(111)

for ii, (ob, tag) in enumerate(zip(obs, tags)):
    ax1.plot(np.max(np.abs(ob.mean_x), axis=1), label=tag)

    ax2.plot(np.argmax(np.abs(ob.mean_x), axis=1), label=labels[ii])

    ax3.plot(ob.mean_x[:, i_bun_list[ii]]*1e3,
              linewidth=1.5, color=colorlist[ii],
              label=labels[ii])


for ax in [ax1, ax2, ax3]:
    ax.legend(loc='upper left', fontsize=12)
    ax.set_xlim(0, 650)
    ax.set_xlabel('Turn')
    ax.grid('True', linestyle=':')

ax3.set_ylim(-ylim, ylim)
ax3.set_ylabel('Horizontal position [mm]')

fig3.subplots_adjust(bottom=.12, top=0.9)
fig3.suptitle(fname, fontsize=14)

fig3.savefig(fname+'.png', dpi=200)

if ylim_zoom is not None:
    ax3.set_ylim(-ylim_zoom, ylim_zoom)
    ax3.legend(loc='upper left', fontsize=12, framealpha=0.9, ncol=2)
    fig3.savefig(fname+'_zoom.png', dpi=200)

plt.show()

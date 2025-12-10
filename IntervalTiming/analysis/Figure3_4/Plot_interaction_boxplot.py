#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 14:23:46 2023

@author: va18024
"""

import pandas as pd
import numpy as np
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib as mpl
from mpl_toolkits.axisartist.axislines import Subplot
import matplotlib as mpl
import scipy.stats as stats
import matplotlib.ticker as mtick

fig = plt.figure(figsize=(14, 7))


ax_dict = fig.subplot_mosaic(
  [
        ["performance", "t_hold", "reward_lat", "trials"],#,  ],
        ["performance_delta","t_hold_delta",  "reward_lat_delta", "trials_delta"]

    ],
)


mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
plt.rcParams['axes.labelsize'] =24
plt.rcParams['axes.titlesize'] =24
plt.rcParams['ytick.labelsize'] = 18
plt.rcParams['xtick.labelsize'] =18
sns.despine()

#set paths
stage=4
SAVE = True
ex_outliers = False
manip='I.P. injections'#'infusions'#'I.P. injections'#'infusions'#
# save_path = '/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/THESIS/FIGURES/Results/'


orange = (0.9,0.38,0)
blue = (93/255, 58/255, 155/255)

from matplotlib.patches import PathPatch

def adjust_box_widths(g, fac):
    """
    Adjust the withs of a seaborn-generated boxplot.
    """

    # iterating through Axes instances
    for ax in g.axes:

        # iterating through axes artists:
        for c in ax.get_children():

            # searching for PathPatches
            if isinstance(c, PathPatch):
                # getting current width of box:
                p = c.get_path()
                verts = p.vertices
                verts_sub = verts[:-1]
                xmin = np.min(verts_sub[:, 0])
                xmax = np.max(verts_sub[:, 0])
                xmid = 0.5*(xmin+xmax)
                xhalf = 0.5*(xmax - xmin)

                # setting new width of box
                xmin_new = xmid-fac*xhalf
                xmax_new = xmid+fac*xhalf
                verts_sub[verts_sub[:, 0] == xmin, 0] = xmin_new
                verts_sub[verts_sub[:, 0] == xmax, 0] = xmax_new

                # setting new width of median line
                for l in ax.lines:
                    if np.all(l.get_xdata() == [xmin, xmax]):
                        l.set_xdata([xmin_new, xmax_new])
                        
                        
def plot_box_violin(test, variable, ax):
    if variable not in ['performance', 'trials']:
        test[variable] =test[variable]/100

    test['group_manip'] = test['group'] + "_" + test['manipulation']
    sns.boxplot(data=test, x="group", y= variable,
                      hue="manipulation", hue_order=['VEH', 'CNO'], dodge=True,gap =0.1, width=.8, linecolor = 'k',  palette=my_colors, ax=ax)#, showcaps=False, fliersize=3, zorder=2, dodge=True, ax=ax)  # Overlay boxplot
    
  
    ms =6
    alpha  = 0.9
    c_dots = 'k'#(0.5, 0.5, 0.5)
    for i in test.rat.unique():
        dfq = test.query('rat == @i').reset_index()

        if len(dfq)>1:
            if dfq['group'].unique()=='C':
                ax.plot([-0.2, 0.2], [dfq[variable][1], dfq[variable][0]], 'k-', linewidth=.8)
                ax.plot([-0.2], [dfq[variable][1]], 'o', color = c_dots, markersize = ms, alpha = alpha)
                ax.plot([0.2], [dfq[variable][0]], 'o',color = c_dots, markersize = ms, alpha = alpha)


        
            else:
                ax.plot([0.8, 1.2], [dfq[variable][1], dfq[variable][0]], 'k-', linewidth=.8)
                ax.plot([0.8], [dfq[variable][1]], 'o', color = c_dots, markersize = ms, alpha = alpha)
                ax.plot([1.2], [dfq[variable][0]], 'o', color = c_dots, markersize = ms, alpha = alpha)
        else:
            if dfq['group'].unique()=='C':

                ax.plot([0.2], dfq[variable][0], 'o', color = c_dots, markersize = ms, alpha = alpha)
            else:
                ax.plot([1.2], dfq[variable][0], 'o',color = c_dots, markersize = ms, alpha = alpha)

         


    old_len_collections = len(ax.collections)

                
    legend = ax.legend()
    legend.remove()


def cohen_d(x, y):
    diff = np.mean(y) - np.mean(x)
    pooled_std = np.sqrt((np.std(y, ddof=1)**2 + np.std(x, ddof=1)**2) / 2)
    return diff / pooled_std

# Bootstrapping function to estimate Cohen's d with confidence intervals
def bootstrap_cohen_d(x, y, n_bootstraps=1000, conf_level=0.95):
    boot_d = []
    for _ in range(n_bootstraps):
        x_resample = np.random.choice(x, size=len(x), replace=True)
        y_resample = np.random.choice(y, size=len(y), replace=True)
        boot_d.append(cohen_d(x_resample, y_resample))
    
    # Calculate confidence intervals
    lower_bound = np.percentile(boot_d, (1 - conf_level) / 2 * 100)
    upper_bound = np.percentile(boot_d, (1 + conf_level) / 2 * 100)
    
    return np.mean(boot_d), lower_bound, upper_bound, boot_d
            
    
def plot_delta(test, variable, ax):
    if variable not in ['performance', 'trials']:
        test[variable] =test[variable]*1000
    delta_value_C = np.zeros((len(np.unique(test['rat'][test.group=='C']))))
    delta_value_D = np.zeros((len(np.unique(test['rat'][test.group=='D']))))
    c_idx =0
    d_idx=0
    
    for idx, rat in enumerate(test.rat.unique()):
        if np.unique(test['group'][test.rat ==rat])=='C':
            delta_value_C[c_idx] = -test[variable][(test.rat ==rat)].diff()[-1:] #& (test.manipulation == 'CNO')] - test['t_hold'][(test.rat ==rat) & (test.manipulation == 'VEH')]
            c_idx+=1
            print(c_idx)
        elif np.unique(test['group'][test.rat ==rat])=='D':
            delta_value_D[d_idx] = -test[variable][(test.rat ==rat)].diff()[-1:]
            d_idx+=1
            
            
    ax.errorbar([0, 2], [np.mean(delta_value_C), np.mean(delta_value_D)], yerr = [stats.sem(delta_value_C), stats.sem(delta_value_D)], fmt='k.', capsize = 10)
        
            
    ax.plot([0, 2], [np.mean(delta_value_C),np.mean(delta_value_D)], 'k.', markersize = 10)
    # ax.plot([0, 0], [c_ci_lower, c_ci_upper], '-')
    # ax.plot([1, 1], [d_ci_lower, d_ci_upper], '-')
    
def add_sig_bar(ax, x1, x2, y, text, line_height=0.03, fontsize=24):
    """
    Draw a horizontal significance bar between x1 and x2 at height y,
    with the given text (e.g. '*', '**', 'n.s.').
    line_height controls the small vertical offset of the bar.
    """
    # draw connecting line
    ax.plot([x1, x1, x2, x2],
            [y, y + line_height, y + line_height, y],
            lw=1.5, c='k')
    # add centered text above line
    ax.text((x1 + x2) / 2, y + line_height * 1.3, text,
            ha='center', va='bottom',
            fontsize=fontsize, fontweight='bold')


    
        
def adjust_lightness(color, amount=0.1):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])
#script to plot 
#concatenate data from the correct sessions 


if stage==3:
    path_to_batch1 = r"PATHTOFOLDER\IntervalTiming\data_csv\Batch1_Stage_3.xls""
    path_to_batch2= r"PATHTOFOLDER\IntervalTiming\data_csv\Batch2_Stage_3.xls"

    

elif stage==4:
    path_to_batch1= r"PATHTOFOLDER\IntervalTiming\data_csv\Batch2_Stage_3.xls"
    
    path_to_batch2= r"PATHTOFOLDER\IntervalTiming\data_csv\Batch2_Stage_4.xls"
#get data

batch1 = pd.read_excel(path_to_batch1)
batch2 = pd.read_excel(path_to_batch2)
if stage ==3:
    if manip =='I.P. injections':
        batch1_sub = batch1[(batch1['Session_date']>20210510) & (batch1['Session_date']<20210513)]
    else:
        batch1_sub = batch1[(batch1['Session_date']>20210519) & (batch1['Session_date']<20210521)]
    batch1_sub=batch1_sub.replace(regex='BASE', value ='VEH')
    batch2_sub = batch2[batch2['manipulation_type']==manip]
elif stage==4:
    batch1_sub = batch1[batch1['manipulation_type']==manip]
    batch2_sub = batch2[batch2['manipulation_type']==manip]
    
# =============================================================================
#     dataframe containing all data 
# =============================================================================
df =pd.concat([batch1_sub, batch2_sub], ignore_index=True)
# to exclude potential outliers 
if ex_outliers:
    print('excluding outliers')
    df=df[(df['rat']!='TITET_19') & (df['rat']!='TITET_20')]
if manip =='infusions':
    df=df[(df['rat']!='TITET_4') & (df['rat']!='TITET_21')]

print(len(df))

(0.1, 0.2, 0.5, 0.5) 
my_colors = {'CNO': orange, 'VEH': (1/2,1/2,1/2)}#, 'D_CNO': blue, 'D_VEH': (1/2,1/2,1/2)}
my_colors2 = {'CNO': (1,1,1), 'VEH': (1,1,1)}

# my_cs=['gray', orange]


#subdataset for performance
df_sub = df[(df["reward"]==1)]   
test=df_sub.groupby( ['group', 'rat', 'manipulation'] )['reward'].sum().to_frame(name = 'reward').reset_index()
test1=df_sub.groupby( ['group', 'rat', 'manipulation'] )['trials'].max().to_frame(name = 'trials').reset_index()
test['performance'] = test['reward']/test1['trials']*100
test['group_manip'] = test['group'] + "_" + test['manipulation']


variable = 'trials'
ax = ax_dict[variable]
plot_box_violin(test1, variable, ax)
# --- Recolor only the EGFP–CNO box ---
# seaborn box order: [EGFP–VEH, EGFP–CNO, hM4D–VEH, hM4D–CNO]
boxes = [p for p in ax.patches if isinstance(p, mpl.patches.PathPatch)]
if len(boxes) >= 2:
    boxes[2].set_facecolor(blue)  # purple, adjust to your liking
    boxes[2].set_edgecolor('k')
ax.set_xlabel('')
ax.set_ylabel('trials')
ax.set_xticklabels(('EGFP', 'hM4D(Gi)'))

ax = ax_dict['trials_delta']
plot_delta(test1, variable, ax)
ax.set_xlabel('')
ax.set_xticks([0, 2])
ax.set_xlim([-1, 3])
ax.set_ylabel('\u0394 (trials)')

ax.set_xticklabels(('EGFP', 'hM4D(Gi)'))

# ax.set_ylim([-0.7, 0.7])

variable = 'performance'
ax = ax_dict[variable]
plot_box_violin(test, variable, ax)
boxes = [p for p in ax.patches if isinstance(p, mpl.patches.PathPatch)]
if len(boxes) >= 2:
    boxes[2].set_facecolor(blue)  # purple, adjust to your liking
    boxes[2].set_edgecolor('k')
ax.set_xlabel('')
ax.set_ylabel('Performance (%)')
ax.set_xticklabels(('EGFP', 'hM4D(Gi)'))

ax = ax_dict['performance_delta']
plot_delta(test, variable, ax)
ax.set_xlabel('')
# ax.set_ylabel('\u0394')
ax.set_xticks([0, 2])
ax.set_xlim([-1, 3])
# ax.set_ylim([-0.7, 0.7])

ax.set_xticklabels(('EGFP', 'hM4D(Gi)'))
ax.set_ylabel('\u0394 (%)')



#subdataset for exit time
variable = 't_hold'
ax = ax_dict[variable]

    
df_sub = df[(df["reward"]>-1) & (df['t_hold']>20)  & (df['t_hold']<=450)]   
test=df_sub.groupby( ['group', 'rat', 'manipulation'] )['t_hold'].mean().to_frame(name = 't_hold').reset_index()


plot_box_violin(test, variable, ax)
boxes = [p for p in ax.patches if isinstance(p, mpl.patches.PathPatch)]
if len(boxes) >= 2:
    boxes[2].set_facecolor(blue)  # purple, adjust to your liking
    boxes[2].set_edgecolor('k')
ax.set_xlabel('')
ax.set_ylabel('exit time (s)')
ax.set_xticklabels(('EGFP', 'hM4D(Gi)'))


variable = 't_hold'
ax = ax_dict['t_hold_delta']

plot_delta(test, variable, ax)
ax.set_xlabel('')

# ax.set_ylabel('cohen\'s d')
ax.set_xticks([0, 2])
ax.set_xlim([-1, 3])
# ax.set_ylim([-0.7, 0.7])
ax.set_ylabel('\u0394 (ms)')


ax.set_xticklabels(('EGFP', 'hM4D(Gi)'))

groups = ['C', 'D']
manips = ['CNO', 'VEH']

for i, group in enumerate(groups):
    for j, manip in enumerate(manips):
        n = len(test[(test.group ==group) & (test.manipulation == manip)])
        print("n= {} in the {} group during {}".format(n, group, manip))
        

ax.set_xticklabels(('EGFP', 'hM4D(Gi)'))


# plot for reward latency
variable = 'reward_lat'
ax = ax_dict[variable]

df_sub = df[(df["reward_lat"]>0)]   
test=df_sub.groupby( ['group', 'rat', 'manipulation'] )['reward_lat'].mean().to_frame(name = 'reward_lat').reset_index()

plot_box_violin(test, variable, ax)
boxes = [p for p in ax.patches if isinstance(p, mpl.patches.PathPatch)]
if len(boxes) >= 2:
    boxes[2].set_facecolor(blue)  # purple, adjust to your liking
    boxes[2].set_edgecolor('k')
ax.set_xlabel('')
ax.set_ylabel('reward latency (s)')
# ax.set_ylabel('\u0394 (s)')

ax.set_xticklabels(('EGFP', 'hM4D(Gi)'))


ax = ax_dict['reward_lat_delta']
plot_delta(test, variable, ax)
ax.set_xlabel('')
ax.set_xticks([0, 2])
ax.set_xlim([-1, 3])
ax.set_ylabel('\u0394 (ms)')

ax.set_xticklabels(('EGFP', 'hM4D(Gi)'))


# ax = ax_dict['trials_delta']
# plot_delta(test, variable, ax)
# ax.set_xlabel('')
# ax.set_xticks([0, 2])
# ax.set_xlim([-1, 3])
# ax.set_ylabel('\u0394 (trials)')


ax.set_xticklabels(('EGFP', 'hM4D(Gi)'))


if stage ==3: 
    # --- Performance Δ subplot ---
    ax = ax_dict['performance_delta']
    add_sig_bar(ax, 0, 2, 5, 'n.s.')       # EGFP
    
    # --- Exit time Δ subplot ---
    ax = ax_dict['t_hold_delta']
    add_sig_bar(ax, 0, 2, 200, '***')       # EGFP
    
    
    # --- Reward latency Δ subplot ---
    ax = ax_dict['reward_lat_delta']
    add_sig_bar(ax, 0, 2, 140, '***')       # EGFP
    
    
    # --- Trials Δ subplot ---
    ax = ax_dict['trials_delta']
    add_sig_bar(ax, 0, 2, 5, '*')       # EGFP
    
else: 
    # --- Performance Δ subplot ---
    ax = ax_dict['performance_delta']
    add_sig_bar(ax, 0, 2, 5, '*')       # EGFP
    
    # --- Exit time Δ subplot ---
    ax = ax_dict['t_hold_delta']
    add_sig_bar(ax, 0, 2, 100, '***')       # EGFP
    
    
    # --- Reward latency Δ subplot ---
    ax = ax_dict['reward_lat_delta']
    add_sig_bar(ax, 0, 2, 100, '***')       # EGFP
    
    
    # --- Trials Δ subplot ---
    ax = ax_dict['trials_delta']
    add_sig_bar(ax, 0, 2, 5, 'n.s.')       # EGFP
    


 
plt.tight_layout()
plt.show()




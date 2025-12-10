#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 16:04:20 2022

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
from scipy import stats
from matplotlib.patches import Rectangle
from scipy.stats import gaussian_kde

path = r"PATHTOFOLDER\IntervalTiming\data_csv\Batch1_Stage_3.xls"
path = r"PATHTOFOLDER\IntervalTiming\data_csv\Batch2_Stage_3.xls"

df1 = pd.read_excel(path)
df2 = pd.read_excel(path2)

training_session = 6
df1_sub = df1[(df1['Session_date']==sorted(df1['Session_date'].unique())[training_session])] #20210507
df2_sub= df2[(df2['Session_date']==sorted(df2['Session_date'].unique())[6])] #20220113
df =pd.concat([df1_sub, df2_sub], ignore_index =True)

dat = df[(df['reward'] > -1) & (df['t_hold'] > 20)].copy()
dat['t_hold'] = dat['t_hold'] / 100
# Label trial type

dat['manipulation'] = dat['manipulation'].replace({'VEH': 'vehicle'})
dat['group'] = dat['group'].replace({'C': 'EGFP'})
dat['group'] = dat['group'].replace({'D': 'hM4D(Gi)'})



#######PLOT DABEST

import dabest
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Define colors per group
group_colors = {
    'hM4D(Gi)': (0.9,0.38,0),   # blue-ish
    'EGFP': (0.365, 0.227, 0.608)    # orange-ish
}



# Compute per-rat means
subj_means = (
    dat.groupby(['rat', 'group'])['t_hold']
    .mean()
    .reset_index()
)

import dabest

dabest_obj = dabest.load(
    data=subj_means,
    x='group',
    y='t_hold',
    idx=('EGFP', 'hM4D(Gi)'),
    resamples=5000,
    random_seed=42
)
# Create a new axes outside the mosaic for DABEST plot
# dabest_ax = fig.add_axes([0.75, 0.55, 0.22, 0.35])  # [left, bottom, width, height]

fig = plt.figure(figsize=(8, 6))

dabest_obj.mean_diff.plot(
    raw_marker_size=0,
    contrast_label='Δ (hM4D(Gi)− EGFP)',
    custom_palette=group_colors
)
plt.ylabel("Exit time (s)")



plt.tight_layout()
plt.show()


# Extract DABEST stats
dabest_stats = dabest_obj.mean_diff.statistical_tests.iloc[0]
mean_diff = float(dabest_stats["difference"])
ci_low = float(dabest_stats["bca_low"])
ci_high = float(dabest_stats["bca_high"])
p_value = float(dabest_stats["pvalue_permutation"])

# Format stats string
stats_text = (
    f"Δ = {mean_diff:.3f} s\n"
    f"95% CI: [{ci_low:.3f}, {ci_high:.3f}] s\n"
    f"p = {p_value:.3g}"
)


### Plot normal plot
fig = plt.figure(figsize=(10,4))

fig.text(
    0.76, 0.48, stats_text,
    fontsize=12,
    ha='left',
    va='top',
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.9)
)
# ax_dict = fig.subplot_mosaic(
#     [
#         ["Averages",  "Control", "Weber"],
#          ["Averages","Control", "Weber"]
    
#     ],
# )

ax_dict = fig.subplot_mosaic(
    [
        [ "Averages", "Averages", "Control", "Control",  "Weber", "Weber" ],
         ["Averages","Averages","Control",  "Control", "Weber", "Weber" ],
         ["Averages","Averages","Control",  "Control", "Weber", "Weber" ], 
         ["Averages","Averages","Control",  "Control", "Weber", "Weber" ]
    
    ],
)

mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
plt.rcParams['axes.labelsize'] =20
plt.rcParams['axes.titlesize'] =18
plt.rcParams['ytick.labelsize'] =16
plt.rcParams['xtick.labelsize'] =16

C_mean=np.zeros((10))
C_std=np.zeros((10))


D_mean=np.zeros((10))
D_std=np.zeros((10))
column_n='group_id'

c=0
d=0
gray= [0.35, 0.73, 0.49]
CUMU = True

# ax_dict["A"].axis("off")

for idx, group in enumerate(sorted(df[column_n].unique())):

    # plt.figure()
    axes=ax_dict['Control']
    # plt.title(group)
    df_base1=df[(df[column_n]==group) &(df['reward']>-1)& (df['t_hold']>20)]
    df_base1['t_hold']=df_base1['t_hold']/100
    #df_base2=df[(df[column_n]==group) & (df['reward']>-1) & (df['t_hold']>10) & (df['manipulation_type']=='BASE') & (df['Session_date']==20210519)]
    if group[0]=='C':
        #axes=ax_dict["Control"]
        t=sns.kdeplot(data=df_base1, x="t_hold", color=(93/255, 58/255, 155/255), ax=axes, cumulative=CUMU, lw=0.9, linestyle="-")

        # x = t.lines[len(t.lines)-1].get_xdata() # Get the x data of the distribution
        # y = t.lines[len(t.lines)-1].get_ydata() # Get the y data of the distribution
        # maxid = np.argmax(y)
        #axes.plot([x[maxid], x[maxid]], [0, 0.016], '--g', alpha=.2)
        C_mean[c]=np.mean(df_base1['t_hold'])
        C_std[c]=np.std(df_base1['t_hold'])
        c+=1
        print(c)
        #sns.distplot(df_base1['t_hold'], color='g', bins=np.arange(0, 500, 100), ax=axes, rug=False, hist=False)
    elif group[0]=='D':
        #axes=ax_dict["Control"]
        t=sns.kdeplot(data=df_base1, x="t_hold", color=(0.9,0.38,0), ax=axes, cumulative=CUMU, lw=0.9, linestyle="-")
        # x = t.lines[len(t.lines)-1].get_xdata() # Get the x data of the distribution
        # y = t.lines[len(t.lines)-1].get_ydata() # Get the y data of the distribution
        # maxid = np.argmax(y)
        #axes.plot([x[maxid], x[maxid]], [0, 0.016], '--r', alpha=.2)    
        D_mean[d]=np.mean(df_base1['t_hold'])
        D_std[d]=np.std(df_base1['t_hold'])
        d+=1
        print(d)
    axes.set_xlabel(' ')
    axes.set_ylabel(' ')

    axes.set_xlim([0, 4.50])
    axes.set_ylim([0, 1.05])


    legendEnt2 = 'BASE ' + '(n=' + str(len(df_base1['t_hold']))+')'

ax_dict["Control"].plot([2.50, 2.50], [0, 1.9], color=gray, alpha=0.6, label='Target duration')

# Create a Rectangle patch
rect = Rectangle((2.25, 0),1.25,1.3,linewidth=1,edgecolor='none',facecolor=gray, alpha =0.3)

# Add the patch to the Axes
ax_dict["Averages"].add_patch(rect)

rect = Rectangle((2.25, 0),1.25,1.9,linewidth=1,edgecolor='none',facecolor=gray, alpha =0.3)

ax_dict["Control"].add_patch(rect)



ax_dict["Control"].set_xticks([0, 1.00, 2.00, 3.00, 4.00, 5.00])
ax_dict["Control"].set_xticklabels(['0', '1','2', '3', '4', '5'])

ax_dict["Averages"].set_xlabel(' ')
axes = ax_dict["Averages"]
axes.set_xlabel(' ')
axes.set_ylabel(' ')

axes.set_xlim([0, 4.50])
axes.set_ylim([0, 1.05])




dat= df[(df['reward']>-1)& (df['t_hold']>20) & (df['t_hold']<=450)]
dat['t_hold']=dat['t_hold']/100
axes=ax_dict["Averages"]
axes.sharex(ax_dict['Control'])
b=sns.kdeplot(data=dat, x="t_hold", color=(0,0,0), ax=axes, cumulative=CUMU, lw=2, linestyle="-")


kde = gaussian_kde(dat['t_hold'])
x_vals = np.linspace(min(dat['t_hold']), max(dat['t_hold']), 1000)
kde_vals = kde(x_vals)

# Find the peak
peak_x = x_vals[np.argmax(kde_vals)]
peak_y = max(kde_vals)



axes.set_xticks([0, 1.00, 2.00, 3.00, 4.00, 5.00])
axes.set_xticklabels(['0', '1','2', '3', '4', '5'])

axes.set_xlabel(' ')

axes.set_ylabel('cumulative probability', fontsize = 15)
axes.legend(loc='upper left', fontsize=2)
#ax_dict["Averages"].fill_between([225, 350], 0, 0.014,
        #facecolor=gray, alpha=0.2)
ax_dict["Averages"].plot([2.50, 2.50], [0, 1.3], color=gray, alpha=0.6, label='target')

ax_dict["Averages"].legend(frameon=False, fontsize=2, loc='upper left', ncol=1)

all_mean = np.concatenate((C_mean, D_mean))
all_std = np.concatenate((C_std, D_std))

axes.set_aspect('equal')
ax_dict["Averages"].set_aspect('auto')
ax_dict["Control"].set_aspect('auto')

plt.tight_layout()



fig.text(1.3, -0.2, 'exit time (s)', transform=ax_dict["Averages"].transAxes,
        fontsize=16, va='top', ha='right')


# Add the patch to the Axes

plt.tight_layout()


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mean ± SD raw data with dabest contrasts.
@author: va18024
"""

import matplotlib.pyplot as plt
import seaborn as sns
import dabest
import numpy as np
import pandas as pd
import matplotlib as mpl
import io
from PIL import Image

# ----------------------------
# Plot style
# ----------------------------
plt.rcParams['axes.labelsize'] = 24
plt.rcParams['axes.titlesize'] = 18
sns.set_style("ticks")

label_size = 18
mpl.rcParams['xtick.labelsize'] = 16
mpl.rcParams['ytick.labelsize'] = 16
mpl.rcParams['axes.labelsize'] = label_size 
mpl.rcParams['axes.linewidth'] = 3
mpl.rcParams['xtick.major.size']=4
mpl.rcParams['ytick.major.size']=4
mpl.rcParams['ytick.major.width']=1
mpl.rcParams['xtick.major.width']=1
mpl.rcParams['lines.linewidth']=2
mpl.rcParams['lines.markersize']=5
mpl.rcParams["legend.borderpad"] = 0.5

# ----------------------------
# Load data
# ----------------------------
path =r"C:\Users\eboven\OneDrive - Erasmus MC\Documents\PhD\Data\TITET\Batch2_stage_4.xls"
path_2 = r"C:\Users\eboven\OneDrive - Erasmus MC\Documents\PhD\Data\TITET\Batch1_stage_4.xls"



df2_a = pd.read_excel(path)
df1_a = pd.read_excel(path_2)
df_all = pd.concat([df1_a, df2_a])

df = df_all[df_all['manipulation_type'] == 'I.P. injections'].copy()
df['t_hold'] = df['t_hold'] / 100
df['manipulation'] = df['manipulation'].replace({'VEH': 'vehicle'})

# ----------------------------
# Group/trial setup
# ----------------------------
group_names = ['EGFP', 'hM4D(Gi)']
trial_names = ['cued', 'uncued']
groups = ['C', 'D']
trial_types = [1, 2]

images = []


orange = (0.9,0.38,0)
blue = (93/255, 58/255, 155/255)


# ----------------------------
# Loop over conditions
# ----------------------------
for group in groups:
    if group == 'C':
        my_colors = {'CNO': (0.365, 0.227, 0.608), 'vehicle': (0.5, 0.5, 0.5)}
        group_name = group_names[0]
    else:
        my_colors = {'CNO': (0.9, 0.38, 0), 'vehicle': (0.5, 0.5, 0.5)}
        group_name = group_names[1]

    for trial_type in trial_types:
        df_sub = df[
            (df['group'] == group) &
            (df['trial'] == trial_type) &
            (df['reward'] > -1)
        ].copy()

        if df_sub['manipulation'].nunique() < 2:
            continue

        dabest_obj = dabest.load(
            data=df_sub,
            x='manipulation',
            y='t_hold',
            idx=('vehicle', 'CNO'),
            resamples=5000,
            random_seed=42
        )

        fig = dabest_obj.mean_diff.plot(
            raw_marker_size=0,
            raw_label='exit time (s)',
            swarm_side = 'center',
            contrast_label='Δ (CNO − vehicle)',
            fig_size=(6, 4),
            custom_palette=my_colors
        )
        
        # -------------------------------------------------------
        # CLEAN UP DEFAULT DABEST LAYERS
        # -------------------------------------------------------
        raw_ax, contrast_ax = fig.axes
        
        # --- Left: remove shaded bars and connector lines
        for patch in raw_ax.patches:
            patch.set_visible(False)
        
        for line in raw_ax.lines:
            if line.get_linewidth() < 3:
                line.set_visible(False)
        
        # --- Right: remove contrast bars, connector lines, and effect-size text
        for patch in contrast_ax.patches:
            patch.set_visible(False)
        for line in contrast_ax.lines:
            if line.get_linewidth() < 3:
                line.set_visible(False)
        for txt in contrast_ax.texts:
            txt.set_visible(False)  # removes +0.04 etc.
            


        # ---- Replace raw swarm with mean ± SD ----

            
        # ---- Replace raw swarm with mean ± SD ----
        # enforce same order as dabest idx
        order = ['vehicle', 'CNO']
        group_stats = (
            df_sub.groupby("manipulation")["t_hold"]
            .agg(['mean', 'std'])
            .reindex(order)        # <- ensure vehicle = 0, CNO = 1
            .reset_index()
        )
        
        for i, row in group_stats.iterrows():
            mean = row['mean']
            sd = row['std']
            x = i  # 0=vehicle, 1=CNO
        
            raw_ax.errorbar(
                x, mean, yerr=sd,
                fmt='o',                        # circle for mean
                color=my_colors[row['manipulation']],
                ecolor=my_colors[row['manipulation']],
                elinewidth=2, capsize=6, capthick=2, markersize=10
            )


        # Axis labels/limits
        raw_ax.set_ylabel("exit time (s)", fontsize=14)
        raw_ax.set_ylim([1.7, 3.2])
        contrast_ax.set_ylim([-0.5, 0.5])

        # Title
        trial_type_name = trial_names[trial_type - 1]
        fig.suptitle(f"{group_name} | {trial_type_name}", fontsize=14)
        fig.tight_layout()

        # Save to buffer as image
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        img = Image.open(buf)
        images.append(img)

        plt.close(fig)

# ----------------------------
# Combine all into 2×2 panel
# ----------------------------
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

for i, ax in enumerate(axs.flat):
    if i < len(images):
        ax.imshow(images[i])
        ax.axis('off')
    else:
        ax.remove()

plt.tight_layout()
# plt.savefig(r'C:\Users\eboven\OneDrive - Erasmus MC\Documents\PhD\CodeOutput\Figure4\Figure6_DABEST_mean_SD.svg')

plt.show()

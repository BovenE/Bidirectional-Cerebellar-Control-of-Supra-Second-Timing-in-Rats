#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage 3 baseline DABEST plot with mean ± SD, dot at mean, and larger fonts.
"""

import pandas as pd
import matplotlib.pyplot as plt
import dabest

# ==========================
# Load and preprocess data
# ==========================

path1 = r"PathtoData\Figure2\Panel_B-D_IntervalTiming\data\Batch1_predictabletimecue.xls"
path2 = r"PathtoData\Figure2\Panel_B-D_IntervalTiming\data\Batch2_predictabletimecue.xls"


df1 = pd.read_excel(path1)
df2 = pd.read_excel(path2)

# Pick one training session from each batch
training_session = 6
df1_sub = df1[df1['Session_date'] == sorted(df1['Session_date'].unique())[training_session]]
df2_sub = df2[df2['Session_date'] == sorted(df2['Session_date'].unique())[training_session]]

df = pd.concat([df1_sub, df2_sub], ignore_index=True)

# Filter and clean
dat = df[(df['reward'] > -1) & (df['t_hold'] > 20)].copy()
dat['t_hold'] = dat['t_hold'] / 100  # convert to seconds

# Rename labels for clarity
dat['manipulation'] = dat['manipulation'].replace({'VEH': 'vehicle'})
dat['group'] = dat['group'].replace({'C': 'EGFP', 'D': 'hM4D(Gi)'})

# ==========================
# Aggregate per-rat means
# ==========================
subj_means = (
    dat.groupby(['rat', 'group'])['t_hold']
    .mean()
    .reset_index()
)

# ==========================
# Define colors
# ==========================
group_colors = {
    'EGFP': (0.365, 0.227, 0.608),
    'hM4D(Gi)': (0.9, 0.38, 0),
}

# ==========================
# DABEST analysis
# ==========================
dabest_obj = dabest.load(
    data=subj_means,
    x='group',
    y='t_hold',
    idx=('EGFP', 'hM4D(Gi)'),
    resamples=5000,
    random_seed=42
)
mean_diff = dabest_obj.mean_diff

# Display summary (includes p-value)
print(mean_diff)
p_value = mean_diff.results['pvalue_permutation']

print(p_value)
# ==========================
# Plot with DABEST
# ==========================
fig = dabest_obj.mean_diff.plot(
    raw_marker_size=6,  # hide individual datapoints
    contrast_label='Δ (hM4D(Gi) − EGFP)',
    custom_palette=group_colors,
    fig_size=(8, 6)
)

plt.ylabel('exit time (s)')

# Access axes
raw_ax, contrast_ax = fig.axes

# ==========================
# Overlay mean ± SD with dot
# ==========================
for i, g in enumerate(['EGFP', 'hM4D(Gi)']):
    values = subj_means.loc[subj_means['group'] == g, 't_hold']
    mean_val = values.mean()
    sd_val = values.std()

    # Error bar (mean ± SD)
    raw_ax.errorbar(
        i, mean_val,
        yerr=sd_val,
        fmt='none',
        ecolor=group_colors[g],
        elinewidth=2,
        capsize=6,
        zorder=4
    )

    # Dot at the mean
    raw_ax.scatter(
        i, mean_val,
        color=group_colors[g],
        s=80,
        zorder=5,
        edgecolor='k',
        linewidth=1.2
    )

    # Text annotation above the error bar
    raw_ax.text(
        i, mean_val + sd_val + 0.05,
        f"{mean_val:.3f}",
        ha='center', va='bottom',
        fontsize=12, fontweight='bold'
    )

# ==========================
# Make labels and ticks bigger
# ==========================
raw_ax.set_xlabel("group", fontsize=18, labelpad=10)
raw_ax.set_ylabel("exit time (s)", fontsize=18, labelpad=10)
contrast_ax.set_xlabel("contrast", fontsize=18, labelpad=10)
contrast_ax.set_ylabel("Δ (hM4D(Gi) − EGFP)", fontsize=18, labelpad=10)

raw_ax.tick_params(axis='both', labelsize=16)
contrast_ax.tick_params(axis='both', labelsize=16)


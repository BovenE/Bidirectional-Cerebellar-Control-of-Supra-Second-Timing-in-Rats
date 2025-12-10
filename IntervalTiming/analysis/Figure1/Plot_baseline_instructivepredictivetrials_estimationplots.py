#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stage 4 baseline DABEST plot with mean ± SD, subject-level points (jittered),
annotations, and larger axis fonts.
"""

import pandas as pd
import matplotlib.pyplot as plt
import dabest
import numpy as np

# ==========================
# Load and preprocess data
# ==========================
path = r"C:\Users\eboven\OneDrive - Erasmus MC\Documents\PhD\Data\TITET\Batch1_Stage_4.xls"
path2= r"C:\Users\eboven\OneDrive - Erasmus MC\Documents\PhD\Data\TITET\Batch2_Stage_4.xls"
df1 = pd.read_excel(path1)
df2 = pd.read_excel(path2)

# Select training session
df1_sub = df1[df1['Session_date'] == sorted(df1['Session_date'].unique())[6]]   # e.g. 20210611
df2_sub = df2[df2['Session_date'] == sorted(df2['Session_date'].unique())[11]]  # e.g. 20220225
df = pd.concat([df1_sub, df2_sub], ignore_index=True)

# Filter and clean
dat = df[(df['reward'] > -1) & (df['t_hold'] > 20)].copy()
dat['t_hold'] = dat['t_hold'] / 100  # convert to seconds

# Relabel categories
dat['trial_label'] = dat['trial'].map({1: 'cued', 2: 'uncued'})
dat['manipulation'] = dat['manipulation'].replace({'VEH': 'vehicle'})
dat['group'] = dat['group'].replace({'C': 'EGFP', 'D': 'hM4D(Gi)'})

# ==========================
# Colors
# ==========================
group_colors = {
    'EGFP': (0.365, 0.227, 0.608),
    'hM4D(Gi)': (0.9, 0.38, 0),
}
trial_type_colors = {
    'cued': (0, 0, 0),
    'uncued': (0.5, 0.5, 0.5),
}

# ==========================
# Per-subject means
# ==========================
subj_means = (
    dat.groupby(['rat', 'trial_label', 'group'])['t_hold']
    .mean()
    .reset_index()
)

# ==========================
# DABEST analysis
# ==========================
dabest_obj = dabest.load(
    data=subj_means,
    x='trial_label',
    y='t_hold',
    idx=('cued', 'uncued'),
    resamples=5000,
    random_seed=42
)

mean_diff = dabest_obj.mean_diff

# Display summary (includes p-value)
print(mean_diff)

# Access the p-value directly
p_value = mean_diff.results['pvalue_permutation']
print(p_value)

# ==========================
# Base DABEST plot
# ==========================
fig = dabest_obj.mean_diff.plot(
    raw_marker_size=0,  # hide default swarm
    contrast_label='Δ (uncued − cued)',
    custom_palette=trial_type_colors,
    fig_size=(8, 6)
)

plt.ylabel('exit time (s)')


# Access axes
raw_ax, contrast_ax = fig.axes

# ==========================
# Overlay per-subject means (jittered)
# ==========================
jitter_strength = 0.08  # adjust spacing
for cond_idx, cond in enumerate(['cued', 'uncued']):
    for grp in subj_means['group'].unique():
        y_vals = subj_means[
            (subj_means['trial_label'] == cond) &
            (subj_means['group'] == grp)
        ]['t_hold']
        
        # Apply jitter in x so points don't overlap with mean/SD
        x_jitter = cond_idx + np.random.uniform(-jitter_strength, jitter_strength, size=len(y_vals))
        
        raw_ax.scatter(
            x_jitter,
            y_vals,
            color=group_colors[grp],
            alpha=0.4,
            edgecolor='k',
            zorder=10,
            label=f'{grp}' if cond_idx == 0 else ""  # add legend entry only once
        )

# ==========================
# Overlay mean ± SD with annotation (centered)
# ==========================
for i, cond in enumerate(['cued', 'uncued']):
    vals = subj_means.loc[subj_means['trial_label'] == cond, 't_hold']
    mean_val = vals.mean()
    sd_val = vals.std()

    # Error bar
    raw_ax.errorbar(
        i, mean_val,
        yerr=sd_val,
        fmt='none',
        ecolor=trial_type_colors[cond],
        elinewidth=2,
        capsize=6,
        zorder=4
    )

    # Dot at mean
    raw_ax.scatter(
        i, mean_val,
        color=trial_type_colors[cond],
        s=80,
        zorder=11,
        edgecolor='k',
        linewidth=1.2
    )

    # Text annotation above bar
    raw_ax.text(
        i, mean_val + sd_val + 0.05,
        f"{mean_val:.3f}",
        ha='center', va='bottom',
        fontsize=12, fontweight='bold'
    )

# ==========================
# Font sizes for labels and ticks
# ==========================
raw_ax.set_xlabel("trial type", fontsize=18, labelpad=10)
raw_ax.set_ylabel("exit time (s)", fontsize=18, labelpad=10)
contrast_ax.set_xlabel("contrast", fontsize=18, labelpad=10)
contrast_ax.set_ylabel("Δ (uncued − cued)", fontsize=18, labelpad=10)

raw_ax.tick_params(axis='both', labelsize=16)
contrast_ax.tick_params(axis='both', labelsize=16)

# ==========================
# Legend cleanup
# ==========================
handles, labels = raw_ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
raw_ax.legend(
    by_label.values(),
    by_label.keys(),
    frameon=False,
    fontsize=12,
    title="Groups",
    title_fontsize=13,
    loc='upper left'
)

# ==========================
# Save and show
# ==========================
plt.tight_layout()
plt.show()

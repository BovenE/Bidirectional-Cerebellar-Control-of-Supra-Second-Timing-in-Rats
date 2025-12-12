# Bidirectional Cerebellar Control of Supra-Second Timing in Rats

This repository contains the **data, analysis scripts, and supplementary material** for the study  
**“Bidirectional Cerebellar Control of Supra-Second Timing in Rats”**.

The repository enables full reproduction of the analyses presented in the associated publication.

---

## Contents

- Raw and processed behavioural, histological, and open-field locomotion data  
- Analysis code used to generate all figures  
- Metadata and summary tables  
- Example DeepLabCut outputs and videos  

---

## Table of Contents

- [Overview](#overview)  
- [Directory Structure](#directory-structure)  
- [Data Description](#data-description)  
- [Reproducing the Analyses](#reproducing-the-analyses)  
- [Requirements](#requirements)  
- [Dependencies](#dependencies)  
- [Usage / Running the Analysis](#usage--running-the-analysis)  
- [Contact Information](#contact-information)  

---

## Overview

This project investigates how **cerebellar circuits contribute to supra-second timing behaviour** using:

- Interval-timing behavioural tasks  
- Open-field locomotion assays  
- Histological verification of DREADD and control manipulations  

All data and scripts required to reproduce the figures in the publication are included.

The dataset is organised according to three experimental data types:

### 1. Histology
Histological verification of control and DREADD manipulations (Figure 2A–D)

### 2. Interval Timing
Behavioural interval-timing measures (Figures 1 and 3–5)

### 3. Open Field
Effects of DREADD manipulation on locomotor behaviour (Figure 2E–G)

---

## Directory Structure

```text
Data/
├── Histology/
│   ├── analysis/
│   │   ├── Figure2C_D/
│   │   └── PlotHistology.py
│   └── data_csv/
│       ├── Microscopy_Expression_Summary_CONTROLS.csv
│       └── Microscopy_Expression_Summary_DREADD.csv
│
├── IntervalTiming/
│   ├── analysis/
│   │   ├── Figure1/
│   │   │   ├── Plot_baseline_instructivepredictivetrials_estimationplots.py
│   │   │   └── Plot_baseline_instructivetrials_estimationplots.py
│   │   └── Figure3_4/
│   │       └── Plot_interaction_boxplot.py
│   └── data_csv/
│       ├── Batch1_Stage_predictabletimecue.csv
│       ├── Batch1_Stage_unpredictabletimecue.csv
│       ├── Batch2_Stage_predictabletimecue.csv
│       └── Batch2_Stage_unpredictabletime.csv
│
└── OpenField/
    ├── analysis/
    │   └── Figure2E_F_G/
    │       ├── openfield_master.m
    │       ├── openFieldAnalysis.m
    │       └── Open_field_finalPlots.m
    └── data_csv/
        ├── *.csv
        ├── example_video_1.mp4
        ├── example_video_2.mp4
        └── trajectory_plots.png

Note:
Experiments were performed in two batches (Batch 1 and Batch 2).

```


---

## Data Description

### Interval Timing CSV Files
**Location:** `IntervalTiming/data_csv/`  

Each row represents **one behavioural trial**.

| Column | Description | Units / Codes |
|------|------------|---------------|
| rat_id | Animal ID | string |
| session_date | Session date | YYYY-MM-DD |
| group | Virus group | EGFP / hM4Di |
| manipulation | Treatment | vehicle / CNO |
| trial_type | Cue type | cued / uncued |
| trial_start | Trial start time | centiseconds |
| sound_onset | Auditory cue onset | centiseconds |
| sound_offset | Auditory cue offset | centiseconds |
| exit_time | t_release − t_sound_onset | centiseconds |
| reward_latency | Exit → reward port entry | centiseconds |
| rewarded | Reward delivered | 1 / 0 |
| too_early | Exit during random delay | 1 / 0 |
| incorrect | Exit before reward window | 1 / 0 |
| too_late | Exit after reward window | 1 / 0 |

---

### Histology CSV Files
**Location:** `Histology/data_csv/`

| Column | Description | Units |
|------|------------|-------|
| animal_id | Animal ID | — |
| section_mediolateral_mm | Distance from midline | mm |
| cortex_intensity | Fluorescence intensity | 0–5 |
| nuclei_intensity | Fluorescence intensity | 0–5 |
| white_matter_intensity | Fluorescence intensity | 0–5 |

---

### Open Field CSV Files
**Location:** `OpenField/data_csv/`

| Column | Description | Units |
|------|------------|-------|
| frame | Frame index | integer |
| x | Estimated head x-coordinate | pixels |
| y | Estimated head y-coordinate | pixels |
| likelihood | DLC confidence | 0–1 |
| velocity | Estimated velocity | cm/s |
| distance | Cumulative distance | meters |

---

## Units and Conventions

- Time values are reported in **centiseconds**  
- DeepLabCut coordinates are in **pixels**  
- Velocity and distance are reported in **cm** and **m**, respectively  
- Fluorescence intensity is reported on a **0–5 ordinal scale**

---

## Reproducing the Analyses

### Histology
Regenerates histology summary plots shown in Figure 2:

bash
python Data/Histology/analysis/PlotHistology.py

### Interval timing
Figure 1 (Estimation Plots)

bash
python Data/IntervalTiming/analysis/Figure1/Plot_baseline_instructivepredictivetrials_estimationplots.py
python Data/IntervalTiming/analysis/Figure1/Plot_baseline_instructivetrials_estimationplots.py

Figure 3-4 (interaction box plots)
bash
python Data/IntervalTiming/analysis/Figure3_4/Plot_interaction_boxplot.py

### Open Field

Generates open-field locomotion plots shown in Figure 2E–G:
    openfield_master
    Open_field_finalPlots


# Requirements

Python ≥ 3.9 — behavioural and histology analysis

MATLAB ≥ R2021a — open-field locomotion analysis

R ≥ 4.2.0 — statistical analyses

# Dependencies (Python)

numpy ≥ 1.22

pandas ≥ 1.5

matplotlib ≥ 3.6

seaborn ≥ 0.12

scipy ≥ 1.10

dabest ≥ 0.3.0

### Contact Information

Author ORCID:
https://orcid.org/0000-0001-6919-7612
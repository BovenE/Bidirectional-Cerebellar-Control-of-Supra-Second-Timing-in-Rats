# Bidirectional Cerebellar Control of Supra-Second Timing in Rats

This repository contains the data, analysis scripts, and supplementary material for the study **“Bidirectional Cerebellar Control of Supra-Second Timing in Rats”**.  

You will find:  
- raw and processed behavioural, histological and open-field locomotion data  
- code used to generate figures in the publication  
- metadata and summary tables  
- example DeepLabCut outputs and videos  

## Table of Contents

- [Overview](#overview)  
- [Directory Structure](#directory-structure)  
- [Requirements](#requirements)  
- [Usage / Running the Analysis](#usage--running-the-analysis)  
- [Data Description](#data-description)  
- [Citation](#citation)  
- [Contact information of the author](#license)  

## Overview

The goal of this project was to investigate how cerebellar circuits contribute to supra-second timing behaviour, using a combination of interval-timing tasks, open-field locomotion assays, and histological verification of manipulations.  
The repository bundles all data and scripts required to reproduce the analyses shown in the associated publication.

If you want to explore the data, re-run analysis, or extend the project, this repository gives full transparency and reproducibility.  

## Directory Structure

Data/
│
├── Histology/
│ ├── analysis/
│ │ PlotHistology.py
│ └── data_csv/
│ Microscopy_Expression_Summary_CONTROLS.csv
│ Microscopy_Expression_Summary_DREADD.csv
│
├── IntervalTiming/
│ ├── analysis/
│ │ ├── Figure1/
│ │ │ Plot_baseline_instructivepredictivetrials_estimationplots.py
│ │ │ Plot_baseline_instructivetrials_estimationplots.py
│ │ └── Figure3_4/
│ │ Plot_interaction_boxplot.py
│ └── data_csv/
│ Batch1_Stage_3.csv
│ Batch1_Stage_4.csv
│ Batch2_Stage_3.csv
│ Batch2_Stage_4.csv
│
└── OpenField/
├── analysis/
│ openfield_master.m
│ openFieldAnalysis.m
│ Open_field_finalPlots.m
└── data_csv/
*.csv (DeepLabCut output)
example_video_1.mp4
example_video_2.mp4
trajectory_plots.png


---

## Data Description

### Interval Timing CSV Files
Located in: `IntervalTiming/data_csv/`

Each row represents **one trial**.

| Column | Description | Units / Codes |
|--------|-------------|---------------|
| rat_id | Animal ID | string |
| session_date | Date of session | YYYY-MM-DD |
| group | Virus group | EGFP / hM4Di |
| manipulation | Treatment | vehicle / CNO |
| trial_type | Cue type | cued / uncued |
| trial_start | Trial start time | seconds |
| sound_onset | Onset of auditory cue | seconds |
| sound_offset | Offset of auditory cue | seconds |
| exit_time | t_release − t_sound_onset | seconds |
| reward_latency | Time from exit to reward-port entry | seconds |
| rewarded | Reward delivered | 1/0 |
| too_early | Exit during random delay | 1/0 |
| incorrect | Exit before reward window | 1/0 |
| too_late | Exit after reward window | 1/0 |

---

### Histology CSV Files
Located in: `Histology/data_csv/`

| Column | Description |
|--------|-------------|
| animal_id | Animal ID |
| section_mediolateral_mm | Distance from midline | mm |
| cortex_intensity | Fluorescence intensity (0–5) |
| nuclei_intensity | Fluorescence intensity (0–5) |
| white_matter_intensity | Fluorescence intensity (0–5) |
| mean_expression | Average intensity across regions |
| laterality_index | (Right − Left)/(Right + Left) |
| spread | Maximum − minimum expression extent |
| asymmetry_index | Lateral bias / total spread |

---

### Open Field CSV Files
Located in: `OpenField/data_csv/`

| Column | Description | Units |
|--------|-------------|--------|
| frame | Frame index | integer |
| x | Estimated head x-coordinate | pixels |
| y | Estimated head y-coordinate | pixels |
| likelihood | DLC confidence | 0–1 |
| velocity | Estimated velocity | cm/s |
| distance | Cumulative distance | meters |

---

## Units and Conventions
- Time values in seconds  
- DLC coordinates in pixels  
- Velocity/distance in cm/m  
- Fluorescence scale = 0–5

---

## Reproducing the Analyses

### Histology
```bash
python PlotHistology.py


## Requirements

- **Python ≥ 3.9** (for behavioural and histology analysis scripts)  
- **MATLAB ≥ R2021a** (for open-field locomotion analysis)
- - **R ≥ 4.2.0**  
  - Required for statistical analyses 

If you wish, I can also provide a `requirements.txt` or `environment.yml` for the Python dependencies.

## Usage / Running the Analysis

### Histology  
This code regenerates the histology summary plots in figure 1
python Data/Histology/analysis/PlotHistology.py

### Openfield
This code generates the plots in figure 2
openfield_finalPlots
openfield_master.m

### Interval Timing
This code regenerates the estimation plots of Figure 2
python Data/IntervalTiming/analysis/Figure1/Plot_baseline_instructivepredictivetrials_estimationplots.py
python Data/IntervalTiming/analysis/Figure1/Plot_baseline_instructivetrials_estimationplots.py
This code regenerates the interaction box plots in figure 3 and 4
python Data/IntervalTiming/analysis/Figure3_4/Plot_interaction_boxplot.py

### Contact information of the author
https://orcid.org/0000-0001-6919-7612






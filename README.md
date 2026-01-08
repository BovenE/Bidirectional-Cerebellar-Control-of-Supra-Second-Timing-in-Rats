# Bidirectional Cerebellar Control of Supra-Second Timing in Rats

This repository contains the **data and analysis scripts** for the study  
**“Bidirectional Cerebellar Control of Supra-Second Timing in Rats”**.

The repository enables reproduction of the analyses and figures presented in the associated publication.

---

## Contents

- Data from behavioural, histological, and open-field locomotion experiments
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

- Interval-timing behavioural tasks in rats
- Open-field locomotion assays in rats
- Histological verification of DREADD and control manipulations in rats
- Estimation statistics & General linear models to perform statistical analysis of behavioural measures 

The dataset is organised **by figure**, such that each figure in the manuscript corresponds to a dedicated data and analysis folder.
Each figure directory contains:
- `data/`: Raw or minimally processed data used for that figure
- `analysis/`: Scripts used to generate the analyses and plots

---

## Directory Structure


```text
Data/
├── Figure1/
│   ├── Panel__C-D__DREADDManipulation/
│  │   ├── data/
│   │   │    ├── Microscopy_Expression_Summary_CONTROLS.xls
│   │   │    └── Microscopy_Expression_Summary_DREADD.xls
│   │   ├── analysis/
│   │       └── PlotHistology.py  
│   │──Panel_E-F-G_OpenFieldLocomotion/
│   │   ├── data/
│   │   │    ├── 20220202_DTITET10DLC_resnet50_YR10-29-OpenFieldMay5shuffle1_101000.xls
│   │   │    └── 20220202_DTITET11DLC_resnet50_YR10-29-OpenFieldMay5shuffle1_101000.xls
│   │   │    │                              .
│   │   │    │                              .
│   │   │    │                              .
│   │   │    └── 20220202_DTITET21DLC_resnet50_YR10-29-OpenFieldMay5shuffle1_101000.xls
│   │   │    └── 20220202_DTITET21DLC_resnet50_YR10-29-OpenFieldMay5shuffle1_101000_labeled.mp4
│   │   ├── analysis/
│   │       └── Open_field_finalPlots.m  
├── Figure2/
│   ├── Panel_B-D_IntervalTiming/
│   │   ├── data/
│   │   │   ├── Batch1_predictabletimecue.csv
│   │   │   └── Batch1_unpredictabletimecue.csv
│   │   │   └── Batch2_predictabletimecue.csv
│   │   │   └── Batch2_unpredictabletimecue.csv
│   │   └── analysis/
│   │       └── Predictabletimecue.py
│   │       └── Unppredictabletimecue.py
├──Figure3-4/
│   │   ├── data/
│   │   │   ├── PredictableStage_GLMDataset.csv
│   │   │   └── UnpredictableStage_GLMDataset.csv
│   │   └── analysis/
│   │   │   └── ExitTime_GLMER/
│   │   │   │   └── GLM_PredictableStage.R
│   │   │   │   └── GLM_UnpredictableStage.R
│   │   │   │   └── PredictableTiming_anova_results.txt 
│   │   │   │   └── PredictableTiming_detailed_model_summary.txt
│   │   │   │   └── PredictableTiming_model_summary.txt
│   │   │   │   └── UnpredictableTiming_anova_results.txt
│   │   │   │   └── UnpredictableTiming_detailed_model_summary.txt 
│   │   │   │   └── UnpredictableTiming_model_summary.txt
│   │   │   └── NullModel_GLMER/
│   │   │       └── Review_CombinedGLM.R
│   │   │           └── Review_CombinedGLM.R
│   │   │           └── Review_CombinedGLM_Performance.R
│   │   │           └── Review_CombinedGLM_reward.R
│   │   │   └── Performance_GLMER/
│   │   │   │   └── GLM_performance_binomial_predictabletimecue.R
│   │   │   │   └── GLM_performance_binomial_predictabletimecue.R
│   │   │   │   └── PredictableTiming_anova_results.txt 
│   │   │   │   └── PredictableTiming_detailed_model_summary.txt
│   │   │   │   └── PredictableTiming_model_summary.txt
│   │   │   │   └── UnpredictableTiming_anova_results.txt
│   │   │   │   └── UnpredictableTiming_detailed_model_summary.txt 
│   │   │   │   └── UnpredictableTiming_model_summary.txt
│   │   │   └── RewardLat__LMER/
│   │   │   │   └── GLM_predictabletiming_reward_lat.R
│   │   │   │   └── GLM_unpredictabletiming_reward_lat.R
│   │   │   │   └── PredictableTiming_anova_results.txt 
│   │   │   │   └── PredictableTiming_detailed_model_summary.txt
│   │   │   │   └── PredictableTiming_model_summary.txt
│   │   │   │   └── UnpredictableTiming_anova_results.txt
│   │   │   │   └── UnpredictableTiming_detailed_model_summary.txt 
│   │   │   │   └── UnpredictableTiming_model_summary.txt
│   │   │   └── Trial__GLMER/
│   │   │   │   └── LMER_Trials.R
│   │   │   │   └── PredictableTiming_anova_results.txt 
│   │   │   │   └── PredictableTiming_detailed_model_summary.txt
│   │   │   │   └── PredictableTiming_model_summary.txt
│   │   │   │   └── UnpredictableTiming_anova_results.txt
│   │   │   │   └── UnpredictableTiming_detailed_model_summary.txt 
│   │   │   │   └── UnpredictableTiming_model_summary.txt
├── Figure5/
│   ├── data/
│   │      └── Batch1_unpredictabletimecue.csv
│   │      └── Batch2_unpredictabletimecue.csv
│   └── analysis/
│   │       └── GLM_UnpredictableStage.R
│   │       └── PredTrials_anova_results.txt
│   │       └── PredTrials_detailed_model_summary.txt
│   │       └── PredTrials_model_summary.txt
│   │       └── UnpredTrials_anova_results.txt
│   │       └── UnpredTrials_detailed_model_summary.txt
│   │       └── UnpredTrials_model_summary.txt

Note
Experiments were performed in two batches (Batch 1 and Batch 2), therefor datafiles are reported as batch 1 & batch 2.

```


---

## Data Description

---

### Figure1 - Panel C & D - Histology Files
**Location:** `Figure1\Panel_C_D\data`
**methodology:** see manuscript

| Sheet |
|------|------------|-------|
| animal_id | Animal ID | — |
| Column | Description | Units |
|------|------------|-------|
| Nuclei | Distance from midline | mm |
| Anterior | Fluorescence intensity | 0–5 |
| Posterior | Fluorescence intensity | 0–5 |
| Dorsal | Fluorescence intensity | 0–5 |
| Ventral | Fluorescence intensity | 0–5 |

---

### Figure1 - Panel E & F & G -  Open Field CSV Files Deeplabcut output
**Location:** `Figure1\Panel_E-F-G\data`
**methodology:** This is the standard deeplabcut output 


| Column | Description | Units |
|------|------------|-------|
| frame | Frame index | integer |
| x | Estimated head x-coordinate | pixels |
| y | Estimated head y-coordinate | pixels |
| likelihood | DLC confidence | 0–1 |
| velocity | Estimated velocity | cm/s |
| distance | Cumulative distance | meters |

---

### Figure 2 - Panel C & D - Interval Timing CSV Files
**Location:** `Figure2\Panel_B-D_IntervalTiming\data`  
**methodology:** see manuscript

Each row represents **one behavioural trial**.

| Column | Description | Units / Codes |
|------|------------|---------------|
| rat_id | Animal ID | string |
| group_id | Individual mouse ID for virus group | C (EGFP) / D (hM4Di) |
| group | Virus group | C (EGFP) / D (hM4Di) |
| session_date | Session date | YYYY-MM-DD |
| manipulation | Treatment | BASE (baseline session) 
| manipulation_type | Drug delivery  | BASE (baseline session) 
| trial | Cue type | 0 (too early) / 1 (cued) / 2 (uncued) | ** note: this column is specific for the unpredictable interval timing sessions
| trials | Session specific trial number | integer
| exit_time | t_release − t_sound_onset | centiseconds |
| reward_latency (reward_lat) | Exit → reward port entry | centiseconds |
| reward | Reward delivered | 1 (correct) / 0 (incorrect, too late) / -1 (too early trial) |


### Figure 3 & 4 - Interval Timing with DREADD manipulation 
**Location:** `Figure2\Panel_B-D_IntervalTiming\data`  
**methodology:** see manuscript
This data description applies to both PreditableStage_GLMDataset & UnpredictableStageGLMDataset_

Each row represents **one behavioural trial**.

| Column | Description | Units / Codes |
|------|------------|---------------|
| rat_id | Animal ID | string |
| group_id | Individual mouse ID for virus group | C (EGFP) / D (hM4Di) |
| group | Virus group | C (EGFP) / D (hM4Di) |
| session_date | Session date | YYYY-MM-DD |
| manipulation | Treatment | vehicle / CNO / BASE (baseline session) |
| manipulation_type | Drug delivery  | BASE (baseline session) /  i.p. injections
| trial | Cue type | 0 (too early) / 1 (cued) / 2 (uncued) | ** note: this column is specific for the unpredictable interval timing sessions
| trials | Session specific trial number | integer
| t_hold_ | t_release − t_sound_onset | seconds|
| reward_latency (reward_lat) | Exit → reward port entry | centiseconds |
| reward | Reward delivered | 1 (correct) / 0 (incorrect, too late) / -1 (too early trial) |

### Figure 5 - Interval Timing with unpredictable timecue with DREADD manipulation 
**Location:** `Figure2\Panel_B-D_IntervalTiming\data`  
**methodology:** see manuscript
This data description applies to both Batch1_unpredictableTimecue & Batch1_unpredictableTimecue

Each row represents **one behavioural trial**.

| Column | Description | Units / Codes |
|------|------------|---------------|
| rat_id | Animal ID | string |
| group_id | Individual mouse ID for virus group | C (EGFP) / D (hM4Di) |
| group | Virus group | C (EGFP) / D (hM4Di) |
| session_date | Session date | YYYY-MM-DD |
| manipulation | Treatment | vehicle / CNO / BASE (baseline session) |
| manipulation_type | Drug delivery  | BASE (baseline session) 
| trial | Cue type | 0 (too early) / 1 (cued) / 2 (uncued) | ** note: this column is specific for the unpredictable interval timing sessions
| trials | Session specific trial number | integer
| exit_time | t_release − t_sound_onset | centiseconds |
| reward_latency (reward_lat) | Exit → reward port entry | centiseconds |
| reward | Reward delivered | 1 (correct) / 0 (incorrect, too late) / -1 (too early trial) |



---

## Units and Conventions

- Time values are reported in **centiseconds**  
- DeepLabCut coordinates are in **pixels**  
- Velocity and distance are reported in **cm** and **m**, respectively  
- Fluorescence intensity is reported on a **0–5 ordinal scale**

---

## Reproducing the Analyses

### Figure 1 C & D
Regenerates histology summary plots shown in Figure 1:

bash
python Data/Histology/analysis/PlotHistology.py

### Figure 1 E & F & G

Generates open-field locomotion plots shown in Figure 1E–G:
    Open_field_finalPlots


### Figure 2 B & D
Regenerates the estimation plots

bash
python Figure2\Panel_B-D_IntervalTiming\analysis\Predictabletimecue.py
python Figure2\Panel_B-D_IntervalTiming\analysis\Un[redictabletimecue.py

### Figure 3 & 4

regenerates GLM analysis that is presented in figure 3 & 4 

To regenerate the GLM models run the .R files for each behavioural measure in Figure3-4\analysis
The output of the corresponding GLM models is saved to a .txt file

### Figure 5

regenerates GLM analysis that is presented in figure 5

To regenerate the GLM analysis run GLM_UnpredictableStage.R
The output of the corresponding GLM models is saved to a .txt file




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
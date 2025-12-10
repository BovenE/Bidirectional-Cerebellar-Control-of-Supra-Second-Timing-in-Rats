# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 14:46:31 2022

@author: valep
"""

# library
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap



# Create layout
layout = [
    ["B", "A"],
    ["B", "A"]
]

fig, axd = plt.subplot_mosaic(layout, figsize=(14,5))


#TO DO: Set path to file
#file = "/Users/va18024/Library/CloudStorage/OneDrive-UniversityofBristol/Documents/PhD/Cerebellearning/Experimental/Valentina_Pauly_Msc_project/Microscopy/Expression/Microscopy_Expression_Summary_DREADD.xlsx"
file = r"INSERTPATHTOFOLDER\Histology\data_csv\Microscopy_Expression_Summary_DREADD.xlsx"
#get sheet names since names have different structure
xl = pd.ExcelFile(file)


#Set area that you want to extract: Nuclei, Cortex or Fibers
area='Nuclei'


#default locations with default of Nuclei
ant='Anterior'
post='Posterior'
dors='Dorsal'
vent='Ventral'


locs = [ant, post, dors, vent]

#Change locations column name according to area 
if area =='Fibers':
    add_n = '.2'
elif area =='Cortex':
    add_n = '.1'     
    
if area != 'Nuclei': #"!=" means "not equal"; used bc "Nuclei" is default
    for i, n in enumerate(locs):
        n=n+add_n
        locs[i]=n

#number of sheets\animals to loop over
num=10
mmBregma = ["-4.6","-4.2","-3.9","-3.4","-2.9","-2.4","1.9","-1.4","-0.9","-0.4","-0.18","0.18","0.4","0.9","1.4","1.9","2.4","2.9","3.4","3.9","4.2","4.6"]
mmBregma2 = ["4.4","3.4","2.4","1.4","0.4","0","0.4","1.4","2.4","3.4","4.4"]

summary_list_dreadd = []
summary_list_controls = []
if 'dfanimal_all' not in locals():
    dfanimal_all = pd.DataFrame()


for j, int_loc in enumerate(locs):#loop over locations in given area
    dfall = pd.DataFrame(columns=['distance', 'animals', 'intensity']) # initialising dataframe with 4 empty categories
#loop over the sheets 
    for i, sheet_i in enumerate(xl.sheet_names[:num]):

        df=pd.read_excel(file, sheet_name=sheet_i) #read sheet number as dataframe 
        dfsub = df[(df[area]==-4.6) | (df[area]==-4.2) | (df[area]==-3.9) | (df[area]==-3.4) | (df[area]==-2.9) | (df[area]==-2.4) | (df[area]==-1.9) | (df[area]==-1.4) | (df[area]==-0.9) | (df[area]==-0.4) | (df[area]==-0.18) | (df[area]==0.4) | (df[area]==0.18) | (df[area]==0.9) | (df[area]==1.4) | (df[area]==1.9) | (df[area]==2.4) | (df[area]==2.4) | (df[area]==2.9) | (df[area]==3.4) | (df[area]==3.9) | (df[area]==4.2) | (df[area]==4.6)] 

        print('Processing '+ sheet_i)

        
        dfsub.fillna('-1.0', inplace=True)

        
        animals = np.repeat((sheet_i),len(dfsub[area].unique())) #go through all animals
        distance = np.arange(1,len(dfsub[area].unique())+1) #stack as many lists as animals are being looped over
        intensity = dfsub[int_loc]

        print(len(animals),len(distance),len(intensity))
# Create a dataset
#filling up dataset created above
# --- Build combined dataframe: dfanimal_all for lateral analysis ---

        
        mmBregma_floats = [float(x) for x in mmBregma]
        dfanimal=pd.DataFrame({ 'distance': mmBregma_floats, 'animals': animals, 'intensity': intensity})
        dfanimal['location'] = int_loc  # tag the source location
        dfanimal_all = pd.concat([dfanimal_all, dfanimal], ignore_index=True)


        
        #### safe to a structure 
        
        # Compute summary stats for this animal
        avg_intensity = intensity.astype(float).mean()
        max_intensity = intensity.astype(float).max()
        
        summary_entry = {
            'animal': sheet_i,
            'region': int_loc,
            'avg_intensity': avg_intensity,
            'max_intensity': max_intensity
        }
        
        if 'DREADD' in file:
            summary_list_dreadd.append(summary_entry)
        else:
            summary_list_controls.append(summary_entry)

        
        
        dfall = dfall.append(dfanimal, ignore_index=True)
        df_wide = dfall.pivot_table(index='animals', columns='distance', values='intensity')
    
        colors = [(1, 1, 1), (0.9,0.38,0)] # From white to magenta
        cmap_name = 'white_to_magenta'
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=6)
        num_colors = 6
        im = sns.heatmap(df_wide, vmin=-1, vmax=num_colors, cmap=cmap,square=False, cbar=False, cbar_kws={'label': 'intensity'}, ax=axd['A'])

# Convert types
dfanimal_all['distance'] = dfanimal_all['distance'].astype(float)
dfanimal_all['intensity'] = dfanimal_all['intensity'].astype(float)

# Compute injection spread where intensity > 0
dfanimal_all['intensity'] = dfanimal_all['intensity'].astype(float)
dfanimal_all['distance'] = dfanimal_all['distance'].astype(float)
df_summary_dreadd = pd.DataFrame(summary_list_dreadd)

dreadd_animals = list(df_summary_dreadd['animal'].unique())
dfanimal_dreadd = dfanimal_all[dfanimal_all['animals'].isin(dreadd_animals)]

# --- Compute spread features ---
expressed = dfanimal_dreadd[dfanimal_dreadd['intensity'] > 0].copy()

def compute_spread_features(df):
    left = df[df['distance'] < 0]['distance']
    right = df[df['distance'] > 0]['distance']
    
    left_spread = abs(left.min()) if not left.empty else 0
    right_spread = right.max() if not right.empty else 0
    
    total = left_spread + right_spread
    asymmetry = (right_spread - left_spread) / total if total > 0 else np.nan
    
    return pd.Series({
        'left_spread': left_spread,
        'right_spread': right_spread,
        'total_spread': total,
        'asymmetry_index': asymmetry
    })

# Apply per animal
spread_features = expressed.groupby('animals').apply(compute_spread_features).reset_index()

# Extract rat number for merging
spread_features['rat_num'] = spread_features['animals'].str.extract(r'(\d+)$')[0].astype(int)

# --- Merge with df_summary_dreadd ---
df_summary_dreadd['rat_num'] = df_summary_dreadd['animal'].str.extract(r'(\d+)$')[0].astype(int)
merged_summary = pd.merge(df_summary_dreadd, spread_features, on='rat_num', how='left')

# Save updated summary

# Preview
print(merged_summary[['animal', 'avg_intensity', 'left_spread', 'right_spread', 'total_spread', 'asymmetry_index']].drop_duplicates())


# Average across locations per animal × distance
df_lateral = dfanimal_all.groupby(['animals', 'distance'], as_index=False)['intensity'].mean()

# Compute lateral index per animal:
# sum(intensity × distance) / sum(intensity)
lateral_index_df = df_lateral.groupby('animals').apply(
    lambda x: np.sum(x['distance'] * x['intensity']) / np.sum(x['intensity'])
).reset_index(name='lateral_index')

# Clean up for merging
lateral_index_df['rat_num'] = lateral_index_df['animals'].str.extract(r'(\d+)$')[0].astype(int)

# Save if needed
        


cbar = fig.colorbar(im.collections[0], ax=axd['A'], orientation='vertical',pad=0.01, cmap=cmap)# location = 'bottom')
yticks = np.linspace(*cbar.ax.get_ylim(), 6+1)[:-1]
yticks += (yticks[1] - yticks[0]) / 2

# add tick labels to colorbar

# add tick labels to colorbar
cbar.set_ticks(yticks, labels=['0','1','2','3', '4', '5'])
cbar.ax.tick_params(length=0)          # remove tick lines
cbar.set_label('fluorescence (N.A.)')
tmp= -0.01
fs=14
axd['A'].text(2.5, tmp, 'LCN', fontsize=fs)        
axd['A'].text(5, tmp, 'IN', fontsize=fs)
axd['A'].text(7.5, tmp, 'MCN', fontsize=fs)
axd['A'].text(17.5, tmp, 'LCN', fontsize=fs)        
axd['A'].text(15, tmp, 'IN', fontsize=fs)
axd['A'].text(12.5, tmp, 'MCN', fontsize=fs)
axd['A'].set_yticklabels(axd['A'].get_yticklabels(), rotation = 0, fontsize = 16)



axd['A'].set_xticks(ticks = [1.5, 3.5, 5.5, 7.5, 9.5, 10.5, 11.5, 13.5, 15.5, 17.5, 19.5], labels = mmBregma2,fontsize = 18)
axd['A'].set_xticklabels(mmBregma2, rotation = 0, fontsize = 14)


axd['A'].set_ylabel('animal number',fontsize=18)
axd['A'].set_xlabel('mediolateral distance (mm)', labelpad=17, fontsize=16)


axd['A'].legend()


####plot Controls
# file = r"C:\Users\eboven\OneDrive - Erasmus MC\Documents\PhD\Data\Histology\Microscopy_Expression_Summary_CONTROLS.xlsx"
file = r"INSERTPATHTOFOLDER\Histology\data_csv\Microscopy_Expression_Summary_CONTROLS.xlsx"

#get sheet names since names have different structure
xl = pd.ExcelFile(file)



#Set area that you want to extract: Nuclei, Cortex or Fibers
area='Nuclei'


#default locations with default of Nuclei
ant='Anterior'
post='Posterior'
dors='Dorsal'
vent='Ventral'


locs = [ant]#, post, dors, vent]

#Change locations column name according to area 
if area =='Fibers':
    add_n = '.2'
elif area =='Cortex':
    add_n = '.1'     
    
if area != 'Nuclei': #"!=" means "not equal"; used bc "Nuclei" is default
    for i, n in enumerate(locs):
        n=n+add_n
        locs[i]=n

#number of sheets\animals to loop over
num=10
mmBregma = ["-4.6","-4.2","-3.9","-3.4","-2.9","-2.4","1.9","-1.4","-0.9","-0.4","-0.18","0.18","0.4","0.9","1.4","1.9","2.4","2.9","3.4","3.9","4.2","4.6"]
mmBregma2 = ["4.4","3.4","2.4","1.4","0.4","0","0.4","1.4","2.4","3.4","4.4"]




if 'dfanimal_all' not in locals():
    dfanimal_all = pd.DataFrame()

for j, int_loc in enumerate(locs):#loop over locations in given area
    dfall = pd.DataFrame(columns=['distance', 'animals', 'intensity']) # initialising dataframe with 4 empty categories
#loop over the sheets 
    for i, sheet_i in enumerate(xl.sheet_names[:num]):

        df=pd.read_excel(file, sheet_name=sheet_i) #read sheet number as dataframe 
        dfsub = df[(df[area]==-4.6) | (df[area]==-4.2) | (df[area]==-3.9) | (df[area]==-3.4) | (df[area]==-2.9) | (df[area]==-2.4) | (df[area]==-1.9) | (df[area]==-1.4) | (df[area]==-0.9) | (df[area]==-0.4) | (df[area]==-0.18) | (df[area]==0.4) | (df[area]==0.18) | (df[area]==0.9) | (df[area]==1.4) | (df[area]==1.9) | (df[area]==2.4) | (df[area]==2.4) | (df[area]==2.9) | (df[area]==3.4) | (df[area]==3.9) | (df[area]==4.2) | (df[area]==4.6)] 

        print('Processing '+ sheet_i)

        
        dfsub.fillna('-1.0', inplace=True)

        
        animals = np.repeat((sheet_i),len(dfsub[area].unique())) #go through all animals
        distance = np.arange(1,len(dfsub[area].unique())+1) #stack as many lists as animals are being looped over
        intensity = dfsub[int_loc]

        print(len(animals),len(distance),len(intensity))

        mmBregma_floats = [float(x) for x in mmBregma]
        dfanimal=pd.DataFrame({ 'distance': mmBregma_floats, 'animals': animals, 'intensity': intensity})
        dfanimal['location'] = int_loc  # tag the source location
        dfanimal_all = pd.concat([dfanimal_all, dfanimal], ignore_index=True)


        
        #### safe to a structure 
        
        # Compute summary stats for this animal
        avg_intensity = intensity.astype(float).mean()
        max_intensity = intensity.astype(float).max()
        
        summary_entry = {
            'animal': sheet_i,
            'region': int_loc,
            'avg_intensity': avg_intensity,
            'max_intensity': max_intensity
        }
        
        if 'DREADD' in file:
            summary_list_dreadd.append(summary_entry)
        else:
            summary_list_controls.append(summary_entry)

        
        dfall = dfall.append(dfanimal, ignore_index=True)
        df_wide = dfall.pivot_table(index='animals', columns='distance', values='intensity')

        
        import matplotlib.pyplot as plt
        from matplotlib.colors import LinearSegmentedColormap
        colors = [(1, 1, 1), (93/255, 58/255, 155/255)] # (0.1953,    0.8008,    0.1953)From white to magenta
        cmap_name = 'white_to_magenta'
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=6)
        #cmap_reds = plt.get_cmap('magma')
        num_colors = 6
        #colors = ['white'] + [cmap_reds(t) for t in range(1, num_colors)]
        #cmap = LinearSegmentedColormap.from_list('', colors, num_colors)
        ax=sns.heatmap(df_wide, vmin=-1, vmax=num_colors, cmap=cmap,square=False, cbar=False, cbar_kws={'label': 'intensity'}, ax = axd['B'])

        #sns.heatmap(df_wide)
        #plt.title(int_loc)
        plt.xticks(rotation = 0,  fontsize = 14)
        test=plt.xticks()[0]
        plt.yticks(rotation = 0, fontsize = 14)



# Convert types
dfanimal_all['distance'] = dfanimal_all['distance'].astype(float)
dfanimal_all['intensity'] = dfanimal_all['intensity'].astype(float)

# Average across locations per animal × distance
df_lateral = dfanimal_all.groupby(['animals', 'distance'], as_index=False)['intensity'].mean()

# Compute lateral index per animal:
# sum(intensity × distance) / sum(intensity)
lateral_index_df = df_lateral.groupby('animals').apply(
    lambda x: np.sum(x['distance'] * x['intensity']) / np.sum(x['intensity'])
).reset_index(name='lateral_index')

# Clean up for merging
lateral_index_df['rat_num'] = lateral_index_df['animals'].str.extract(r'(\d+)$')[0].astype(int)

# Save if needed
        

# Convert summaries to DataFrames
df_summary_controls = pd.DataFrame(summary_list_controls)

control_animals = list(df_summary_controls['animal'].unique())
dfanimal_control= dfanimal_all[dfanimal_all['animals'].isin(control_animals)]

# --- Compute spread features ---
expressed = dfanimal_control[dfanimal_control['intensity'] > 0].copy()


def compute_spread_features(df):
    left = df[df['distance'] < 0]['distance']
    right = df[df['distance'] > 0]['distance']
    
    left_spread = abs(left.min()) if not left.empty else 0
    right_spread = right.max() if not right.empty else 0
    
    total = left_spread + right_spread
    asymmetry = (right_spread - left_spread) / total if total > 0 else np.nan
    
    return pd.Series({
        'left_spread': left_spread,
        'right_spread': right_spread,
        'total_spread': total,
        'asymmetry_index': asymmetry
    })

# Apply per animal
spread_features = expressed.groupby('animals').apply(compute_spread_features).reset_index()

# Extract rat number for merging
spread_features['rat_num'] = spread_features['animals'].str.extract(r'(\d+)$')[0].astype(int)

# --- Merge with df_summary_dreadd ---
df_summary_controls['rat_num'] = df_summary_controls['animal'].str.extract(r'(\d+)$')[0].astype(int)
merged_summary = pd.merge(df_summary_controls, spread_features, on='rat_num', how='left')



# Save updated summary

# Preview
print(merged_summary[['animal', 'avg_intensity', 'left_spread', 'right_spread', 'total_spread', 'asymmetry_index']].drop_duplicates())


# Print or save
print("DREADD summary:")
print(df_summary_dreadd.groupby('animal')[['avg_intensity', 'max_intensity']].mean())

print("\nCONTROL summary:")
print(df_summary_controls.groupby('animal')[['avg_intensity', 'max_intensity']].mean())



tmp= -0.01
fs=14


axd['B'].text(2.5, tmp, 'LCN', fontsize=fs)        
axd['B'].text(5, tmp, 'IN', fontsize=fs)
axd['B'].text(7.5, tmp, 'MCN', fontsize=fs)
axd['B'].text(17.5, tmp, 'LCN', fontsize=fs)        
axd['B'].text(15, tmp, 'IN', fontsize=fs)
axd['B'].text(12.5, tmp, 'MCN', fontsize=fs)
axd['B'].set_yticklabels(axd['B'].get_yticklabels(), rotation = 0, fontsize = 16)
        

axd['B'].set_xticks(ticks = [1.5, 3.5, 5.5, 7.5, 9.5, 10.5, 11.5, 13.5, 15.5, 17.5, 19.5], labels = mmBregma2,fontsize = 18)
axd['B'].set_xticklabels(mmBregma2, rotation = 0, fontsize = 16)


axd['B'].set_ylabel('animal number',fontsize=18)
axd['B'].set_xlabel('mediolateral distance (mm)', labelpad=17, fontsize=16)


cbar = fig.colorbar(ax.collections[0], ax=axd['B'], orientation='vertical',pad=0.01, cmap=cmap)# location = 'bottom')
cbar.set_label('fluorescence (N.A.)')
yticks = np.linspace(*cbar.ax.get_ylim(), 6+1)[:-1]
yticks += (yticks[1] - yticks[0]) / 2

# add tick labels to colorbar

# add tick labels to colorbar
cbar.set_ticks(yticks, labels=['0','1','2','3', '4', '5'])
cbar.ax.tick_params(length=0)          # remove tick lines



plt.tight_layout()

plt.legend()

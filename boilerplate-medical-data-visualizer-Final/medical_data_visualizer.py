import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
data = pd.read_csv('medical_examination.csv')
df = pd.DataFrame(data)

# Add 'overweight' column
BMI = df['weight'] / (df['height']/100).pow(2)
BMI_overweight = []
for i in BMI:
  if i > 25:
    BMI_overweight.append(1)
  elif i <= 25:
    BMI_overweight.append(0)

df['overweight'] = BMI_overweight

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
norm_gluc = []
norm_chol = []

for i in df['gluc']:
  if i > 1:
    norm_gluc.append(1)
  elif i <= 1:
    norm_gluc.append(0)

df['gluc'] = norm_gluc

for i in df['cholesterol']:
  if i > 1:
    norm_chol.append(1)
  elif i <= 1:
    norm_chol.append(0)

df['cholesterol'] = norm_chol

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df[['cardio','active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat= df[['cardio','active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']]
    long_cat = pd.melt(df_cat, id_vars = ['cardio'])

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(data = long_cat, kind='count', x='variable', hue='value', col= 'cardio').set_ylabels('total').fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.loc[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975)) ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask = mask, annot = True,fmt = '.1f' )

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig


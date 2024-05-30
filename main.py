#%%
# import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#%%
df = pd.read_csv('bengaluru_house_prices.csv')
df.head()
#%%
df.shape
#%%
df2 = df.drop(['area_type', 'availability', 'society', 'balcony'], axis='columns')
df2.head()
#%%
df2.isnull().sum()
#%%
df3 = df2.dropna()
df3.isnull().sum()
#%%
df3["size"].unique()
df3["bhk"] = df3["size"].apply(lambda x: int(x.split(' ')[0]))
df3['bhk'].unique()
# %%
df3[df3.bhk>20]
#%%
df3.total_sqft.unique()
# %%
def is_float(x):
    try:
        float(x)
    except:
        return False
    return True
#%%
df3[~df3['total_sqft'].apply(is_float)].head(10)
# %%
def convert_sqft_to_num(x):
    tokens = x.split('-')
    if len(tokens) == 2:
        return (float(tokens[0])+float(tokens[1]))/2
    try:
        return float(x)
    except:
        return None
# %%
df4 = df3.copy()
df4.total_sqft = df4.total_sqft.apply(convert_sqft_to_num)
df4.head(3)
# %%
df.loc[30]
# %%
df5 = df4.copy()
df5['price_per_sqft'] = df5['price']*100000/df5['total_sqft']
df5.head()
# %%
len(df5.location.unique())
# %%
df5.location = df5.location.apply(lambda x: x.strip())

location_stats = df5.groupby('location')['location'].agg('count').sort_values(ascending=False)
location_stats
# %%
len(location_stats[location_stats<=10])
# %%
location_stats_less_than_10 = location_stats[location_stats<=10] # Location with less than 10 data points
df5.location = df5.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)
len(df5.location.unique())
# %%
df5[df5.total_sqft/df5.bhk<300].head()  # Outlier Detection
# %%
df6 = df5[~(df5.total_sqft/df5.bhk<300)] # Removing Outliers
# %%
df6.price_per_sqft.describe()
# %%
"""
import seaborn as sns
plt.figure(figsize=(20, 10))
plt.subplot(121)
sns.boxplot(df6.price_per_sqft)
dfTemp = df6[df6.price_per_sqft<7000]
plt.subplot(122)
sns.boxplot(dfTemp.price_per_sqft)
dfTemp.describe()
dfTemp.shape"""
#%%
def remove_pps_outliers(df):
    df_out = pd.DataFrame()
    for key, subdf in df.groupby('location'):
        m = subdf.price_per_sqft.mean()
        st = subdf.price_per_sqft.std()
        reduced_df = subdf[(subdf.price_per_sqft>(m-st)) & (subdf.price_per_sqft<=(m+st))]
        df_out = pd.concat([df_out, reduced_df], ignore_index=True)
    return df_out
df7 = remove_pps_outliers(df6)
df7.shape
# %%

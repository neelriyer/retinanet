#merge_csv
#merge csvs to create retinanet_data.csv


import pandas as pd
import os


df1 = pd.read_csv('/Users/neeliyer/Documents/SPOT/retinanet/retinanet/processed_JSON/retinanet_data_spacenet.csv')
df2 = pd.read_csv('/Users/neeliyer/Documents/SPOT/retinanet/retinanet/processed_JSON/retinanet_data_supervisely.csv')

final_df = df1.append(df2)
print(final_df)

final_df.to_csv(os.getcwd()+'/processed_JSON/retinanet_data.csv', header=True, index=None, sep=',')


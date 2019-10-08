import pandas as pd

data_in = "../dataset.csv"
data_out = "../dataset_ordered.csv"

df = pd.read_csv(data_in)
df = df.sort_values('score', ascending=False)
df.to_csv(data_out, index=False)
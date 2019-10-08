import pandas as pd

data_in = "../datasets/dataset_ordered.csv"
df = pd.read_csv(data_in)

df.drop(df.tail(14831).index, inplace=True)

df.to_csv('../datasets/working_dataset_2000.csv')
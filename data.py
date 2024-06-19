import pandas as pd

df = pd.read_csv('test.csv')

df = df['district']
districts_list = df.unique().tolist()
print(districts_list)


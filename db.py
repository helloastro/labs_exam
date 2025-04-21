from sklearn.datasets import load_iris
iris = load_iris()

import pandas as pd

df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['label'] = iris.target
df['species'] = iris.target_names[iris.target]
print(df.head())

from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://madang:madang@localhost:3306/madangdb')

df.to_sql(name='t_iris', con=engine, if_exists='replace')

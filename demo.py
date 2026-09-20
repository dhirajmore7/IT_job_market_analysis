import pandas as pd

# df = pd.DataFrame([{'name':'dhiraj','age':'','add':'','last_name':'more'}])

df=pd.read_csv('dhiraj.csv')
df['age']=22
df['add']='patonda'

df.to_csv('dhiraj.csv',mode='a',index=False)
print(df)
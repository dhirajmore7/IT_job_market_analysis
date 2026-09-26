from sqlalchemy import create_engine

import pandas as pd

from pathlib import Path

conn =create_engine("mysql+pymysql://root:sql123@localhost:3306/It_jobs_data")

clean_data = Path("processed_data/naukri/naukri_clean_data.csv")


df = pd.read_csv(clean_data)

df.to_sql('naukri_job',con=conn,index=False)

print("data load succesfully")

from pathlib import Path
from sqlalchemy import text
from etl.config import engine

db_schema = Path("database/db.sql")

with open(db_schema,"r",encoding='utf-8') as file:
    sql_script = file.read()
    sql_script = sql_script.split(';')
    # print(sql_script)

try:

    with engine.begin() as conn:

        for query in sql_script:
            query = query.strip()

            if query:
                conn.execute(text(query))
                print("query run succesfully")

        print("database created sucessfuly ")

except Exception as e:
    print('error',e)




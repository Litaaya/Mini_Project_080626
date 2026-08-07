import pandas as pd
from sqlalchemy import create_engine

db_url = "postgresql://postgres:postgres@localhost:5432/db"

def load(df: pd.DataFrame, table_name: str = "cleaned_jobs") -> None:
    if df.empty:
        print("No data found")
        return

    try:
        engine = create_engine(db_url)
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",
            index=False,
            method="multi"
        )
    except Exception as e:
        print(e)
        raise e
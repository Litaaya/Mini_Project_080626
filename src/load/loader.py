import pandas as pd
from sqlalchemy import create_engine

def load(df: pd.DataFrame,database_url: str, table_name: str) -> None:
    if df.empty:
        print("No data found")
        return

    try:
        engine = create_engine(database_url)
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
            method="multi"
        )
    finally:
        engine.dispose()
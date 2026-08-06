import pandas as pd

from src.transform.address_normalize import address_normalize
from src.transform.job_title_normalize import job_title_normalize
from src.transform.salary_normalize import salary_normalize


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    df_transformed = (
        df.pipe(salary_normalize)
        .pipe(address_normalize)
        .pipe(job_title_normalize)
    )

    return df_transformed

__all__ = [
    "transform_data",
    "salary_normalize",
    "address_normalize",
    "job_title_normalize"
]
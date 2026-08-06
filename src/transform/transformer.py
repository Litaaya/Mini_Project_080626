import pandas as pd
from src.transform.address_normalize import address_normalize
from src.transform.job_title_normalize import job_title_normalize
from src.transform.salary_normalize import salary_normalize


def transform(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    return (
        df.pipe(salary_normalize)
        .pipe(address_normalize)
        .pipe(job_title_normalize)
    )
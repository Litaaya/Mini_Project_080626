import pandas as pd
from .address_normalize import address_normalize
from .job_title_normalize import job_title_normalize
from .salary_normalize import salary_normalize


def transform(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()

    return (
        df.pipe(salary_normalize)
        .pipe(address_normalize)
        .pipe(job_title_normalize)
    )
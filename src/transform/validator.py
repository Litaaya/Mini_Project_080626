import pandas as pd
from typing import Tuple
import re

def is_valid_salary(salary_string: str) -> bool:
    if pd.isna(salary_string) or not str(salary_string).strip():
        return False

    s = str(salary_string).strip().lower()

    unit = "USD" if "usd" in s else "VND"
    if unit == "USD":
        s_clean = s.replace(",", "")
    else:
        s_clean = s.replace(".", "").replace(",", ".")
    numbers = [float(n) for n in re.findall(r"\d+\.?\d*", s_clean)]

    if len(numbers) >= 2 and numbers[0] > numbers[1]:
        return False

    return True

def is_valid_time(time_string: str) -> bool:
    if pd.isna(time_string) or not str(time_string).strip():
        return False

    s = str(time_string).strip().lower()
    numbers = re.findall(r"\d+", s)

    if numbers:
        days = int(numbers[0])
        return days >= 0

    return False

def validate_records(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    valid_date = pd.to_datetime(df["created_date"], errors="coerce").notna()

    valid_company = df["company"].notna() & (df["company"].astype(str).str.strip() != "")

    valid_salary = df["salary"].apply(is_valid_salary)

    valid_address = df["address"].notna() & (df["address"].astype(str).str.strip() != "")

    valid_time = df["time"].apply(is_valid_time)

    valid_url = df["job_url"].notna() & df["job_url"].astype(str).str.strip().str.lower().str.startswith("https://")

    valid_mask = valid_date & valid_company & valid_salary & valid_address & valid_time & valid_url
    valid_df = df[valid_mask].copy()
    dlq_valid = df[~valid_mask].copy()

    return valid_df, dlq_valid
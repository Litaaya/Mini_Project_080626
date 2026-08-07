import re
import pandas as pd
from typing import Tuple, Optional

def parse_salary_string(salary_string: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    if pd.isna(salary_string) or not str(salary_string).strip():
        return None, None, None

    s = str(salary_string).strip().lower()

    if "thoả thuận" in s or "thỏa thuận" in s:
        return None, None, None

    unit = "USD" if "usd" in s else "VND"

    if unit == ("USD"):
        s_clean = s.replace(",", "")
    else:
        s_clean = s.replace(",", ".")
    numbers = [float(n) for n in re.findall(r"\d+\.?\d*", s_clean)]

    if not numbers:
        return None, None, None

    multiplier = 1_000_000 if (unit == "VND" and "triệu" in s) else 1

    if len(numbers) >= 2:
        return numbers[0] * multiplier, numbers[1] * multiplier, unit

    if "tới" in s:
        return None, numbers[0] * multiplier, unit

    if "trên" in s:
        return numbers[0] * multiplier, None, unit

    return numbers[0] * multiplier, numbers[0] * multiplier, unit

def salary_normalize(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    salary_data = df_clean["salary"].apply(parse_salary_string)

    df_clean[["min_salary", "max_salary", "salary_unit"]] = pd.DataFrame(salary_data.tolist(), index=df_clean.index)

    return df_clean
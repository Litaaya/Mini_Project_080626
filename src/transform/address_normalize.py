import pandas as pd
from vietnam_provinces import Province

valid_cities = set()
for p in Province.iter_all():
    valid_cities.add(p.name)
    valid_cities.add(p.name.replace("Thành phố ", "").replace("Tỉnh ", ""))

def format_address(address_string: str) -> str:
    if pd.isna(address_string) or not str(address_string).strip():
        return ""

    parts = [p.strip() for p in str(address_string).split(":") if p.strip()]
    if not parts:
        return ""

    branches = []
    i = 0
    while i < len(parts):
        current_part = parts[i]
        if i + 1 < len(parts):
            next_part = parts[i + 1]
            if next_part in valid_cities:
                branches.append(current_part)
                i += 1
            else:
                branches.append(f"{current_part} - {next_part}")
                i += 2
        else:
            branches.append(current_part)
            i += 1

    return "; ".join(branches)

def address_normalize(df: pd.DataFrame) -> pd.DataFrame:
    if "address" not in df.columns:
        raise KeyError("Missing required column: 'address'")

    df_clean = df.copy()

    df_clean["clean_address"] = df_clean["address"].apply(format_address)

    return df_clean
import os
import pandas as pd
from typing import Optional

def extract(file_path: str) -> Optional[pd.DataFrame]:
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        return None

    try:
        df = pd.read_csv(file_path, encoding = "utf-8")
        print(f"File {file_path} is read with encoding utf-8")
        return df
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file_path, encoding = "utf-8-sig")
            print(f"File {file_path} is read with encoding utf-8-sig")
            return df
        except Exception as e:
            print(f"File {file_path} is read with encoding error: {e}")
            return None
    except pd.errors.EmptyDataError:
        print(f"File {file_path} is empty")
        return None
    except Exception as e:
        print(f"File {file_path} is read with encoding error: {e}")
        return None
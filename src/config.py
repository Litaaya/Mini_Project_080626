import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent

data_dir = base_dir / "data"
raw_data_path = data_dir / "raw" / "data.csv"
cleaned_data_path = data_dir / "processed" / "cleaned_data.csv"
dlq_data_path = data_dir / "dlq" / "invalid_records.csv"

postgres_user = os.getenv("POSTGRES_USER", "postgres")
postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
postgres_host = os.getenv("POSTGRES_HOST", "localhost")
postgres_port = os.getenv("POSTGRES_PORT", "5432")
postgres_database = os.getenv("POSTGRES_DATABASE", "mini_project_db")

database_url = (
    f"postgresql://{postgres_user}:{postgres_password}@"
    f"{postgres_host}:{postgres_port}/{postgres_database}"
)

default_table_name = "cleaned_jobs"
import logging
from extract import extract
from load import load
from config import database_url
from transform import transform, validate_records
from config import default_table_name, raw_data_path, cleaned_data_path, dlq_data_path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

column_order = [
        "created_date",
        "job_title",
        "clean_job_title",
        "normalized_job_title",
        "company",
        "salary",
        "min_salary",
        "max_salary",
        "salary_unit",
        "address",
        "clean_address",
        "time",
        "link_description"
    ]

def run_pipeline() -> None:
    logging.info("Pipeline started")

    try:
        logging.info("Extracting data")
        df_raw = extract(raw_data_path)
        logging.info(f"extracted {len(df_raw)} records")

        logging.info("Validate records")
        df_valid, df_dlq = validate_records(df_raw)
        logging.info(f"Valid: {len(df_valid)} records, Invalid {len(df_dlq)} records")

        logging.info("Transforming data")
        df_clean = transform(df_valid)
        df_clean = df_clean[column_order]
        logging.info("Transforming data complete")

        df_clean.to_csv(cleaned_data_path, index=False)
        df_dlq.to_csv(dlq_data_path, index=False)

        logging.info("Loading data")
        load(df_clean, database_url=database_url, table_name=default_table_name)
        logging.info("Loading data complete")

        logging.info("Pipeline completed")

    except FileNotFoundError as e:
        logging.error(f"Input file not found: {e}")
        raise
    except Exception:
        logging.exception("Unexpected pipeline failure")
        raise


if __name__ == "__main__":
    run_pipeline()
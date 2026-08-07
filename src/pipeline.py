import logging
from extract import extract
from load import load
from transform import transform, validate_records
from config import default_table_name, raw_data_path, cleaned_data_path, dlq_data_path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def run_pipeline() -> None:
    logging.info("Pipeline started")

    try:
        logging.info("Extracting data")
        df_raw = extract(raw_data_path)
        logging.info(f"extracted {len(df_raw)} records")

        df_valid, df_dlq = validate_records(df_raw)

        logging.info("Transforming data")
        df_clean = transform(df_valid)
        logging.info("Transforming data complete")

        df_clean.to_csv(cleaned_data_path, index=False)
        df_dlq.to_csv(dlq_data_path, index=False)

        logging.info("Loading data")
        load(df_clean, table_name=default_table_name)
        logging.info("Loading data complete")

        logging.info("Pipeline completed")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise e


if __name__ == "__main__":
    run_pipeline()
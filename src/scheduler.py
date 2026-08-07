import logging
import subprocess
import time
import schedule
from config import base_dir
from pipeline import run_pipeline


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def ensure_docker_running() -> bool:
    try:
        subprocess.run(
            ["docker", "compose", "up", "-d"],
            cwd=base_dir,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        logging.info("Docker container is running")
        return True

    except subprocess.CalledProcessError as exc:
        logging.error(
            f"Failed to start Docker containers: {exc}"
        )
        return False

    except FileNotFoundError:
        logging.error("Docker command not found")
        return False


def job() -> None:
    logging.info("Scheduled ETL job started")

    if not ensure_docker_running():
        logging.error(
            "Pipeline skipped because Docker is unavailable"
        )
        return

    try:
        run_pipeline()

    except Exception:
        logging.exception(
            "Scheduled pipeline failed"
        )

schedule.every().day.at("08:00").do(job)

if __name__ == "__main__":
    logging.info("Scheduler started")

    while True:
        schedule.run_pending()
        time.sleep(1)
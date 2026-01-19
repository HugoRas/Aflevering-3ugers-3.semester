import time
import logging
from config import Config
from repositories.recording_repo import fetch_next_queued, set_status, upsert_signal_path
from services.processing_service import process_recording

POLL_SECONDS = 2


def main():
    logging.basicConfig(level=logging.INFO)

    import os, sys
    logging.info("Worker started: cwd=%s python=%s", os.getcwd(), sys.executable)

    cfg = {
        "DB_HOST": Config.DB_HOST,
        "DB_PORT": getattr(Config, "DB_PORT", 3306),  # <-- add this
        "DB_USER": Config.DB_USER,
        "DB_PASSWORD": Config.DB_PASSWORD,
        "DB_NAME": Config.DB_NAME,
        "RAW_DIR": Config.RAW_DIR,
        "FILTERED_DIR": Config.FILTERED_DIR,
        "PLOTS_DIR": Config.PLOTS_DIR,
        "LOG_DIR": Config.LOG_DIR,
    }

    while True:
        logging.info("Polling queue...")
        job = fetch_next_queued(cfg)
        if not job:
            time.sleep(POLL_SECONDS)
            continue

        recording_id = job["recording_id"]
        try:
            set_status(cfg, recording_id, "PROCESSING", pipeline_version="v1")
            result = process_recording(cfg, recording_id)

            upsert_signal_path(
                cfg,
                recording_id,
                "filtered",
                result["filtered_path"],
                sample_rate=result["fs"],
            )

            set_status(cfg, recording_id, "DONE")
            logging.info("Processed recording_id=%s", recording_id)

        except Exception as e:
            set_status(cfg, recording_id, "FAILED", error_message=str(e))
            logging.exception("Failed processing recording_id=%s", recording_id)


if __name__ == "__main__":
    main()

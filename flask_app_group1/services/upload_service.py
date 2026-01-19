import os
import re
from infrastructure.storage import recording_raw_dir
from repositories.patient_repo import get_patient_by_user_id
from repositories.recording_repo import create_recording, upsert_signal_path, set_status


def _safe_stem(filename: str) -> str:
    # "rec_3.dat" -> "rec_3"
    stem = os.path.splitext(filename)[0]
    # keep it filesystem-safe
    stem = re.sub(r"[^A-Za-z0-9_\-]", "_", stem)
    return stem or "rec"


def handle_patient_upload(cfg, user_id: int, dat_file, hea_file) -> int:
    if not dat_file or not hea_file:
        raise ValueError("Missing .dat or .hea")

    patient = get_patient_by_user_id(cfg, user_id)
    if not patient:
        raise RuntimeError("No patient linked to this user_id")

    recording_id = create_recording(cfg, patient_id=patient["patient_id"], uploaded_by=user_id)

    try:
        rec_dir = recording_raw_dir(cfg, recording_id)
        os.makedirs(rec_dir, exist_ok=True)

        # Use the base name from the uploaded files (must match the .hea internal reference)
        dat_stem = _safe_stem(dat_file.filename or "rec.dat")
        hea_stem = _safe_stem(hea_file.filename or "rec.hea")
        if dat_stem != hea_stem:
            # If user uploads mismatched pair, fail early
            raise ValueError(f"Mismatched WFDB pair: {dat_stem}.dat vs {hea_stem}.hea")

        record_name = dat_stem  # e.g. "rec_3"
        base_path = os.path.join(rec_dir, record_name)

        dat_path = base_path + ".dat"
        hea_path = base_path + ".hea"

        dat_file.save(dat_path)
        hea_file.save(hea_path)

        upsert_signal_path(cfg, recording_id, "raw", base_path, sample_rate=None)
        return recording_id

    except Exception as e:
        set_status(cfg, recording_id, "FAILED", error_message=str(e))
        raise

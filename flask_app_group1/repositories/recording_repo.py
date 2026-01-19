from datetime import datetime, timedelta
from repositories.db import fetchone_dict, fetchall_dict, execute

# --------------------------
# ECG recording (metadata)
# --------------------------

def create_recording(cfg, patient_id: int, uploaded_by: int | None):
    now = datetime.now()
    start_time = now
    end_time = now + timedelta(seconds=20)

    recording_id = execute(
        cfg,
        """
        INSERT INTO ecg (patient_id, uploaded_by, start_time, end_time, status)
        VALUES (?,?,?,?, 'QUEUED')
        """,
        (patient_id, uploaded_by, start_time, end_time),
    )
    return recording_id


def set_status(cfg, recording_id: int, status: str, error_message=None, pipeline_version=None):
    execute(
        cfg,
        """
        UPDATE ecg
        SET status=?, error_message=?, pipeline_version=COALESCE(?, pipeline_version)
        WHERE recording_id=?
        """,
        (status, error_message, pipeline_version, recording_id),
    )


def list_recent_recordings(cfg, limit=50):
    return fetchall_dict(
        cfg,
        """
        SELECT recording_id, patient_id, upload_time, status, error_message
        FROM ecg
        ORDER BY upload_time DESC
        LIMIT ?
        """,
        (limit,),
    )


def list_recordings_for_patient(cfg, patient_id: int, limit: int = 50):
    """
    Bruges af patientens Medical Record.
    Returnerer KUN patientens egne uploads.
    """
    return fetchall_dict(
        cfg,
        """
        SELECT recording_id, patient_id, upload_time, status, error_message
        FROM ecg
        WHERE patient_id = ?
        ORDER BY upload_time DESC
        LIMIT ?
        """,
        (patient_id, limit),
    )


def get_recording(cfg, recording_id: int):
    return fetchone_dict(
        cfg,
        "SELECT * FROM ecg WHERE recording_id=?",
        (recording_id,),
    )


def fetch_next_queued(cfg):
    return fetchone_dict(
        cfg,
        """
        SELECT e.recording_id
        FROM ecg e
        JOIN ecg_signal s
          ON s.recording_id = e.recording_id
         AND s.signal_type = 'raw'
         AND s.file_path IS NOT NULL
         AND s.file_path <> ''
        WHERE e.status='QUEUED'
        ORDER BY e.upload_time ASC
        LIMIT 1
        """
    )


# --------------------------
# File references (ecg_signal)
# --------------------------

def upsert_signal_path(cfg, recording_id: int, signal_type: str, file_path: str, sample_rate=None):
    execute(
        cfg,
        """
        INSERT INTO ecg_signal (recording_id, signal_type, file_path, sample_rate)
        VALUES (?,?,?,?)
        ON DUPLICATE KEY UPDATE
          file_path=VALUES(file_path),
          sample_rate=VALUES(sample_rate)
        """,
        (recording_id, signal_type, file_path, sample_rate),
    )


def get_signal_path(cfg, recording_id: int, signal_type: str):
    return fetchone_dict(
        cfg,
        """
        SELECT *
        FROM ecg_signal
        WHERE recording_id=? AND signal_type=?
        """,
        (recording_id, signal_type),
    )

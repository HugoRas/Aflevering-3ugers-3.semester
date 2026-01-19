from repositories.db import execute, fetchall_dict

def ensure_comment_table(cfg):
    # Harmless hvis den allerede findes
    execute(
        cfg,
        """
        CREATE TABLE IF NOT EXISTS clinician_comment (
          comment_id INT AUTO_INCREMENT PRIMARY KEY,
          recording_id INT NOT NULL,
          clinician_user_id INT NOT NULL,
          comment_text TEXT NOT NULL,
          created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB
        """,
    )


def add_comment(cfg, recording_id: int, clinician_user_id: int, text: str):
    ensure_comment_table(cfg)
    execute(
        cfg,
        """
        INSERT INTO clinician_comment (recording_id, clinician_user_id, comment_text)
        VALUES (?,?,?)
        """,
        (recording_id, clinician_user_id, text),
    )


def list_comments(cfg, recording_id: int):
    ensure_comment_table(cfg)
    return fetchall_dict(
        cfg,
        """
        SELECT comment_id, clinician_user_id, comment_text, created_at
        FROM clinician_comment
        WHERE recording_id=?
        ORDER BY created_at DESC
        """,
        (recording_id,),
    )


def list_comments_for_recordings(cfg, recording_ids: list[int]):
    """
    Batch-hent kommentarer til Medical Record (undgår N+1 queries).
    """
    ensure_comment_table(cfg)

    if not recording_ids:
        return []

    placeholders = ",".join(["?"] * len(recording_ids))
    sql = f"""
        SELECT recording_id, clinician_user_id, comment_text, created_at
        FROM clinician_comment
        WHERE recording_id IN ({placeholders})
        ORDER BY recording_id DESC, created_at DESC
    """
    return fetchall_dict(cfg, sql, tuple(recording_ids))

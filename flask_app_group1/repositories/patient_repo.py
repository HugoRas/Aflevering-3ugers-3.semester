from repositories.db import fetchone_dict, fetchall_dict, execute


def get_patient_by_user_id(cfg, user_id: int):
    return fetchone_dict(
        cfg,
        """
        SELECT *
        FROM patient
        WHERE user_id=?
        """,
        (user_id,),
    )


def get_patient_by_id(cfg, patient_id: int):
    return fetchone_dict(
        cfg,
        """
        SELECT *
        FROM patient
        WHERE patient_id=?
        """,
        (patient_id,),
    )


def list_patients(cfg):
    return fetchall_dict(
        cfg,
        """
        SELECT *
        FROM patient
        ORDER BY patient_id
        """
    )


def update_patient_by_user_id(cfg, user_id: int, name: str):
    """
    Opdaterer KUN navn.
    Phone er fjernet helt fra UI og backend.
    """
    execute(
        cfg,
        """
        UPDATE patient
        SET name=?
        WHERE user_id=?
        """,
        (name, user_id),
    )


def ensure_patient_for_user(cfg, user_id: int, name: str | None = None):
    """
    Sikrer at der findes en patient-række for en given user_id.
    Bruges når admin opretter en patient-bruger, så uploads aldrig fejler.
    Returnerer patient_id.
    """
    existing = fetchone_dict(
        cfg,
        "SELECT patient_id FROM patient WHERE user_id=?",
        (user_id,),
    )
    if existing:
        return existing["patient_id"]

    if not name:
        name = "Unknown"

    patient_id = execute(
        cfg,
        """
        INSERT INTO patient (user_id, name)
        VALUES (?, ?)
        """,
        (user_id, name),
    )
    return patient_id

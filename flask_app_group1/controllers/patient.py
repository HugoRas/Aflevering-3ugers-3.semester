from flask import Blueprint, render_template, request, session, current_app
from services.auth_service import require_role
from services.upload_service import handle_patient_upload
from repositories.patient_repo import (
    get_patient_by_user_id,
    update_patient_by_user_id,
)

patient_bp = Blueprint("patient", __name__)


# -----------------------
# Dashboard
# -----------------------
@patient_bp.get("/dashboard")
@require_role("patient")
def dashboard():
    return render_template(
        "patient/dashboard.html",
        active_page="dashboard",
    )


# -----------------------
# Patientinfo (GET)
# -----------------------
@patient_bp.get("/patientinfo")
@require_role("patient")
def patientinfo():
    cfg = current_app.config
    user_id = session["user_id"]

    patient = get_patient_by_user_id(cfg, user_id)

    return render_template(
        "patient/patientinfo.html",
        active_page="patientinfo",
        patient=patient,
    )


# -----------------------
# Patientinfo (POST)
# -----------------------
@patient_bp.post("/patientinfo")
@require_role("patient")
def patientinfo_post():
    cfg = current_app.config
    user_id = session["user_id"]

    name = (request.form.get("name") or "").strip()

    if not name:
        patient = get_patient_by_user_id(cfg, user_id)
        return render_template(
            "patient/patientinfo.html",
            active_page="patientinfo",
            patient=patient,
            msg="Name is required.",
        )

    update_patient_by_user_id(cfg, user_id, name)

    patient = get_patient_by_user_id(cfg, user_id)
    return render_template(
        "patient/patientinfo.html",
        active_page="patientinfo",
        patient=patient,
        msg="Information updated successfully.",
    )


# -----------------------
# Medical record (GET)
# -----------------------
@patient_bp.get("/medicalrecord")
@require_role("patient")
def medicalrecord():
    """
    Patientens egen medical record:
    - Basis info
    - Uploads
    - Clinician comments
    """
    cfg = current_app.config
    user_id = session["user_id"]

    patient = get_patient_by_user_id(cfg, user_id)
    if not patient:
        return render_template(
            "patient/medicalrecord.html",
            active_page="medicalrecord",
            patient_name="Unknown",
            patient_id="Unknown",
            recs=[],
            comments_by_recording={},
        )

    patient_id = patient["patient_id"]
    patient_name = patient.get("name") or "Unknown"

    # --- Uploads ---
    from repositories.recording_repo import list_recordings_for_patient
    recs = list_recordings_for_patient(cfg, patient_id, limit=50)

    # --- Comments ---
    recording_ids = [r["recording_id"] for r in recs]
    from repositories.comment_repo import list_comments_for_recordings
    comments = list_comments_for_recordings(cfg, recording_ids)

    # Gruppér comments pr recording
    comments_by_recording = {}
    for c in comments:
        rid = c["recording_id"]
        comments_by_recording.setdefault(rid, []).append(c)

    return render_template(
        "patient/medicalrecord.html",
        active_page="medicalrecord",
        patient_name=patient_name,
        patient_id=patient_id,
        recs=recs,
        comments_by_recording=comments_by_recording,
    )


# -----------------------
# Upload ECG
# -----------------------
@patient_bp.post("/upload")
@require_role("patient")
def upload():
    cfg = current_app.config
    user_id = session["user_id"]

    dat_file = request.files.get("dat_file")
    hea_file = request.files.get("hea_file")

    if not dat_file or not hea_file:
        return render_template(
            "patient/dashboard.html",
            active_page="dashboard",
            upload_error="Missing .dat or .hea file",
        )

    if not dat_file.filename.lower().endswith(".dat"):
        return render_template(
            "patient/dashboard.html",
            active_page="dashboard",
            upload_error="Invalid file type for .dat file",
        )

    if not hea_file.filename.lower().endswith(".hea"):
        return render_template(
            "patient/dashboard.html",
            active_page="dashboard",
            upload_error="Invalid file type for .hea file",
        )

    try:
        recording_id = handle_patient_upload(cfg, user_id, dat_file, hea_file)
    except Exception as e:
        current_app.logger.exception("Patient upload failed")
        return render_template(
            "patient/dashboard.html",
            active_page="dashboard",
            upload_error=str(e),
        )

    return render_template(
        "patient/dashboard.html",
        active_page="dashboard",
        upload_ok=True,
        recording_id=recording_id,
    )

import os
from flask import Blueprint, render_template, request, session, current_app, send_from_directory, abort
from services.auth_service import require_role
from repositories.patient_repo import list_patients, get_patient_by_id
from repositories.recording_repo import list_recent_recordings, get_recording
from repositories.comment_repo import add_comment, list_comments

clinician_bp = Blueprint("clinician", __name__)


@clinician_bp.get("/")
@require_role("clinician")
def dashboard():
    cfg = current_app.config
    recs = list_recent_recordings(cfg, limit=50)
    patients = list_patients(cfg)
    return render_template("clinician/search_record.html", recs=recs, patients=patients)


@clinician_bp.route("/record/<int:recording_id>", methods=["GET", "POST"])
@require_role("clinician")
def medical_record(recording_id):
    cfg = current_app.config

    rec = get_recording(cfg, recording_id)
    if not rec:
        abort(404)

    # Add comment
    if request.method == "POST":
        text = (request.form.get("comment_text") or "").strip()
        if text:
            add_comment(cfg, recording_id, session["user_id"], text)

    comments = list_comments(cfg, recording_id)

    # Build plot URLs (served through the /plots route below)
    # Using relative URLs keeps it safe behind proxy/prefix.
    time_plot_filename = f"{recording_id}_time.png"
    freq_plot_filename = f"{recording_id}_freq.png"
    time_plot_url = f"/clinician/plots/{time_plot_filename}"
    freq_plot_url = f"/clinician/plots/{freq_plot_filename}"

    patient = get_patient_by_id(cfg, rec["patient_id"])

    return render_template(
        "clinician/medicalrecord.html",
        rec=rec,
        patient=patient,
        time_plot_url=time_plot_url,
        freq_plot_url=freq_plot_url,
        comments=comments,
    )


@clinician_bp.get("/plots/<path:filename>")
@require_role("clinician")
def plots(filename):
    """
    Serve plot images to clinicians only.

    Security:
    - prevent path traversal
    - optionally enforce .png only
    """
    if ".." in filename or filename.startswith(("/", "\\")):
        abort(400)

    if not filename.lower().endswith(".png"):
        abort(404)

    plots_dir = current_app.config["PLOTS_DIR"]
    full_path = os.path.join(plots_dir, filename)

    if not os.path.isfile(full_path):
        abort(404)

    return send_from_directory(plots_dir, filename)

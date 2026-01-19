import os
import numpy as np

from repositories.recording_repo import get_signal_path
from signal_processing.wfdb_io import load_from_raw_dir
from signal_processing.filters import filter_ecg
from signal_processing.plots import save_time_plot, save_spectrum_plot
from signal_processing.features import detect_sudden_hr_change


def process_recording(cfg, recording_id: int) -> dict:
    # --- locate raw signal ---
    raw_row = get_signal_path(cfg, recording_id, "raw")
    if not raw_row or not raw_row.get("file_path"):
        raise RuntimeError("Missing raw signal file_path")

    raw_base = raw_row["file_path"]          # /.../raw/11/rec_3
    raw_dir = os.path.dirname(raw_base)      # /.../raw/11
    record_name = os.path.basename(raw_base) # rec_3

    # --- load raw ECG ---
    ecg, fs = load_from_raw_dir(
        raw_dir,
        record_name=record_name,
        channel=0,
    )

    # --- filtering ---
    ecg_f = filter_ecg(ecg, fs)

    # --- save filtered signal ---
    filtered_path = os.path.join(cfg["FILTERED_DIR"], f"{recording_id}.npy")
    os.makedirs(os.path.dirname(filtered_path), exist_ok=True)
    np.save(filtered_path, ecg_f)

    # --- plots ---
    time_plot_path = os.path.join(cfg["PLOTS_DIR"], f"{recording_id}_time.png")
    freq_plot_path = os.path.join(cfg["PLOTS_DIR"], f"{recording_id}_freq.png")

    save_time_plot(
        path=time_plot_path,
        raw=ecg,
        filtered=ecg_f,
        fs=fs,
    )

    save_spectrum_plot(
        path=freq_plot_path,
        raw=ecg,
        filtered=ecg_f,
        fs=fs,
    )

    # --- feature extraction / flags ---
    flags = detect_sudden_hr_change(ecg_f, fs)

    return {
        "filtered_path": filtered_path,
        "time_plot_path": time_plot_path,
        "freq_plot_path": freq_plot_path,
        "fs": fs,
        "flags": flags,
    }

import numpy as np
from scipy import signal


def detect_sudden_hr_change(filtered, fs, min_hr_jump_bpm=30, window_beats=3):
    """
    Simple HR change detector:
      1) Detect R-peaks (rough)
      2) Compute RR intervals -> HR series
      3) Flag sudden change if HR jumps by >= min_hr_jump_bpm over a short beat window

    Returns a dict like your placeholder.
    """

    x = np.asarray(filtered, dtype=float)
    if fs <= 0:
        raise ValueError("fs must be > 0")
    if x.size < int(fs * 3):
        return {
            "sudden_hr_change": False,
            "note": "signal too short for HR change detection",
        }

    # --- 1) R-peak detection (rough but works for many ECGs) ---
    # Bandpass around QRS energy (approx 5-15 Hz) to boost peaks
    b_bp, a_bp = signal.butter(2, [5, 15], btype="bandpass", fs=fs)
    y = signal.filtfilt(b_bp, a_bp, x)

    # Square to emphasize peaks
    y2 = y ** 2

    # Moving average integration (~150 ms)
    win = max(1, int(0.15 * fs))
    kernel = np.ones(win) / win
    y_int = np.convolve(y2, kernel, mode="same")

    # Peak picking: enforce refractory period (~250 ms)
    refractory = int(0.25 * fs)
    thresh = np.percentile(y_int, 95)  # adaptive-ish threshold
    peaks, _ = signal.find_peaks(y_int, height=thresh, distance=refractory)

    if len(peaks) < (window_beats + 2):
        return {
            "sudden_hr_change": False,
            "note": "too few R-peaks detected",
        }

    # --- 2) RR -> HR(t) ---
    rr_sec = np.diff(peaks) / fs
    # Basic sanity: ignore impossible RR
    rr_sec = rr_sec[(rr_sec > 0.3) & (rr_sec < 2.0)]  # 30–200 bpm

    if rr_sec.size < (window_beats + 1):
        return {
            "sudden_hr_change": False,
            "note": "RR series too short after filtering",
        }

    hr_bpm = 60.0 / rr_sec

    # --- 3) Sudden HR change test ---
    # Compare local average HR over last "window_beats" vs previous window
    w = window_beats
    max_jump = 0.0
    sudden = False

    for i in range(2 * w, len(hr_bpm) + 1):
        prev = np.mean(hr_bpm[i - 2*w : i - w])
        curr = np.mean(hr_bpm[i - w : i])
        jump = abs(curr - prev)
        if jump > max_jump:
            max_jump = jump
        if jump >= min_hr_jump_bpm:
            sudden = True
            break

    return {
        "sudden_hr_change": sudden,
        "max_hr_jump_bpm": float(max_jump),
        "note": "simple R-peak/RR HR-jump detector",
    }

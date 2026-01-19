import os
import wfdb


def load_from_raw_dir(raw_dir: str, record_name: str = "rec", channel: int = 0, sampfrom: int = 0, sampto: int | None = None):
    """
    Loads one ECG channel from a WFDB recording located in raw_dir.

    Expects WFDB files like:
      raw_dir/rec.dat, raw_dir/rec.hea, raw_dir/rec.atr (optional), etc.

    Parameters
    ----------
    raw_dir : str
        Directory containing the WFDB recording files.
    record_name : str
        Base name of the WFDB record (default: "rec").
    channel : int
        Channel index to load (default: 0).
    sampfrom : int
        Start sample index (default: 0).
    sampto : int | None
        End sample index (exclusive). If None, loads entire record.

    Returns
    -------
    ecg : ndarray
        ECG signal (1D).
    fs : float
        Sampling frequency.
    """
    base = os.path.join(raw_dir, record_name)

    if not os.path.exists(base + ".hea"):
        raise FileNotFoundError(f"WFDB header not found: {base}.hea")

    signals, info = wfdb.rdsamp(
        base,
        channels=[channel],
        sampfrom=sampfrom,
        sampto=sampto,
    )

    fs = info["fs"]
    ecg = signals[:, 0]
    return ecg, fs

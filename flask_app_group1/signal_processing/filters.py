from scipy import signal
import numpy as np


def filter_ecg(ecg, fs):
    """
    ECG filtering pipeline:
    1) High-pass filter to remove baseline wander
    2) Notch filter at 50 Hz to remove powerline interference
    3) Low-pass filter to reduce EMG / high-frequency noise
    """

    if fs <= 0:
        raise ValueError("Sampling frequency fs must be > 0")

    ecg = np.asarray(ecg)

    # 1) High-pass filter (baseline wander)
    b_hp, a_hp = signal.butter(
        N=4,
        Wn=0.5,
        btype="highpass",
        fs=fs
    )
    ecg_hp = signal.filtfilt(b_hp, a_hp, ecg)

    # 2) Notch filter (50 Hz powerline noise)
    b_notch, a_notch = signal.iirnotch(
        w0=50,
        Q=30,
        fs=fs
    )
    ecg_notch = signal.filtfilt(b_notch, a_notch, ecg_hp)

    # 3) Low-pass filter (EMG / high-frequency noise)
    b_lp, a_lp = signal.butter(
        N=4,
        Wn=40,
        btype="lowpass",
        fs=fs
    )
    ecg_filtered = signal.filtfilt(b_lp, a_lp, ecg_notch)

    return ecg_filtered

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def save_time_plot(path, raw, filtered, fs):
    """
    Saves a time-domain plot comparing raw and filtered ECG.
    """
    if fs <= 0:
        raise ValueError("Sampling frequency fs must be > 0")

    raw = np.asarray(raw)
    filtered = np.asarray(filtered)

    t = np.arange(len(raw)) / fs

    plt.figure(figsize=(10, 4))
    plt.plot(t, raw, label="Raw", alpha=0.8)
    plt.plot(t, filtered, label="Filtered", alpha=0.8)

    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.title("ECG: Raw vs Filtered")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def save_spectrum_plot(path, raw, filtered, fs):
    """
    Saves a frequency-domain magnitude spectrum plot
    showing BOTH raw and filtered ECG.
    """
    if fs <= 0:
        raise ValueError("Sampling frequency fs must be > 0")

    raw = np.asarray(raw)
    filtered = np.asarray(filtered)

    plt.figure(figsize=(8, 4))

    # Raw spectrum
    plt.magnitude_spectrum(
        raw,
        Fs=fs,
        scale="dB",
        label="Raw",
        alpha=0.8,
    )

    # Filtered spectrum
    plt.magnitude_spectrum(
        filtered,
        Fs=fs,
        scale="dB",
        label="Filtered",
        alpha=0.8,
    )

    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude [dB]")
    plt.title("Spectrum: Raw vs Filtered ECG")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()

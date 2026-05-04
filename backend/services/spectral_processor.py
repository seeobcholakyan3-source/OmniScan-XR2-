import numpy as np
import logging

logger = logging.getLogger("spectral-processor")


def normalize_spectrum(spectrum):
    spectrum = np.array(spectrum, dtype=float)

    if spectrum.size == 0:
        raise ValueError("Empty spectrum")

    max_val = np.max(spectrum)
    if max_val == 0:
        return spectrum

    return spectrum / max_val


def extract_features(spectrum):
    spectrum = normalize_spectrum(spectrum)

    return {
        "mean": float(np.mean(spectrum)),
        "std": float(np.std(spectrum)),
        "max": float(np.max(spectrum)),
        "min": float(np.min(spectrum))
    }

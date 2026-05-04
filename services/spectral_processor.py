import numpy as np
import logging

logger = logging.getLogger("spectral-processor")

# ==========================================================
# CORE SPECTRAL NORMALIZATION
# ==========================================================

def normalize_spectrum(spectrum):
    """
    Normalize spectral values between 0–1.
    Prevents scale distortion from satellite inputs.
    """
    try:
        spectrum = np.array(spectrum, dtype=float)

        if spectrum.size == 0:
            raise ValueError("Empty spectrum received")

        max_val = np

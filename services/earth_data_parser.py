import numpy as np

class EarthDataParser:
    """
    Converts satellite raster data into simplified scan signals.
    This simulates processing of:
    - Sentinel-2 bands
    - NASA EMIT spectral outputs
    """

    def parse_spectral_array(self, spectral_array):
        """
        Input: multi-band raster array (simulated as numpy array)
        Output: extracted geospatial features
        """

        # Normalize data
        normalized = spectral_array / (np.max(spectral_array) + 1e-6)

        return {
            "mean_reflectance": float(np.mean(normalized)),
            "variance": float(np.var(normalized)),
            "high_intensity_ratio": float(np.sum(normalized > 0.8) / normalized.size)
        }

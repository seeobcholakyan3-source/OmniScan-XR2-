import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os


class AnomalyModel:
    """
    Unsupervised anomaly detection for geospatial signals.
    Uses Isolation Forest (standard in real-world anomaly systems).
    """

    def __init__(self):
        self.model_path = "model.joblib"
        self.model = self._load_or_train()

    def _load_or_train(self):
        if os.path.exists(self.model_path):
            return joblib.load(self.model_path)

        # Train on synthetic baseline geospatial behavior
        X = np.random.rand(500, 2)  # [density, anomaly]

        model = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42
        )

        model.fit(X)
        joblib.dump(model, self.model_path)

        return model

    def predict(self, density_index, anomaly_score):
        features = np.array([[density_index / 100, anomaly_score / 100]])

        prediction = self.model.predict(features)[0]

        return {
            "is_anomaly": prediction == -1,
            "confidence_score": float(
                abs(self.model.decision_function(features)[0])
            )
        }

# src/classify.py
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import os

# Load training features and labels
# These should be pre-saved using extract_features() + labels
FEATURES_PATH = "data/train_features.npy"
LABELS_PATH = "data/train_labels.npy"

# Load at module level to avoid reloading on every inference
if os.path.exists(FEATURES_PATH) and os.path.exists(LABELS_PATH):
    train_features = np.load(FEATURES_PATH)
    train_labels = np.load(LABELS_PATH)
    
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(train_features, train_labels)
else:
    raise FileNotFoundError("Training features or labels not found. Please generate them first.")

def classify_image(features_tensor):
    """
    features_tensor: Torch tensor of shape [1, D] from DINOv2
    Returns:
        - predicted class (str)
        - confidence score (float between 0 and 1)
    """
    feature = features_tensor.detach().cpu().numpy()
    prediction = knn.predict(feature)[0]
    probs = knn.predict_proba(feature)[0]
    confidence = max(probs)

    return prediction, confidence

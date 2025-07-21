# src/generate_train_features.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from src.extract_features import extract_features

# Set your dataset directory
DATASET_DIR = "data/train"  # e.g., data/train/class1/img1.jpg, data/train/class2/img2.jpg

features = []
labels = []

for class_name in os.listdir(DATASET_DIR):
    class_dir = os.path.join(DATASET_DIR, class_name)
    if not os.path.isdir(class_dir):
        continue
    for fname in os.listdir(class_dir):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(class_dir, fname)
            feat = extract_features(img_path)
            features.append(feat.detach().cpu().numpy().flatten())
            labels.append(class_name)

features = np.stack(features)
labels = np.array(labels)

np.save("data/train_features.npy", features)
np.save("data/train_labels.npy", labels)

print("Saved features to data/train_features.npy and labels to data/train_labels.npy")
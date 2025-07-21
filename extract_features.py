# src/extract_features.py
from transformers import AutoProcessor, AutoModel
import torch
from PIL import Image

model = AutoModel.from_pretrained("facebook/dinov2-base")
processor = AutoProcessor.from_pretrained("facebook/dinov2-base", use_fast=True)

def extract_features(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs)
    return output.last_hidden_state.mean(dim=1)

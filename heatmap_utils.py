import torch
import cv2
import numpy as np
from PIL import Image
import os

def generate_gradcam(image_path, model, target_layer, class_idx=None, output_path="heatmap.jpg"):
    """
    Generate a Grad-CAM heatmap for the given image and model.
    Args:
        image_path (str): Path to the input image.
        model (torch.nn.Module): The model to use.
        target_layer (torch.nn.Module): The layer to compute Grad-CAM for.
        class_idx (int, optional): The class index for which to compute Grad-CAM. If None, uses predicted class.
        output_path (str): Where to save the heatmap image.
    Returns:
        output_path (str): Path to the saved heatmap image.
    """
    # Preprocess image
    img = Image.open(image_path).convert("RGB")
    img_resized = img.resize((224, 224))
    img_np = np.array(img_resized)
    img_tensor = torch.from_numpy(img_np).permute(2, 0, 1).unsqueeze(0).float() / 255.0

    # Enable gradients for input
    img_tensor.requires_grad = True

    # Hook the gradients and activations
    activations = []
    gradients = []

    def forward_hook(module, input, output):
        activations.append(output.detach())

    def backward_hook(module, grad_in, grad_out):
        gradients.append(grad_out[0].detach())

    handle_fwd = target_layer.register_forward_hook(forward_hook)
    handle_bwd = target_layer.register_backward_hook(backward_hook)

    # Forward pass
    model.eval()
    output = model(img_tensor)
    if class_idx is None:
        class_idx = output.argmax(dim=1).item()

    # Backward pass
    model.zero_grad()
    loss = output[0, class_idx]
    loss.backward()

    # Get hooked data
    acts = activations[0][0]  # [C, H, W]
    grads = gradients[0][0]   # [C, H, W]

    # Compute weights and Grad-CAM
    weights = grads.mean(dim=(1, 2))
    gradcam = torch.zeros(acts.shape[1:], dtype=torch.float32)
    for i, w in enumerate(weights):
        gradcam += w * acts[i]
    gradcam = torch.relu(gradcam)
    gradcam = gradcam - gradcam.min()
    gradcam = gradcam / (gradcam.max() + 1e-8)
    gradcam = gradcam.cpu().numpy()
    gradcam = cv2.resize(gradcam, (img_np.shape[1], img_np.shape[0]))
    heatmap = (gradcam * 255).astype(np.uint8)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Ensure img_np is 3-channel BGR and same size as heatmap
    if img_np.shape[2] == 1:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2BGR)
    elif img_np.shape[2] == 3:
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    img_np = cv2.resize(img_np, (224, 224))

    # Now both img_np and heatmap are (224, 224, 3)
    overlay = cv2.addWeighted(img_np, 0.5, heatmap, 0.5, 0)

    # Save the heatmap as a valid .jpg file
    cv2.imwrite(output_path, overlay)
    print(f"[GradCAM] Saved heatmap to: {output_path}, exists: {os.path.exists(output_path)}")
    handle_fwd.remove()
    handle_bwd.remove()
    return output_path
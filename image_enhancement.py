# src/image_enhancement.py
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os
from typing import Tuple, Dict, Optional
import logging

class ImageEnhancer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.enhancement_settings = {
            "brightness": 1.2,
            "contrast": 1.3,
            "sharpness": 1.5,
            "saturation": 1.1
        }
    
    def enhance_image(self, image_path: str, output_path: str = None) -> str:
        """
        Comprehensive image enhancement for better disease detection
        
        Args:
            image_path: Path to input image
            output_path: Path for enhanced image (optional)
            
        Returns:
            str: Path to enhanced image
        """
        try:
            # Load image
            original_image = Image.open(image_path)
            
            # Apply enhancements
            enhanced_image = self._apply_enhancements(original_image)
            
            # Auto-crop to focus on leaf
            cropped_image = self._auto_crop_leaf(enhanced_image)
            
            # Resize for optimal processing
            resized_image = self._resize_for_analysis(cropped_image)
            
            # Save enhanced image
            if output_path is None:
                base_name = os.path.splitext(image_path)[0]
                output_path = f"{base_name}_enhanced.jpg"
            
            resized_image.save(output_path, "JPEG", quality=95)
            
            self.logger.info(f"Image enhanced successfully: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error enhancing image: {e}")
            return image_path  # Return original if enhancement fails
    
    def _apply_enhancements(self, image: Image.Image) -> Image.Image:
        """Apply various image enhancements"""
        enhanced = image
        
        # Brightness enhancement
        brightness_enhancer = ImageEnhance.Brightness(enhanced)
        enhanced = brightness_enhancer.enhance(self.enhancement_settings["brightness"])
        
        # Contrast enhancement
        contrast_enhancer = ImageEnhance.Contrast(enhanced)
        enhanced = contrast_enhancer.enhance(self.enhancement_settings["contrast"])
        
        # Sharpness enhancement
        sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
        enhanced = sharpness_enhancer.enhance(self.enhancement_settings["sharpness"])
        
        # Color saturation enhancement
        color_enhancer = ImageEnhance.Color(enhanced)
        enhanced = color_enhancer.enhance(self.enhancement_settings["saturation"])
        
        return enhanced
    
    def _auto_crop_leaf(self, image: Image.Image) -> Image.Image:
        """Automatically crop image to focus on the leaf"""
        try:
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Convert to HSV for better leaf detection
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
            
            # Create mask for green/brown colors (typical leaf colors)
            lower_green = np.array([35, 40, 40])
            upper_green = np.array([85, 255, 255])
            
            # Create mask
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Apply morphological operations to clean up mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find the largest contour (likely the main leaf)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get bounding rectangle
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Add padding around the crop
                padding = 20
                x = max(0, x - padding)
                y = max(0, y - padding)
                w = min(cv_image.shape[1] - x, w + 2 * padding)
                h = min(cv_image.shape[0] - y, h + 2 * padding)
                
                # Crop the image
                cropped_cv = cv_image[y:y+h, x:x+w]
                
                # Convert back to PIL
                cropped_pil = Image.fromarray(cv2.cvtColor(cropped_cv, cv2.COLOR_BGR2RGB))
                
                return cropped_pil
            
        except Exception as e:
            self.logger.warning(f"Auto-crop failed: {e}")
        
        # Return original if cropping fails
        return image
    
    def _resize_for_analysis(self, image: Image.Image) -> Image.Image:
        """Resize image to optimal size for AI analysis"""
        # Optimal size for DINOv2 model
        target_size = (224, 224)
        
        # Maintain aspect ratio
        image.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Create new image with target size and paste resized image
        new_image = Image.new("RGB", target_size, (255, 255, 255))
        
        # Center the image
        x = (target_size[0] - image.width) // 2
        y = (target_size[1] - image.height) // 2
        new_image.paste(image, (x, y))
        
        return new_image
    
    def detect_image_quality(self, image_path: str) -> Dict:
        """Analyze image quality and provide recommendations"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "Could not load image"}
            
            # Calculate quality metrics
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Sharpness (using Laplacian variance)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Brightness
            brightness = np.mean(gray)
            
            # Contrast
            contrast = np.std(gray)
            
            # Resolution
            height, width = image.shape[:2]
            resolution = width * height
            
            # Quality assessment
            quality_score = self._calculate_quality_score(sharpness, brightness, contrast, resolution)
            
            return {
                "sharpness": round(sharpness, 2),
                "brightness": round(brightness, 2),
                "contrast": round(contrast, 2),
                "resolution": resolution,
                "dimensions": f"{width}x{height}",
                "quality_score": quality_score,
                "recommendations": self._get_quality_recommendations(sharpness, brightness, contrast, resolution)
            }
            
        except Exception as e:
            return {"error": f"Quality analysis failed: {str(e)}"}
    
    def _calculate_quality_score(self, sharpness: float, brightness: float, 
                               contrast: float, resolution: int) -> float:
        """Calculate overall image quality score (0-100)"""
        # Normalize metrics
        sharpness_score = min(sharpness / 100, 1.0) * 30  # Max 30 points
        brightness_score = max(0, 1 - abs(brightness - 128) / 128) * 25  # Max 25 points
        contrast_score = min(contrast / 50, 1.0) * 25  # Max 25 points
        resolution_score = min(resolution / 1000000, 1.0) * 20  # Max 20 points
        
        total_score = sharpness_score + brightness_score + contrast_score + resolution_score
        return round(total_score, 1)
    
    def _get_quality_recommendations(self, sharpness: float, brightness: float, 
                                   contrast: float, resolution: int) -> list:
        """Get recommendations for improving image quality"""
        recommendations = []
        
        if sharpness < 50:
            recommendations.append("Image is blurry - try taking a clearer photo")
        
        if brightness < 80:
            recommendations.append("Image is too dark - improve lighting")
        elif brightness > 180:
            recommendations.append("Image is too bright - reduce lighting")
        
        if contrast < 30:
            recommendations.append("Low contrast - try different lighting conditions")
        
        if resolution < 500000:  # Less than 500K pixels
            recommendations.append("Low resolution - use a higher quality camera")
        
        if not recommendations:
            recommendations.append("Image quality is good for analysis")
        
        return recommendations
    
    def batch_enhance(self, image_paths: list, output_dir: str = "enhanced_images") -> Dict:
        """Enhance multiple images in batch"""
        results = {
            "successful": [],
            "failed": [],
            "quality_reports": {}
        }
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        for image_path in image_paths:
            try:
                # Generate output path
                filename = os.path.basename(image_path)
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(output_dir, f"{name}_enhanced.jpg")
                
                # Enhance image
                enhanced_path = self.enhance_image(image_path, output_path)
                
                # Analyze quality
                quality_report = self.detect_image_quality(enhanced_path)
                
                results["successful"].append({
                    "original": image_path,
                    "enhanced": enhanced_path,
                    "quality": quality_report
                })
                
                results["quality_reports"][enhanced_path] = quality_report
                
            except Exception as e:
                results["failed"].append({
                    "path": image_path,
                    "error": str(e)
                })
        
        return results

# Global enhancer instance
image_enhancer = ImageEnhancer() 
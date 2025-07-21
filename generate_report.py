from fpdf import FPDF
import os
from src.disease_info import DISEASE_INFO
from datetime import datetime

def generate_pdf_report(image_path, prediction, severity, heatmap_path):
    # Extract class name (remove confidence if present)
    class_name = prediction.split(' (')[0]
    info = DISEASE_INFO.get(class_name, {
        "description": "No description available.",
        "treatment": "No treatment advice available."
    })

    pdf = FPDF()
    pdf.add_page()
    
    # Header with LeafGuard AI branding
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(46, 139, 87)  # Green color
    pdf.cell(200, 15, "LeafGuard AI", ln=1, align='C')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, "Plant Disease Detection Report", ln=1, align='C')
    
    # Date and time
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 8, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1, align='C')
    
    # Separator line
    pdf.line(10, 45, 200, 45)
    
    # Analysis results
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, "", ln=1)  # Spacing
    pdf.cell(200, 10, "ANALYSIS RESULTS", ln=1)
    
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 8, f"Disease Detected: {prediction}", ln=1)
    pdf.cell(200, 8, f"Severity Level: {severity}%", ln=1)
    
    # Confidence level (if available in prediction)
    if '(' in prediction:
        confidence = prediction.split('(')[1].split(')')[0]
        pdf.cell(200, 8, f"Confidence: {confidence}", ln=1)
    
    # Disease information
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "", ln=1)  # Spacing
    pdf.cell(200, 10, "DISEASE INFORMATION", ln=1)
    
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, f"Description: {info['description']}")
    pdf.cell(200, 5, "", ln=1)  # Spacing
    pdf.multi_cell(0, 8, f"Treatment Advice: {info['treatment']}")
    
    # Images section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "", ln=1)  # Spacing
    pdf.cell(200, 10, "VISUAL ANALYSIS", ln=1)
    
    y_pos = 120
    image_added = False
    
    # Original image
    if os.path.exists(image_path):
        try:
            pdf.image(image_path, x=10, y=y_pos, w=80)
            pdf.set_font("Arial", size=8)
            pdf.cell(80, 5, "Original Image", ln=0, align='C')
            image_added = True
        except Exception as e:
            print(f"Error adding image {image_path} to PDF: {e}")
    
    # Heatmap image
    if os.path.exists(heatmap_path):
        try:
            pdf.image(heatmap_path, x=110, y=y_pos, w=80)
            pdf.set_font("Arial", size=8)
            pdf.cell(80, 5, "AI Heatmap Analysis", ln=1, align='C')
            image_added = True
        except Exception as e:
            print(f"Error adding heatmap {heatmap_path} to PDF: {e}")
    
    if not image_added:
        pdf.cell(200, 10, "[Images not available]", ln=1)
    
    # Footer
    pdf.set_y(-30)
    pdf.set_font("Arial", size=10)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(200, 8, "", ln=1)  # Spacing
    pdf.cell(200, 8, "LeafGuard AI - AI-Powered Plant Disease Detection", ln=1, align='C')
    pdf.cell(200, 8, "Protecting crops with intelligent monitoring", ln=1, align='C')

    report_path = "LeafGuard_AI_Report.pdf"
    pdf.output(report_path)
    return report_path
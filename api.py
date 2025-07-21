# src/api.py
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse, JSONResponse
import shutil
import os
import mimetypes
from src.pipeline import process_image  # Includes feature extraction, classify, heatmap, severity, report
from src.models import SessionLocal, UserResult

app = FastAPI(
    title="LeafGuard AI API",
    description="AI-Powered Plant Disease Detection & Analysis API",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return PlainTextResponse("🌱 LeafGuard AI API is running. Use /predict/ for plant disease analysis.")

@app.post("/predict/")
async def predict(file: UploadFile):
    try:
        print(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()
        content_type = file.content_type

        # Try to guess content type if not provided
        if not content_type:
            guessed_type, _ = mimetypes.guess_type(filename)
            content_type = guessed_type

        if (not content_type or not content_type.startswith('image/')) and ext not in ALLOWED_EXTENSIONS:
            print(f"Invalid file type: {content_type}, extension: {ext}")
            raise HTTPException(status_code=400, detail="Only image files are supported")
        
        # Save uploaded image
        print(f"Saving file to input.jpg...")
        with open("input.jpg", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"File saved successfully. File size: {os.path.getsize('input.jpg')} bytes")
        
        # Process image through LeafGuard AI pipeline
        print("Starting image processing pipeline...")
        prediction, confidence, severity, report_path, enhancement_info = process_image("input.jpg")
        print(f"Pipeline completed. Prediction: {prediction}, Confidence: {confidence}, Severity: {severity}")
        
        # Store result in database
        db = SessionLocal()
        db_result = UserResult(
            image_path="input.jpg",
            prediction=prediction,
            confidence=confidence,
            severity=severity,
            report_path=report_path
        )
        db.add(db_result)
        db.commit()
        db.refresh(db_result)
        db.close()
        
        # Validate report generation
        if not os.path.exists(report_path) or os.path.getsize(report_path) < 100:
            raise Exception("LeafGuard AI report generation failed - PDF is missing or corrupted.")
        
        # Return branded PDF report
        return FileResponse(
            report_path, 
            media_type='application/pdf', 
            filename=f"LeafGuard_AI_Report_{file.filename}.pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"LeafGuard AI Error in /predict/: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"LeafGuard AI analysis failed: {str(e)}"
        )

@app.get("/results/")
def get_results():
    """Get all stored LeafGuard AI analysis results"""
    try:
        db = SessionLocal()
        results = db.query(UserResult).all()
        db.close()
        return JSONResponse([
            {
                "id": r.id,
                "image_path": r.image_path,
                "prediction": r.prediction,
                "confidence": r.confidence,
                "severity": r.severity,
                "report_path": r.report_path,
                "timestamp": r.timestamp.isoformat() if getattr(r, "timestamp", None) is not None else None
            }
            for r in results
        ])
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to retrieve LeafGuard AI results: {str(e)}"
        )

@app.get("/health")
def health_check():
    """Health check endpoint for LeafGuard AI"""
    return {"status": "healthy", "service": "LeafGuard AI", "version": "1.0.0"}

"""
Models API endpoints for ML model management
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Dict, Any
import os
from pathlib import Path

from config.settings import settings

router = APIRouter()

@router.get("/")
async def list_models():
    """List available models"""
    models_dir = Path(settings.MODELS_DIR)
    models = []
    
    if models_dir.exists():
        for model_path in models_dir.iterdir():
            if model_path.is_dir():
                models.append({
                    "id": model_path.name,
                    "name": model_path.name,
                    "path": str(model_path),
                    "type": "custom"
                })
    
    return {"models": models}

@router.post("/upload")
async def upload_model(file: UploadFile = File(...)):
    """Upload custom model"""
    try:
        models_dir = Path(settings.MODELS_DIR)
        models_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = models_dir / file.filename
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "message": f"Model {file.filename} uploaded successfully",
            "path": str(file_path)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{model_id}")
async def delete_model(model_id: str):
    """Delete model"""
    try:
        model_path = Path(settings.MODELS_DIR) / model_id
        
        if not model_path.exists():
            raise HTTPException(status_code=404, detail="Model not found")
        
        if model_path.is_dir():
            import shutil
            shutil.rmtree(model_path)
        else:
            model_path.unlink()
        
        return {"message": f"Model {model_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{model_id}/inference")
async def run_inference(model_id: str, inference_data: Dict[str, Any]):
    """Run inference with model"""
    # TODO: Implement model inference
    return {
        "model_id": model_id,
        "input": inference_data,
        "output": "Inference result will be implemented"
    }
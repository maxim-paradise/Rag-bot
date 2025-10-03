"""
ML Experiments API endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
import asyncio

from models.experiment import (
    MLExperiment, ExperimentCreateRequest, TrainingRequest,
    ExperimentType, ExperimentStatus
)
from services.ml_experiment_service import MLExperimentService

router = APIRouter()
ml_service = MLExperimentService()

@router.post("/experiments", response_model=MLExperiment)
async def create_experiment(request: ExperimentCreateRequest):
    """Create a new ML experiment"""
    try:
        experiment = await ml_service.create_experiment(
            name=request.name,
            experiment_type=request.type,
            description=request.description,
            config=request.config
        )
        return experiment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/experiments", response_model=List[MLExperiment])
async def list_experiments():
    """List all experiments"""
    try:
        experiments = await ml_service.list_experiments()
        return experiments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/experiments/{experiment_id}", response_model=MLExperiment)
async def get_experiment(experiment_id: str):
    """Get experiment by ID"""
    try:
        experiment = await ml_service.get_experiment(experiment_id)
        return experiment
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/experiments/{experiment_id}/train")
async def train_model(
    experiment_id: str,
    training_request: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Start model training"""
    try:
        # Validate experiment exists
        experiment = await ml_service.get_experiment(experiment_id)
        
        if experiment.status != ExperimentStatus.CREATED:
            raise HTTPException(
                status_code=400,
                detail=f"Experiment is in {experiment.status} status, cannot train"
            )
        
        # Start training in background
        if experiment.type == ExperimentType.TEXT_CLASSIFICATION:
            background_tasks.add_task(
                ml_service.train_text_classifier,
                experiment_id=experiment_id,
                **training_request
            )
        else:
            background_tasks.add_task(
                ml_service.run_transformer_experiment,
                experiment_id=experiment_id,
                **training_request
            )
        
        return {"message": "Training started", "experiment_id": experiment_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/experiments/quick-demo")
async def quick_demo(demo_config: Dict[str, Any]):
    """Run a quick ML demo"""
    try:
        task = demo_config.get("task", "sentiment-analysis")
        model_name = demo_config.get("model", "distilbert-base-uncased-finetuned-sst-2-english")
        
        # Create temporary experiment
        experiment = await ml_service.create_experiment(
            name=f"Quick Demo - {task}",
            experiment_type=ExperimentType.SENTIMENT_ANALYSIS,
            description="Quick demonstration experiment"
        )
        
        # Run experiment
        results = await ml_service.run_transformer_experiment(
            experiment_id=experiment.id,
            task=task,
            model_name=model_name,
            dataset_name="demo",
            **demo_config
        )
        
        return {
            "experiment_id": experiment.id,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/available")
async def get_available_models():
    """Get list of available pre-trained models"""
    models = {
        "text_classification": [
            "distilbert-base-uncased",
            "bert-base-uncased",
            "roberta-base",
            "albert-base-v2"
        ],
        "text_generation": [
            "gpt2",
            "gpt2-medium",
            "distilgpt2",
            "microsoft/DialoGPT-medium"
        ],
        "question_answering": [
            "distilbert-base-cased-distilled-squad",
            "bert-large-uncased-whole-word-masking-finetuned-squad",
            "roberta-base-squad2"
        ],
        "sentiment_analysis": [
            "distilbert-base-uncased-finetuned-sst-2-english",
            "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "nlptown/bert-base-multilingual-uncased-sentiment"
        ]
    }
    return models

@router.get("/experiments/{experiment_id}/visualize")
async def visualize_experiment(experiment_id: str):
    """Generate visualizations for experiment"""
    try:
        experiment = await ml_service.get_experiment(experiment_id)
        
        if not experiment.results:
            raise HTTPException(
                status_code=400,
                detail="No results available for visualization"
            )
        
        # Generate visualizations based on experiment type
        viz_data = {
            "experiment_id": experiment_id,
            "type": experiment.type,
            "results": experiment.results,
            "charts": []
        }
        
        # Add specific visualizations based on experiment type
        if experiment.type == ExperimentType.TEXT_CLASSIFICATION:
            viz_data["charts"] = [
                "confusion_matrix",
                "metrics_bar_chart",
                "training_curves"
            ]
        elif experiment.type == ExperimentType.SENTIMENT_ANALYSIS:
            viz_data["charts"] = [
                "sentiment_distribution",
                "confidence_histogram"
            ]
        
        return viz_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
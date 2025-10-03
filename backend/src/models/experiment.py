"""
ML Experiment Models
"""

from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel

class ExperimentType(str, Enum):
    """Types of ML experiments"""
    TEXT_CLASSIFICATION = "text_classification"
    TEXT_GENERATION = "text_generation"
    QUESTION_ANSWERING = "question_answering"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    NAMED_ENTITY_RECOGNITION = "named_entity_recognition"
    COMPUTER_VISION = "computer_vision"
    CUSTOM = "custom"

class ExperimentStatus(str, Enum):
    """Status of ML experiments"""
    CREATED = "created"
    TRAINING = "training"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class MLExperiment(BaseModel):
    """ML Experiment model"""
    id: str
    name: str
    type: ExperimentType
    description: str = ""
    status: ExperimentStatus = ExperimentStatus.CREATED
    config: Dict[str, Any] = {}
    results: Optional[Dict[str, Any]] = None
    model_path: Optional[str] = None
    experiment_dir: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

class TrainingRequest(BaseModel):
    """Request model for training"""
    experiment_id: str
    model_name: str
    dataset_config: Dict[str, Any]
    training_config: Dict[str, Any] = {}

class InferenceRequest(BaseModel):
    """Request model for inference"""
    model_path: str
    input_data: Dict[str, Any]
    config: Dict[str, Any] = {}

class ExperimentCreateRequest(BaseModel):
    """Request model for creating experiment"""
    name: str
    type: ExperimentType
    description: str = ""
    config: Dict[str, Any] = {}
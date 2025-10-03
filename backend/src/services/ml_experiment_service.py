"""
Machine Learning Experiment Service
Handles ML model training, evaluation, and experimentation
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

try:
    from transformers import (
        AutoTokenizer, AutoModel, AutoModelForSequenceClassification,
        TrainingArguments, Trainer, pipeline
    )
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    from datasets import Dataset
    DATASETS_AVAILABLE = True
except ImportError:
    DATASETS_AVAILABLE = False

try:
    import numpy as np
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import wandb
    WANDB_AVAILABLE = True
except ImportError:
    WANDB_AVAILABLE = False

from config.settings import settings
from models.experiment import MLExperiment, ExperimentStatus, ExperimentType

class MLExperimentService:
    """Service for managing ML experiments"""
    
    def __init__(self):
        self.experiments_dir = Path(settings.EXPERIMENTS_DIR)
        self.models_dir = Path(settings.MODELS_DIR)
        self.device = self._get_device()
        
    def _get_device(self) -> str:
        """Get the appropriate device for training"""
        if not TORCH_AVAILABLE:
            return "cpu"
            
        if settings.DEVICE == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        return settings.DEVICE
    
    async def create_experiment(
        self,
        name: str,
        experiment_type: ExperimentType,
        description: str = "",
        config: Dict[str, Any] = None
    ) -> MLExperiment:
        """Create a new ML experiment"""
        
        experiment_id = str(uuid.uuid4())
        experiment_dir = self.experiments_dir / experiment_id
        experiment_dir.mkdir(parents=True, exist_ok=True)
        
        experiment = MLExperiment(
            id=experiment_id,
            name=name,
            type=experiment_type,
            description=description,
            status=ExperimentStatus.CREATED,
            config=config or {},
            created_at=datetime.now(),
            experiment_dir=str(experiment_dir)
        )
        
        # Save experiment metadata
        self._save_experiment_metadata(experiment)
        
        return experiment
    
    async def train_text_classifier(
        self,
        experiment_id: str,
        model_name: str,
        train_data: List[Dict[str, Any]],
        val_data: Optional[List[Dict[str, Any]]] = None,
        num_labels: int = 2,
        training_args: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Train a text classification model"""
        
        if not TRANSFORMERS_AVAILABLE:
            raise RuntimeError("Transformers library not available. Install with: pip install transformers")
        
        if not DATASETS_AVAILABLE:
            raise RuntimeError("Datasets library not available. Install with: pip install datasets")
        
        experiment = await self.get_experiment(experiment_id)
        experiment.status = ExperimentStatus.TRAINING
        self._save_experiment_metadata(experiment)
        
        try:
            # Initialize W&B if available
            if settings.WANDB_API_KEY and WANDB_AVAILABLE:
                wandb.init(
                    project=settings.WANDB_PROJECT,
                    name=f"{experiment.name}_{experiment_id[:8]}",
                    config=experiment.config
                )
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=num_labels
            )
            
            # Prepare datasets
            train_dataset = self._prepare_text_dataset(train_data, tokenizer)
            val_dataset = None
            if val_data:
                val_dataset = self._prepare_text_dataset(val_data, tokenizer)
            
            # Training arguments
            default_args = {
                "output_dir": str(experiment.experiment_dir / "checkpoints"),
                "num_train_epochs": settings.DEFAULT_EPOCHS,
                "per_device_train_batch_size": settings.DEFAULT_BATCH_SIZE,
                "per_device_eval_batch_size": settings.DEFAULT_BATCH_SIZE,
                "learning_rate": settings.DEFAULT_LEARNING_RATE,
                "warmup_steps": 500,
                "weight_decay": 0.01,
                "logging_dir": str(experiment.experiment_dir / "logs"),
                "logging_steps": 10,
                "evaluation_strategy": "epoch" if val_dataset else "no",
                "save_strategy": "epoch",
                "load_best_model_at_end": True if val_dataset else False,
                "report_to": "wandb" if (settings.WANDB_API_KEY and WANDB_AVAILABLE) else "none"
            }
            
            if training_args:
                default_args.update(training_args)
            
            training_arguments = TrainingArguments(**default_args)
            
            # Initialize trainer
            trainer = Trainer(
                model=model,
                args=training_arguments,
                train_dataset=train_dataset,
                eval_dataset=val_dataset,
                tokenizer=tokenizer,
                compute_metrics=self._compute_metrics
            )
            
            # Train model
            trainer.train()
            
            # Save model
            model_path = experiment.experiment_dir / "final_model"
            trainer.save_model(str(model_path))
            tokenizer.save_pretrained(str(model_path))
            
            # Evaluate model
            results = {}
            if val_dataset:
                eval_results = trainer.evaluate()
                results["validation"] = eval_results
            
            # Update experiment
            experiment.status = ExperimentStatus.COMPLETED
            experiment.results = results
            experiment.model_path = str(model_path)
            experiment.completed_at = datetime.now()
            
            self._save_experiment_metadata(experiment)
            
            if settings.WANDB_API_KEY and WANDB_AVAILABLE:
                wandb.finish()
            
            return results
            
        except Exception as e:
            experiment.status = ExperimentStatus.FAILED
            experiment.error_message = str(e)
            self._save_experiment_metadata(experiment)
            raise e
    
    async def run_transformer_experiment(
        self,
        experiment_id: str,
        task: str,
        model_name: str,
        dataset_name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Run a transformer-based experiment"""
        
        if not TRANSFORMERS_AVAILABLE:
            raise RuntimeError("Transformers library not available. Install with: pip install transformers")
        
        experiment = await self.get_experiment(experiment_id)
        experiment.status = ExperimentStatus.TRAINING
        self._save_experiment_metadata(experiment)
        
        try:
            # Create pipeline based on task
            pipe = pipeline(
                task=task,
                model=model_name,
                device=0 if self.device == "cuda" else -1
            )
            
            # Run experiment based on task type
            if task == "text-generation":
                results = await self._run_text_generation_experiment(pipe, **kwargs)
            elif task == "sentiment-analysis":
                results = await self._run_sentiment_analysis_experiment(pipe, **kwargs)
            elif task == "question-answering":
                results = await self._run_qa_experiment(pipe, **kwargs)
            else:
                raise ValueError(f"Unsupported task: {task}")
            
            # Update experiment
            experiment.status = ExperimentStatus.COMPLETED
            experiment.results = results
            experiment.completed_at = datetime.now()
            self._save_experiment_metadata(experiment)
            
            return results
            
        except Exception as e:
            experiment.status = ExperimentStatus.FAILED
            experiment.error_message = str(e)
            self._save_experiment_metadata(experiment)
            raise e
    
    async def get_experiment(self, experiment_id: str) -> MLExperiment:
        """Get experiment by ID"""
        experiment_file = self.experiments_dir / experiment_id / "metadata.json"
        
        if not experiment_file.exists():
            raise ValueError(f"Experiment {experiment_id} not found")
        
        with open(experiment_file, 'r') as f:
            data = json.load(f)
        
        return MLExperiment(**data)
    
    async def list_experiments(self) -> List[MLExperiment]:
        """List all experiments"""
        experiments = []
        
        for exp_dir in self.experiments_dir.iterdir():
            if exp_dir.is_dir():
                metadata_file = exp_dir / "metadata.json"
                if metadata_file.exists():
                    try:
                        with open(metadata_file, 'r') as f:
                            data = json.load(f)
                        experiments.append(MLExperiment(**data))
                    except Exception:
                        continue
        
        return sorted(experiments, key=lambda x: x.created_at, reverse=True)
    
    def _prepare_text_dataset(self, data: List[Dict[str, Any]], tokenizer):
        """Prepare text dataset for training"""
        if not DATASETS_AVAILABLE:
            # Fallback to simple dict structure
            texts = [item["text"] for item in data]
            labels = [item["label"] for item in data]
            
            encodings = tokenizer(
                texts,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt"
            )
            
            return {
                "input_ids": encodings["input_ids"],
                "attention_mask": encodings["attention_mask"],
                "labels": labels
            }
        
        texts = [item["text"] for item in data]
        labels = [item["label"] for item in data]
        
        encodings = tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="pt"
        )
        
        dataset = Dataset.from_dict({
            "input_ids": encodings["input_ids"],
            "attention_mask": encodings["attention_mask"],
            "labels": labels
        })
        
        return dataset
    
    def _compute_metrics(self, eval_pred):
        """Compute metrics for evaluation"""
        if not SKLEARN_AVAILABLE:
            return {"accuracy": 0.0}
            
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        
        precision, recall, f1, _ = precision_recall_fscore_support(
            labels, predictions, average='weighted'
        )
        accuracy = accuracy_score(labels, predictions)
        
        return {
            'accuracy': accuracy,
            'f1': f1,
            'precision': precision,
            'recall': recall
        }
    
    async def _run_text_generation_experiment(self, pipe, **kwargs) -> Dict[str, Any]:
        """Run text generation experiment"""
        prompts = kwargs.get("prompts", ["Hello, how are you?"])
        max_length = kwargs.get("max_length", 100)
        
        results = []
        for prompt in prompts:
            output = pipe(prompt, max_length=max_length, num_return_sequences=1)
            results.append({
                "prompt": prompt,
                "generated_text": output[0]["generated_text"]
            })
        
        return {"generations": results}
    
    async def _run_sentiment_analysis_experiment(self, pipe, **kwargs) -> Dict[str, Any]:
        """Run sentiment analysis experiment"""
        texts = kwargs.get("texts", ["I love this!", "This is terrible."])
        
        results = []
        for text in texts:
            output = pipe(text)
            results.append({
                "text": text,
                "sentiment": output[0]["label"],
                "confidence": output[0]["score"]
            })
        
        return {"predictions": results}
    
    async def _run_qa_experiment(self, pipe, **kwargs) -> Dict[str, Any]:
        """Run question answering experiment"""
        questions = kwargs.get("questions", [])
        context = kwargs.get("context", "")
        
        results = []
        for question in questions:
            output = pipe(question=question, context=context)
            results.append({
                "question": question,
                "answer": output["answer"],
                "confidence": output["score"]
            })
        
        return {"answers": results}
    
    def _save_experiment_metadata(self, experiment: MLExperiment):
        """Save experiment metadata to file"""
        metadata_file = Path(experiment.experiment_dir) / "metadata.json"
        
        with open(metadata_file, 'w') as f:
            json.dump(experiment.dict(), f, indent=2, default=str)
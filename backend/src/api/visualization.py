"""
Visualization API endpoints for ML experiments
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import pandas as pd
import numpy as np
import json
from pathlib import Path
from typing import Dict, Any, List

from config.settings import settings
from services.ml_experiment_service import MLExperimentService

router = APIRouter()
ml_service = MLExperimentService()

# Set matplotlib backend for server environment
plt.switch_backend('Agg')

@router.get("/experiments/{experiment_id}/charts")
async def generate_experiment_charts(experiment_id: str):
    """Generate charts for ML experiment"""
    try:
        experiment = await ml_service.get_experiment(experiment_id)
        
        if not experiment.results:
            raise HTTPException(
                status_code=400,
                detail="No results available for visualization"
            )
        
        charts = []
        viz_dir = Path(settings.VISUALIZATIONS_DIR) / experiment_id
        viz_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate charts based on experiment type
        if experiment.type.value == "text_classification":
            charts.extend(await _generate_classification_charts(experiment, viz_dir))
        elif experiment.type.value == "sentiment_analysis":
            charts.extend(await _generate_sentiment_charts(experiment, viz_dir))
        elif experiment.type.value == "text_generation":
            charts.extend(await _generate_generation_charts(experiment, viz_dir))
        
        return {
            "experiment_id": experiment_id,
            "charts": charts
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/charts/{chart_id}")
async def get_chart(chart_id: str):
    """Get chart file"""
    chart_path = Path(settings.VISUALIZATIONS_DIR) / f"{chart_id}.png"
    
    if not chart_path.exists():
        raise HTTPException(status_code=404, detail="Chart not found")
    
    return FileResponse(chart_path, media_type="image/png")

@router.get("/charts/{chart_id}/interactive")
async def get_interactive_chart(chart_id: str):
    """Get interactive chart data"""
    chart_path = Path(settings.VISUALIZATIONS_DIR) / f"{chart_id}.json"
    
    if not chart_path.exists():
        raise HTTPException(status_code=404, detail="Interactive chart not found")
    
    with open(chart_path, 'r') as f:
        chart_data = json.load(f)
    
    return chart_data

@router.post("/custom-visualization")
async def create_custom_visualization(viz_config: Dict[str, Any]):
    """Create custom visualization"""
    try:
        viz_type = viz_config.get("type", "scatter")
        data = viz_config.get("data", [])
        title = viz_config.get("title", "Custom Visualization")
        
        if not data:
            raise HTTPException(status_code=400, detail="No data provided")
        
        # Convert data to DataFrame
        df = pd.DataFrame(data)
        
        # Generate visualization based on type
        if viz_type == "scatter":
            fig = px.scatter(
                df,
                x=viz_config.get("x_column"),
                y=viz_config.get("y_column"),
                title=title,
                color=viz_config.get("color_column")
            )
        elif viz_type == "line":
            fig = px.line(
                df,
                x=viz_config.get("x_column"),
                y=viz_config.get("y_column"),
                title=title
            )
        elif viz_type == "bar":
            fig = px.bar(
                df,
                x=viz_config.get("x_column"),
                y=viz_config.get("y_column"),
                title=title
            )
        elif viz_type == "histogram":
            fig = px.histogram(
                df,
                x=viz_config.get("x_column"),
                title=title
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported visualization type: {viz_type}")
        
        # Save interactive chart
        chart_id = f"custom_{hash(str(viz_config))}"
        chart_path = Path(settings.VISUALIZATIONS_DIR) / f"{chart_id}.json"
        
        with open(chart_path, 'w') as f:
            json.dump(fig.to_dict(), f, cls=PlotlyJSONEncoder)
        
        return {
            "chart_id": chart_id,
            "chart_data": fig.to_dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def _generate_classification_charts(experiment, viz_dir: Path) -> List[Dict[str, Any]]:
    """Generate charts for text classification experiments"""
    charts = []
    results = experiment.results
    
    # Metrics bar chart
    if "validation" in results:
        metrics = results["validation"]
        
        # Create metrics bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        metric_names = ["accuracy", "f1", "precision", "recall"]
        metric_values = [metrics.get(f"eval_{name}", 0) for name in metric_names]
        
        bars = ax.bar(metric_names, metric_values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        ax.set_title('Model Performance Metrics')
        ax.set_ylabel('Score')
        ax.set_ylim(0, 1)
        
        # Add value labels on bars
        for bar, value in zip(bars, metric_values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                   f'{value:.3f}', ha='center', va='bottom')
        
        chart_path = viz_dir / "metrics_bar_chart.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        charts.append({
            "id": f"{experiment.id}_metrics_bar",
            "title": "Performance Metrics",
            "type": "bar_chart",
            "path": f"/api/visualization/charts/{experiment.id}_metrics_bar"
        })
        
        # Interactive metrics chart
        fig_interactive = go.Figure(data=[
            go.Bar(x=metric_names, y=metric_values, 
                  marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        ])
        fig_interactive.update_layout(
            title='Model Performance Metrics',
            xaxis_title='Metrics',
            yaxis_title='Score'
        )
        
        interactive_path = viz_dir / f"{experiment.id}_metrics_interactive.json"
        with open(interactive_path, 'w') as f:
            json.dump(fig_interactive.to_dict(), f, cls=PlotlyJSONEncoder)
    
    return charts

async def _generate_sentiment_charts(experiment, viz_dir: Path) -> List[Dict[str, Any]]:
    """Generate charts for sentiment analysis experiments"""
    charts = []
    results = experiment.results
    
    if "predictions" in results:
        predictions = results["predictions"]
        
        # Sentiment distribution pie chart
        sentiments = [pred["sentiment"] for pred in predictions]
        sentiment_counts = pd.Series(sentiments).value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%')
        ax.set_title('Sentiment Distribution')
        
        chart_path = viz_dir / "sentiment_distribution.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        charts.append({
            "id": f"{experiment.id}_sentiment_dist",
            "title": "Sentiment Distribution",
            "type": "pie_chart",
            "path": f"/api/visualization/charts/{experiment.id}_sentiment_dist"
        })
        
        # Confidence histogram
        confidences = [pred["confidence"] for pred in predictions]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(confidences, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax.set_title('Confidence Score Distribution')
        ax.set_xlabel('Confidence Score')
        ax.set_ylabel('Frequency')
        
        chart_path = viz_dir / "confidence_histogram.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        charts.append({
            "id": f"{experiment.id}_confidence_hist",
            "title": "Confidence Distribution",
            "type": "histogram",
            "path": f"/api/visualization/charts/{experiment.id}_confidence_hist"
        })
    
    return charts

async def _generate_generation_charts(experiment, viz_dir: Path) -> List[Dict[str, Any]]:
    """Generate charts for text generation experiments"""
    charts = []
    results = experiment.results
    
    if "generations" in results:
        generations = results["generations"]
        
        # Text length distribution
        text_lengths = [len(gen["generated_text"]) for gen in generations]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(text_lengths, bins=15, alpha=0.7, color='lightgreen', edgecolor='black')
        ax.set_title('Generated Text Length Distribution')
        ax.set_xlabel('Text Length (characters)')
        ax.set_ylabel('Frequency')
        
        chart_path = viz_dir / "text_length_distribution.png"
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        charts.append({
            "id": f"{experiment.id}_text_length",
            "title": "Text Length Distribution",
            "type": "histogram",
            "path": f"/api/visualization/charts/{experiment.id}_text_length"
        })
    
    return charts
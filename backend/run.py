#!/usr/bin/env python3
"""
Quick start script for ML/AI Backend Platform
"""

import sys
import os
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    try:
        import uvicorn
        
        print("🚀 Starting ML/AI Backend Platform...")
        print("📊 Dashboard: http://localhost:8000/docs")
        print("📈 Health: http://localhost:8000/health")
        print("🧪 Test: http://localhost:8000/api/test")
        
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Install: pip install fastapi uvicorn pydantic-settings")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
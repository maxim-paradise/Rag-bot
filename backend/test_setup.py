#!/usr/bin/env python3
"""
Simple test script for backend
"""

def test_basic():
    """Test basic imports"""
    print("🧪 Testing basic setup...")
    
    try:
        import fastapi
        print("✅ FastAPI OK")
    except ImportError:
        print("❌ FastAPI missing")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn OK")
    except ImportError:
        print("❌ Uvicorn missing")
        return False
    
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        from main import app
        print("✅ Main app OK")
        return True
        
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

if __name__ == "__main__":
    if test_basic():
        print("🎉 Setup OK! Run: python run.py")
    else:
        print("❌ Setup failed. Install: pip install fastapi uvicorn pydantic-settings")
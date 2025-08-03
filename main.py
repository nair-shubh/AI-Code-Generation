#!/usr/bin/env python3
"""
Main entry point for the Advanced AI-Powered Code Transformation System
"""

import uvicorn
from src.web.interface import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 
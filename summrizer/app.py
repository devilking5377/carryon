"""
CarryOn Summary - Main Application Entry Point
Redirects to the new backend structure
"""
import sys
import os
from pathlib import Path

# Add current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the main application
from backend.main import main

if __name__ == '__main__':
    main()
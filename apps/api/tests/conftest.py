"""
Pytest configuration and fixtures
"""
import sys
from pathlib import Path

# Add parent directory to Python path
api_dir = Path(__file__).parent.parent
sys.path.insert(0, str(api_dir))

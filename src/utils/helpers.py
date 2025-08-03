"""
Utility helper functions for the Intelligent Code Automation Engine
"""

import os
import json
from typing import Dict, Any, List
from pathlib import Path


def validate_api_keys(openai_key: str = None, e2b_key: str = None) -> Dict[str, bool]:
    """Validate API keys format"""
    validation = {
        "openai": False,
        "e2b": False
    }
    
    if openai_key and openai_key.startswith("sk-"):
        validation["openai"] = True
    
    if e2b_key and len(e2b_key) > 10:
        validation["e2b"] = True
    
    return validation


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    return filename


def create_temp_directory() -> str:
    """Create a temporary directory for workspace operations"""
    import tempfile
    temp_dir = tempfile.mkdtemp(prefix="code_automation_")
    return temp_dir


def cleanup_temp_directory(path: str):
    """Clean up temporary directory"""
    import shutil
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as e:
        print(f"Warning: Could not cleanup {path}: {e}")


def format_repository_url(url: str) -> str:
    """Format repository URL to ensure it's a valid GitHub URL"""
    if not url.startswith(('http://', 'https://')):
        url = f"https://github.com/{url}"
    
    # Ensure it's a GitHub URL
    if 'github.com' not in url:
        raise ValueError("Repository URL must be a GitHub URL")
    
    return url


def extract_repo_info_from_url(url: str) -> Dict[str, str]:
    """Extract owner and repo name from GitHub URL"""
    # Handle different GitHub URL formats
    if url.endswith('.git'):
        url = url[:-4]
    
    parts = url.split('/')
    if 'github.com' in parts:
        github_index = parts.index('github.com')
        if len(parts) >= github_index + 3:
            owner = parts[github_index + 1]
            repo = parts[github_index + 2]
            return {"owner": owner, "repo": repo}
    
    raise ValueError("Could not extract repository information from URL")


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load JSON file safely"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise ValueError(f"Could not load JSON file {file_path}: {e}")


def save_json_file(file_path: str, data: Dict[str, Any]):
    """Save data to JSON file safely"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"Could not save JSON file {file_path}: {e}") 
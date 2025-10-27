"""
Utility functions for Twitter sentiment analysis project.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger(__name__)


def ensure_directory(path: str):
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def load_json(file_path: str) -> Dict:
    """
    Load JSON data from file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Loaded JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}")
        return {}


def save_json(data: Dict, file_path: str):
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        file_path: Path to save file
    """
    ensure_directory(Path(file_path).parent)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Data saved to {file_path}")


def clean_text(text: str) -> str:
    """
    Clean tweet text.
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    import re
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()


def format_percentage(value: float, total: float) -> str:
    """
    Format a value as a percentage of total.
    
    Args:
        value: Numerator
        total: Denominator
        
    Returns:
        Formatted percentage string
    """
    if total == 0:
        return "0.0%"
    percentage = (value / total) * 100
    return f"{percentage:.1f}%"


def print_progress_bar(iteration: int, total: int, prefix: str = '', 
                       suffix: str = '', length: int = 50):
    """
    Print a progress bar.
    
    Args:
        iteration: Current iteration
        total: Total iterations
        prefix: Prefix string
        suffix: Suffix string
        length: Bar length
    """
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='')
    if iteration == total:
        print()

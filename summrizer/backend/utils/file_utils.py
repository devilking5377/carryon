"""
File utilities for CarryOn Summary
"""
import re
from typing import List, Set
from pathlib import Path


def extract_file_paths(text: str) -> List[str]:
    """
    Extract file paths from text content
    
    Args:
        text: Input text to scan for file paths
        
    Returns:
        List of unique file paths found in the text
    """
    # Pattern to match common file extensions
    file_pattern = r'\b[\w\-/\\]+\.(?:py|ts|tsx|js|json|md|txt|yaml|yml|xml|html|css|java|cpp|c|h|php|rb|go|rs|swift|kt|scala|sh|bat|ps1|sql|r|m|pl|lua|dart|vue|jsx|scss|less|sass|styl|coffee|elm|clj|hs|ml|fs|ex|exs|erl|nim|cr|zig|v|d|pas|ada|cob|f90|f95|asm|s|S)\b'
    
    matches = re.findall(file_pattern, text, re.IGNORECASE)
    
    # Remove duplicates and sort
    unique_files = sorted(set(matches))
    
    # Filter out common false positives
    filtered_files = []
    for file_path in unique_files:
        # Skip very short paths or those that look like URLs
        if len(file_path) > 3 and not file_path.startswith(('http', 'www')):
            filtered_files.append(file_path)
    
    return filtered_files


def validate_file_path(file_path: str) -> bool:
    """
    Validate if a string looks like a valid file path
    
    Args:
        file_path: Path string to validate
        
    Returns:
        True if the path looks valid, False otherwise
    """
    try:
        path = Path(file_path)
        
        # Check if it has a valid extension
        if not path.suffix:
            return False
        
        # Check if the name is reasonable
        if len(path.name) < 3:
            return False
        
        # Check for invalid characters (basic check)
        invalid_chars = ['<', '>', '|', '"', '?', '*']
        if any(char in file_path for char in invalid_chars):
            return False
        
        return True
    
    except Exception:
        return False


def get_file_type(file_path: str) -> str:
    """
    Get the file type category based on extension
    
    Args:
        file_path: Path to analyze
        
    Returns:
        File type category string
    """
    path = Path(file_path)
    extension = path.suffix.lower()
    
    # Define file type categories
    categories = {
        'python': ['.py'],
        'javascript': ['.js', '.jsx', '.ts', '.tsx'],
        'web': ['.html', '.css', '.scss', '.less', '.sass'],
        'data': ['.json', '.yaml', '.yml', '.xml', '.csv'],
        'documentation': ['.md', '.txt', '.rst'],
        'config': ['.ini', '.conf', '.cfg', '.toml'],
        'database': ['.sql', '.db', '.sqlite'],
        'java': ['.java', '.class', '.jar'],
        'c_cpp': ['.c', '.cpp', '.h', '.hpp'],
        'shell': ['.sh', '.bash', '.zsh', '.fish', '.bat', '.ps1'],
        'other': []
    }
    
    for category, extensions in categories.items():
        if extension in extensions:
            return category
    
    return 'other'


def format_file_list(file_paths: List[str]) -> str:
    """
    Format a list of file paths for display
    
    Args:
        file_paths: List of file paths
        
    Returns:
        Formatted string representation
    """
    if not file_paths:
        return "No files detected"
    
    # Group by file type
    by_type = {}
    for file_path in file_paths:
        file_type = get_file_type(file_path)
        if file_type not in by_type:
            by_type[file_type] = []
        by_type[file_type].append(file_path)
    
    # Format output
    result = []
    for file_type, files in sorted(by_type.items()):
        if file_type != 'other':
            result.append(f"{file_type.title()} files:")
            for file_path in sorted(files):
                result.append(f"  - {file_path}")
        else:
            result.append("Other files:")
            for file_path in sorted(files):
                result.append(f"  - {file_path}")
    
    return "\n".join(result)


def create_continuation_steps(file_paths: List[str]) -> List[str]:
    """
    Create continuation steps based on detected file paths
    
    Args:
        file_paths: List of detected file paths
        
    Returns:
        List of continuation step strings
    """
    if not file_paths:
        return []
    
    steps = []
    
    # Group files by type for better organization
    by_type = {}
    for file_path in file_paths:
        file_type = get_file_type(file_path)
        if file_type not in by_type:
            by_type[file_type] = []
        by_type[file_type].append(file_path)
    
    # Create specific steps based on file types
    for file_type, files in by_type.items():
        if file_type == 'python':
            steps.append(f"Review and update Python files: {', '.join(files)}")
        elif file_type == 'javascript':
            steps.append(f"Check JavaScript/TypeScript files: {', '.join(files)}")
        elif file_type == 'web':
            steps.append(f"Update web files: {', '.join(files)}")
        elif file_type == 'documentation':
            steps.append(f"Update documentation: {', '.join(files)}")
        elif file_type == 'config':
            steps.append(f"Review configuration files: {', '.join(files)}")
        else:
            steps.append(f"Review {file_type} files: {', '.join(files)}")
    
    # Add general steps
    steps.extend([
        "Paste this summary into your next agent to provide context",
        "If the next agent supports file uploads, attach the mentioned files",
        "Reference this summary when making changes to maintain consistency"
    ])
    
    return steps
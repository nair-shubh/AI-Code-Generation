"""
Data models for the Intelligent Code Automation Engine
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from enum import Enum

class ExecutionStatus(str, Enum):
    """Execution status enumeration"""
    PENDING = "pending"
    INITIALIZING = "initializing"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    EXECUTING = "executing"
    DEPLOYING = "deploying"
    COMPLETED = "completed"
    FAILED = "failed"

class ModificationType(str, Enum):
    """Code modification types"""
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"

@dataclass
class CodeModification:
    """Represents a code modification"""
    file_path: str
    operation: str  # 'create', 'modify', 'delete'
    content: Optional[str] = None
    description: str = ""

@dataclass
class RepositoryInfo:
    """Repository information"""
    owner: str
    name: str
    url: str
    description: Optional[str] = None
    language: Optional[str] = None
    stars: int = 0
    forks: int = 0

@dataclass
class CodeAnalysis:
    """Code analysis results"""
    total_files: int
    languages: List[str]
    main_files: List[str]
    structure: Dict[str, Any]
    dependencies: List[str]
    estimated_complexity: str

@dataclass
class ExecutionResult:
    """Execution result"""
    status: ExecutionStatus
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@dataclass
class SessionData:
    """Session data for tracking user requests"""
    session_id: str
    github_token: str
    openai_token: str
    repo_url: str
    prompt: str
    branch_name: str
    commit_message: str
    status: ExecutionStatus = ExecutionStatus.PENDING
    progress: Dict[str, Any] = None 
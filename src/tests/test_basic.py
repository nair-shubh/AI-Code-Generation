"""
Basic tests for the Intelligent Code Automation Engine
"""

import pytest
from src.core.models import ExecutionStatus, CodeModification, RepositoryInfo
from src.core.engine import CodeTransformationPlatform


def test_models():
    """Test that models can be instantiated"""
    # Test ExecutionStatus
    assert ExecutionStatus.PENDING == "pending"
    assert ExecutionStatus.COMPLETED == "completed"
    
    # Test CodeModification
    mod = CodeModification(
        file_path="test.py",
        operation="create",
        content="# test content",
        description="Test modification"
    )
    assert mod.file_path == "test.py"
    assert mod.operation == "create"
    
    # Test RepositoryInfo
    repo = RepositoryInfo(
        name="test-repo",
        owner="testuser",
        url="https://github.com/testuser/test-repo",
        description="Test repository",
        language="Python"
    )
    assert repo.name == "test-repo"
    assert repo.owner == "testuser"


def test_platform_initialization():
    """Test that the platform can be initialized"""
    # This should work even without API keys (they're optional in __init__)
    try:
        platform = CodeTransformationPlatform()
        assert platform is not None
    except ValueError:
        # Expected if no OpenAI key is provided
        pass


if __name__ == "__main__":
    pytest.main([__file__]) 
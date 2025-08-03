#!/usr/bin/env python3
"""
Advanced AI-Powered Code Transformation System
A sophisticated platform for intelligent code modification and deployment
"""

import os
import json
import asyncio
import tempfile
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Optional, AsyncGenerator
from pathlib import Path
import aiohttp

# Import local models
from .models import (
    ExecutionStatus, 
    ModificationType, 
    CodeModification, 
    RepositoryInfo, 
    CodeAnalysis, 
    ExecutionResult
)

# Conditional imports for optional dependencies
try:
    from e2b_code_interpreter import Sandbox
    E2B_AVAILABLE = True
except ImportError:
    E2B_AVAILABLE = False
    print("⚠️ E2B not available. Install with: pip install e2b-code-interpreter")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI not available. Install with: pip install openai")

try:
    from github import Github
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False
    print("⚠️ PyGithub not available. Install with: pip install PyGithub")


class CodeTransformationPlatform:
    """
    Advanced AI-powered code transformation and deployment platform
    """
    
    def __init__(self, openai_api_key: Optional[str] = None, e2b_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.e2b_api_key = e2b_api_key or os.getenv("E2B_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        self.openai_client = OpenAI(api_key=self.openai_api_key) if OPENAI_AVAILABLE else None
        self.github_client = None
        self.e2b_session = None
        self.workspace_path = None
        
    def setup_github_connection(self, github_token: str):
        """Setup GitHub connection with user token"""
        if not GITHUB_AVAILABLE:
            raise RuntimeError("PyGithub is not installed")
        
        self.github_client = Github(github_token)
        print("✅ GitHub connection established")
    
    async def create_execution_environment(self) -> str:
        """Create execution environment for code processing"""
        if not E2B_AVAILABLE:
            # Fallback to local environment
            self.workspace_path = tempfile.mkdtemp(prefix="code_transform_")
            print(f"📁 Local environment created: {self.workspace_path}")
            return self.workspace_path
        
        try:
            if not self.e2b_api_key:
                raise ValueError("E2B API key required for cloud execution")
            
            # Create E2B sandbox using context manager pattern
            self.e2b_session = Sandbox(api_key=self.e2b_api_key)
            await self.e2b_session.__aenter__()
            print("☁️ E2B cloud environment initialized")
            return "e2b_environment"
            
        except Exception as e:
            print(f"⚠️ E2B initialization failed: {e}")
            # Fallback to local environment
            self.workspace_path = tempfile.mkdtemp(prefix="code_transform_")
            print(f"📁 Local environment created: {self.workspace_path}")
            return self.workspace_path
    
    async def retrieve_user_repositories(self) -> List[RepositoryInfo]:
        """Retrieve user's GitHub repositories"""
        if not self.github_client:
            raise RuntimeError("GitHub connection not established")
        
        try:
            user = self.github_client.get_user()
            repos = []
            
            for repo in user.get_repos():
                if not repo.fork:  # Only non-forked repositories
                    repos.append(RepositoryInfo(
                        name=repo.name,
                        owner=repo.owner.login,
                        url=repo.html_url,
                        description=repo.description,
                        language=repo.language
                    ))
            
            return repos
            
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve repositories: {e}")
    
    async def download_repository(self, repo_url: str) -> str:
        """Download repository to execution environment"""
        try:
            if self.e2b_session:
                # Use E2B for downloading
                result = self.e2b_session.run_code(f"git clone {repo_url}")
                repo_name = repo_url.split('/')[-1].replace('.git', '')
                return f"/home/user/{repo_name}"
            else:
                # Local downloading
                repo_name = repo_url.split('/')[-1].replace('.git', '')
                local_path = os.path.join(self.workspace_path, repo_name)
                
                subprocess.run([
                    "git", "clone", repo_url, local_path
                ], check=True, capture_output=True)
                
                return local_path
                
        except Exception as e:
            raise RuntimeError(f"Failed to download repository: {e}")
    
    async def examine_codebase(self, repo_path: str) -> Dict[str, Any]:
        """Examine codebase structure and content"""
        try:
            if self.e2b_session:
                # Examine in E2B
                result = self.e2b_session.run_code(f"find {repo_path} -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.java' -o -name '*.cpp' -o -name '*.c' -o -name '*.go' -o -name '*.rs' | head -20")
                files = result.text.strip().split('\n') if result.text else []
            else:
                # Local examination
                files = []
                for root, dirs, filenames in os.walk(repo_path):
                    for filename in filenames:
                        if filename.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs')):
                            files.append(os.path.join(root, filename))
            
            # Examine file contents
            analysis = {
                "total_files": len(files),
                "languages": self._identify_languages(files),
                "main_files": files[:10],
                "structure": f"Repository with {len(files)} code files"
            }
            
            return analysis
            
        except Exception as e:
            raise RuntimeError(f"Failed to examine codebase: {e}")
    
    async def create_code_transformations(self, prompt: str, analysis: Dict[str, Any]) -> List[CodeModification]:
        """Create code transformations using AI"""
        if not self.openai_client:
            raise RuntimeError("OpenAI client not available")
        
        try:
            context = f"""
Codebase Examination:
- Files: {analysis['total_files']}
- Languages: {', '.join(analysis['languages'])}
- Main files: {', '.join(analysis['main_files'][:5])}

User Request: {prompt}

Create specific code transformations in JSON format:
{{
    "transformations": [
        {{
            "file_path": "path/to/file",
            "operation": "create|modify|delete",
            "content": "file content (for create/modify)",
            "description": "explanation"
        }}
    ]
}}
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software engineer. Create precise, working code transformations based on user requests. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            
            # Extract JSON from response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]
            
            data = json.loads(json_str)
            
            transformations = []
            for mod in data.get("transformations", []):
                transformations.append(CodeModification(
                    file_path=mod["file_path"],
                    operation=mod["operation"],
                    content=mod.get("content", ""),
                    description=mod.get("description", "")
                ))
            
            return transformations
            
        except Exception as e:
            raise RuntimeError(f"Failed to create code transformations: {e}")
    
    async def implement_transformations(self, repo_path: str, transformations: List[CodeModification]) -> List[str]:
        """Implement code transformations in repository"""
        try:
            implemented_files = []
            
            for transformation in transformations:
                if self.e2b_session:
                    # Implement in E2B
                    if transformation.operation == "create":
                        # Create file using echo command
                        self.e2b_session.run_code(f"echo '{transformation.content or ''}' > {repo_path}/{transformation.file_path}")
                    elif transformation.operation == "modify":
                        # Modify file using echo command
                        self.e2b_session.run_code(f"echo '{transformation.content or ''}' > {repo_path}/{transformation.file_path}")
                    elif transformation.operation == "delete":
                        # Delete file using rm command
                        self.e2b_session.run_code(f"rm -f {repo_path}/{transformation.file_path}")
                else:
                    # Local implementation
                    full_path = os.path.join(repo_path, transformation.file_path)
                    
                    if transformation.operation == "create":
                        os.makedirs(os.path.dirname(full_path), exist_ok=True)
                        with open(full_path, 'w') as f:
                            f.write(transformation.content or "")
                    elif transformation.operation == "modify":
                        with open(full_path, 'w') as f:
                            f.write(transformation.content or "")
                    elif transformation.operation == "delete":
                        if os.path.exists(full_path):
                            os.remove(full_path)
                
                implemented_files.append(transformation.file_path)
                print(f"✅ Implemented: {transformation.file_path}")
            
            return implemented_files
            
        except Exception as e:
            raise RuntimeError(f"Failed to implement transformations: {e}")
    
    async def run_code_validation(self, repo_path: str) -> Dict[str, Any]:
        """Run code validation in the execution environment"""
        try:
            if self.e2b_session:
                # Run validation in E2B
                result = self.e2b_session.run_code(f"cd {repo_path} && python -m pytest --tb=short || echo 'No pytest found'")
                validation_output = result.text
            else:
                # Local validation execution
                try:
                    result = subprocess.run(
                        ["python", "-m", "pytest", "--tb=short"],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    validation_output = result.stdout
                except subprocess.TimeoutExpired:
                    validation_output = "Validation timed out"
                except FileNotFoundError:
                    validation_output = "No pytest found"
            
            return {
                "validation_output": validation_output,
                "status": "completed"
            }
            
        except Exception as e:
            return {
                "validation_output": f"Validation execution failed: {e}",
                "status": "failed"
            }
    
    async def commit_and_publish(self, repo_path: str, branch_name: str, commit_message: str, github_token: str) -> Dict[str, Any]:
        """Commit changes and publish to GitHub"""
        try:
            if self.e2b_session:
                # Publish from E2B
                commands = [
                    f"cd {repo_path}",
                    "git add .",
                    f"git commit -m '{commit_message}'",
                    f"git checkout -b {branch_name}",
                    f"git push -u origin {branch_name}"
                ]
                
                for cmd in commands:
                    result = self.e2b_session.run_code(cmd)
                    if result.error:
                        raise RuntimeError(f"Git command failed: {cmd}")
            else:
                # Local publishing
                subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
                subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
                subprocess.run(["git", "checkout", "-b", branch_name], cwd=repo_path, check=True)
                subprocess.run(["git", "push", "-u", "origin", branch_name], cwd=repo_path, check=True)
            
            return {
                "branch": branch_name,
                "commit_message": commit_message,
                "status": "success"
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to commit and publish: {e}")
    
    async def cleanup_resources(self):
        """Clean up resources"""
        try:
            if self.e2b_session:
                await self.e2b_session.__aexit__(None, None, None)
                print("☁️ E2B session closed")
            
            if self.workspace_path and os.path.exists(self.workspace_path):
                import shutil
                shutil.rmtree(self.workspace_path)
                print("📁 Local environment cleaned up")
                
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
    
    def _identify_languages(self, files: List[str]) -> List[str]:
        """Identify programming languages from file extensions"""
        extensions = set()
        for file in files:
            ext = Path(file).suffix.lower()
            if ext:
                extensions.add(ext)
        
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust'
        }
        
        return [language_map.get(ext, ext[1:].upper()) for ext in extensions if ext in language_map]


async def main():
    """Main execution function"""
    print("🚀 Advanced AI-Powered Code Transformation System")
    print("=" * 50)
    
    # Initialize platform
    platform = CodeTransformationPlatform()
    
    try:
        # Setup GitHub (user would provide token)
        github_token = input("Enter your GitHub token: ").strip()
        platform.setup_github_connection(github_token)
        
        # Create execution environment
        await platform.create_execution_environment()
        
        # Retrieve repositories
        repos = await platform.retrieve_user_repositories()
        print(f"📋 Found {len(repos)} repositories")
        
        # Select repository
        for i, repo in enumerate(repos[:5]):
            print(f"{i+1}. {repo.owner}/{repo.name} - {repo.language or 'Unknown'}")
        
        repo_choice = int(input("Select repository (1-5): ")) - 1
        selected_repo = repos[repo_choice]
        
        # Get user prompt
        prompt = input("Describe the changes you want to make: ").strip()
        
        # Download repository
        print(f"📥 Downloading {selected_repo.name}...")
        repo_path = await platform.download_repository(selected_repo.url)
        
        # Examine codebase
        print("🔍 Examining codebase...")
        analysis = await platform.examine_codebase(repo_path)
        print(f"📊 Found {analysis['total_files']} files in {', '.join(analysis['languages'])}")
        
        # Create transformations
        print("🤖 Creating code transformations...")
        transformations = await platform.create_code_transformations(prompt, analysis)
        print(f"✏️ Created {len(transformations)} transformations")
        
        # Implement transformations
        print("🔧 Implementing transformations...")
        implemented_files = await platform.implement_transformations(repo_path, transformations)
        
        # Run validation
        print("🧪 Running validation...")
        validation_results = await platform.run_code_validation(repo_path)
        print(f"✅ Validation completed: {validation_results['status']}")
        
        # Commit and publish
        branch_name = f"ai-transformed-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        commit_message = f"AI-transformed changes: {prompt[:50]}..."
        
        print(f"🚀 Publishing to branch: {branch_name}")
        publish_result = await platform.commit_and_publish(repo_path, branch_name, commit_message, github_token)
        
        print("🎉 Publication completed successfully!")
        print(f"📋 Branch: {publish_result['branch']}")
        print(f"💬 Commit: {publish_result['commit_message']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        await platform.cleanup_resources()


if __name__ == "__main__":
    asyncio.run(main()) 
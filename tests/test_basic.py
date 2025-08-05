"""
Basic tests for AI Video Analysis Platform.
"""

import pytest
import json
import tempfile
import os
from pathlib import Path


class TestProjectStructure:
    """Test basic project structure and functionality."""
    
    def test_project_files_exist(self):
        """Test that essential project files exist."""
        required_files = [
            "README.md",
            "requirements.txt",
            "setup.py",
            "LICENSE",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            ".gitignore"
        ]
        
        for file_path in required_files:
            assert Path(file_path).exists(), f"Required file {file_path} not found"
    
    def test_youtube_analyze_directory(self):
        """Test that youtube_analyze directory exists with required files."""
        youtube_dir = Path("youtube_analyze")
        assert youtube_dir.exists(), "youtube_analyze directory not found"
        
        required_files = [
            "enhanced_youtube_analyzer.py",
            "youtube_analyzer_cli.py",
            "ENHANCED_ANALYZER_README.md"
        ]
        
        for file_path in required_files:
            assert (youtube_dir / file_path).exists(), f"Required file {file_path} not found in youtube_analyze"
    
    def test_custom_agent_directory(self):
        """Test that custom_agent directory exists with required files."""
        agent_dir = Path("custom_agent")
        assert agent_dir.exists(), "custom_agent directory not found"
        
        required_files = [
            "continuous_agent.py",
            "README.md",
            "requirements.txt"
        ]
        
        for file_path in required_files:
            assert (agent_dir / file_path).exists(), f"Required file {file_path} not found in custom_agent"


class TestConfiguration:
    """Test configuration and setup."""
    
    def test_requirements_format(self):
        """Test that requirements.txt has valid format."""
        with open("requirements.txt", "r") as f:
            requirements = f.readlines()
        
        for line in requirements:
            line = line.strip()
            if line and not line.startswith("#"):
                # Basic validation - should contain package name
                assert ">=" in line or "==" in line or not any(char in line for char in [">", "<", "="]), \
                    f"Invalid requirement format: {line}"
    
    def test_setup_py_valid(self):
        """Test that setup.py is valid Python."""
        with open("setup.py", "r") as f:
            setup_content = f.read()
        
        # Basic syntax check
        try:
            compile(setup_content, "setup.py", "exec")
        except SyntaxError as e:
            pytest.fail(f"setup.py has syntax error: {e}")


class TestDocumentation:
    """Test documentation quality."""
    
    def test_readme_has_keywords(self):
        """Test that README contains important keywords for discoverability."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read().lower()
        
        important_keywords = [
            "ai",
            "video analysis",
            "youtube",
            "autonomous",
            "ollama",
            "python",
            "open source"
        ]
        
        missing_keywords = []
        for keyword in important_keywords:
            if keyword not in content:
                missing_keywords.append(keyword)
        
        assert not missing_keywords, f"README missing important keywords: {missing_keywords}"
    
    def test_readme_has_installation_instructions(self):
        """Test that README has installation instructions."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        assert "pip install" in content or "clone" in content, "README should contain installation instructions"
    
    def test_readme_has_usage_examples(self):
        """Test that README has usage examples."""
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        assert "```" in content, "README should contain code examples"


class TestJsonProcessing:
    """Test JSON processing capabilities."""
    
    def test_json_validation(self):
        """Test that JSON files can be processed."""
        test_data = {
            "videos": [
                {
                    "title": "Test Video",
                    "duration": 180,
                    "ai_summary": "This is a test video summary"
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            temp_file = f.name
        
        try:
            with open(temp_file, 'r') as f:
                loaded_data = json.load(f)
            
            assert "videos" in loaded_data
            assert len(loaded_data["videos"]) == 1
            assert loaded_data["videos"][0]["title"] == "Test Video"
        
        finally:
            os.unlink(temp_file)


class TestProjectMetadata:
    """Test project metadata and discoverability."""
    
    def test_github_actions_exist(self):
        """Test that GitHub Actions workflow exists."""
        workflow_path = Path(".github/workflows/ci.yml")
        assert workflow_path.exists(), "GitHub Actions CI workflow not found"
    
    def test_license_is_mit(self):
        """Test that license is MIT."""
        with open("LICENSE", "r") as f:
            license_content = f.read()
        
        assert "MIT License" in license_content, "License should be MIT"
    
    def test_changelog_format(self):
        """Test that changelog follows proper format."""
        with open("CHANGELOG.md", "r") as f:
            changelog_content = f.read()
        
        assert "## [Unreleased]" in changelog_content, "Changelog should have Unreleased section"
        assert "## [1.0.0]" in changelog_content, "Changelog should have version 1.0.0"


if __name__ == "__main__":
    pytest.main([__file__]) 
# Contributing to AI Video Analysis Platform

Thank you for your interest in contributing to the AI Video Analysis Platform! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- 🐛 **Bug Reports**: Help us identify and fix issues
- 💡 **Feature Requests**: Suggest new features or improvements
- 📝 **Documentation**: Improve or expand documentation
- 🔧 **Code Contributions**: Submit code improvements or new features
- 🧪 **Testing**: Help test the platform and report issues

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test your changes**: Ensure everything works as expected
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

## 🛠️ Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Ollama (for AI functionality)

### Local Development

```bash
# Clone your fork
git clone https://github.com/yourusername/ai-video-analysis-platform.git
cd ai-video-analysis-platform

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .  # Install in development mode

# Install development dependencies
pip install -r requirements.txt[dev]
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run linting
flake8 .
black --check .
```

## 📋 Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose

### Example Code Style

```python
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


def analyze_video_content(video_url: str, model: str = "gemma3:4b") -> Dict[str, any]:
    """
    Analyze video content using AI models.
    
    Args:
        video_url: URL of the video to analyze
        model: Ollama model to use for analysis
        
    Returns:
        Dictionary containing analysis results
        
    Raises:
        ValueError: If video_url is invalid
    """
    if not video_url:
        raise ValueError("Video URL cannot be empty")
    
    # Implementation here
    return {"analysis": "results"}
```

### Commit Message Guidelines

Use conventional commit messages:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

Example: `feat: add support for batch video processing`

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

### Example Test

```python
import pytest
from unittest.mock import Mock, patch
from youtube_analyze.enhanced_youtube_analyzer import EnhancedYouTubeAnalyzer


class TestEnhancedYouTubeAnalyzer:
    """Test cases for EnhancedYouTubeAnalyzer."""
    
    def test_analyze_video_success(self):
        """Test successful video analysis."""
        analyzer = EnhancedYouTubeAnalyzer()
        
        with patch('yt_dlp.extract_info') as mock_extract:
            mock_extract.return_value = {
                'title': 'Test Video',
                'duration': 180,
                'view_count': 1000,
                'like_count': 100
            }
            
            result = analyzer.analyze_video('https://youtube.com/watch?v=test')
            
            assert result['title'] == 'Test Video'
            assert result['duration'] == 180
    
    def test_analyze_video_invalid_url(self):
        """Test video analysis with invalid URL."""
        analyzer = EnhancedYouTubeAnalyzer()
        
        with pytest.raises(ValueError, match="Invalid URL"):
            analyzer.analyze_video('invalid-url')
```

## 📝 Documentation Guidelines

### Code Documentation

- Write clear docstrings for all public functions
- Include type hints
- Provide usage examples
- Document exceptions and edge cases

### README Updates

- Update README.md when adding new features
- Include usage examples
- Update installation instructions if needed
- Add screenshots or GIFs for UI changes

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Environment details** (OS, Python version, etc.)
5. **Error messages** or logs
6. **Screenshots** if applicable

## 💡 Feature Requests

When suggesting features:

1. **Clear description** of the feature
2. **Use case** and benefits
3. **Implementation ideas** (if any)
4. **Priority level** (low/medium/high)

## 🔄 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new functionality
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** if applicable
5. **Request review** from maintainers

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Other (please describe)

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🏷️ Issue Labels

We use the following labels:

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## 📞 Getting Help

If you need help:

1. Check existing issues and discussions
2. Read the documentation
3. Ask questions in issues or discussions
4. Join our community (if applicable)

## 🎉 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to the AI Video Analysis Platform! 🚀 
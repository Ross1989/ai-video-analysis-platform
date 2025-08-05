from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-video-analysis-platform",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered video analysis platform with autonomous agents for content intelligence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-video-analysis-platform",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-video-analyzer=youtube_analyze.youtube_analyzer_cli:main",
            "ai-video-agent=custom_agent.continuous_agent:main",
        ],
    },
    keywords=[
        "ai",
        "video-analysis",
        "youtube",
        "autonomous-agents",
        "content-intelligence",
        "machine-learning",
        "ollama",
        "open-source",
        "python",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ai-video-analysis-platform/issues",
        "Source": "https://github.com/yourusername/ai-video-analysis-platform",
        "Documentation": "https://github.com/yourusername/ai-video-analysis-platform#readme",
    },
) 
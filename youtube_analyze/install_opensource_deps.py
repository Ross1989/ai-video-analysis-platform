#!/usr/bin/env python3
"""
Open Source YouTube Analysis Dependencies Installer
Automatically installs all required tools for YouTube video analysis
"""

import subprocess
import sys
import platform
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            return True
        else:
            print(f"❌ {description} - Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def check_python_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_python_packages():
    """Install required Python packages"""
    packages = [
        ("yt-dlp", "Video download and metadata extraction"),
        ("openai-whisper", "Speech-to-text transcription"),
        ("openai", "OpenAI client for Ollama"),
        ("requests", "HTTP requests"),
        ("torch", "PyTorch for Whisper")
    ]
    
    print("\n🐍 Installing Python packages...")
    print("=" * 50)
    
    for package, description in packages:
        if check_python_package(package.replace("-", "_")):
            print(f"✅ {package} already installed")
        else:
            print(f"📦 Installing {package} ({description})...")
            success = run_command(f"pip install {package}", f"Installing {package}")
            if not success:
                print(f"⚠️ Failed to install {package}, you may need to install it manually")

def install_system_dependencies():
    """Install system dependencies based on OS"""
    system = platform.system().lower()
    
    print(f"\n🖥️ Installing system dependencies for {system}...")
    print("=" * 50)
    
    if system == "darwin":  # macOS
        print("🍎 macOS detected")
        
        # Check if Homebrew is installed
        if not run_command("which brew", "Checking Homebrew"):
            print("📦 Installing Homebrew...")
            run_command('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', "Installing Homebrew")
        
        # Install FFmpeg
        run_command("brew install ffmpeg", "Installing FFmpeg")
        
        # Install Ollama
        run_command("brew install ollama", "Installing Ollama")
        
    elif system == "linux":
        print("🐧 Linux detected")
        
        # Detect distribution
        try:
            with open("/etc/os-release", "r") as f:
                content = f.read().lower()
                if "ubuntu" in content or "debian" in content:
                    run_command("sudo apt update", "Updating package list")
                    run_command("sudo apt install -y ffmpeg", "Installing FFmpeg")
                elif "fedora" in content or "rhel" in content or "centos" in content:
                    run_command("sudo dnf install -y ffmpeg", "Installing FFmpeg")
                else:
                    print("⚠️ Unsupported Linux distribution. Please install FFmpeg manually.")
        except:
            print("⚠️ Could not detect Linux distribution. Please install FFmpeg manually.")
        
        # Install Ollama
        run_command("curl -fsSL https://ollama.ai/install.sh | sh", "Installing Ollama")
        
    elif system == "windows":
        print("🪟 Windows detected")
        
        # Check if Chocolatey is installed
        if not run_command("choco --version", "Checking Chocolatey"):
            print("📦 Installing Chocolatey...")
            run_command('powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))"', "Installing Chocolatey")
        
        # Install FFmpeg
        run_command("choco install ffmpeg -y", "Installing FFmpeg")
        
        # Install Ollama (Windows instructions)
        print("📦 Please install Ollama manually from https://ollama.ai/download")
        
    else:
        print(f"⚠️ Unsupported operating system: {system}")
        print("Please install FFmpeg and Ollama manually")

def check_ollama_setup():
    """Check if Ollama is properly set up"""
    print("\n🤖 Checking Ollama setup...")
    print("=" * 50)
    
    # Check if Ollama is running
    if run_command("ollama list", "Checking Ollama installation"):
        print("✅ Ollama is installed and running!")
        
        # Check available models
        result = subprocess.run("ollama list", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            if "gemma3:4b" in result.stdout:
                print("✅ gemma3:4b model is available")
            else:
                print("📦 Installing gemma3:4b model...")
                run_command("ollama pull gemma3:4b", "Installing gemma3:4b")
        else:
            print("⚠️ Could not check Ollama models")
    else:
        print("❌ Ollama is not running. Please start it with: ollama serve")

def create_test_script():
    """Create a simple test script"""
    test_script = '''#!/usr/bin/env python3
"""
Quick test for open-source YouTube analysis setup
"""

def test_setup():
    print("🧪 Testing open-source YouTube analysis setup...")
    
    # Test imports
    try:
        import yt_dlp
        print("✅ yt-dlp imported successfully")
    except ImportError:
        print("❌ yt-dlp not available")
        return False
    
    try:
        import whisper
        print("✅ whisper imported successfully")
    except ImportError:
        print("❌ whisper not available")
        return False
    
    try:
        from openai import OpenAI
        print("✅ openai imported successfully")
    except ImportError:
        print("❌ openai not available")
        return False
    
    # Test FFmpeg
    import subprocess
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg is available")
        else:
            print("❌ FFmpeg not working")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found")
        return False
    
    # Test Ollama
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is working")
        else:
            print("❌ Ollama not responding")
            return False
    except FileNotFoundError:
        print("❌ Ollama not found")
        return False
    
    print("\\n🎉 All dependencies are working correctly!")
    print("You can now use the open-source YouTube analyzer!")
    return True

if __name__ == "__main__":
    test_setup()
'''
    
    with open("test_setup.py", "w") as f:
        f.write(test_script)
    
    print("✅ Created test_setup.py - run it to verify your installation")

def main():
    """Main installation function"""
    print("🔓 Open Source YouTube Analysis Setup")
    print("=" * 50)
    print("This script will install all dependencies needed for")
    print("open-source YouTube video analysis with Ollama.")
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install Python packages
    install_python_packages()
    
    # Install system dependencies
    install_system_dependencies()
    
    # Check Ollama setup
    check_ollama_setup()
    
    # Create test script
    create_test_script()
    
    print("\n🎉 Installation complete!")
    print("=" * 50)
    print("Next steps:")
    print("1. Run: python test_setup.py")
    print("2. If all tests pass, you're ready to analyze YouTube videos!")
    print("3. Use: python opensource_youtube_analyzer.py")
    print()
    print("🔓 All tools are free and open-source!")
    print("💰 No API costs or usage limits!")

if __name__ == "__main__":
    main() 
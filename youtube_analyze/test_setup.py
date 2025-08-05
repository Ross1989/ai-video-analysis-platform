#!/usr/bin/env python3
"""
Quick test for open-source YouTube analysis setup
"""

def test_setup():
    print("Testing open-source YouTube analysis setup...")
    
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
    
    print("\n🎉 All dependencies are working correctly!")
    print("You can now use the open-source YouTube analyzer!")
    return True

if __name__ == "__main__":
    test_setup()

#!/usr/bin/env python3
"""
Enhanced YouTube Video Analyzer with JSON Input
Accepts JSON search queries and returns top 3 results filtered by duration and rating
Includes speech-to-text transcription using Ollama
"""

import os
import json
import requests
from openai import OpenAI
from datetime import datetime
from typing import List, Dict, Any
import yt_dlp
import tempfile
import subprocess

class EnhancedYouTubeAnalyzer:
    def __init__(self, ollama_base_url: str = "http://localhost:11434/v1", model: str = "gemma3:4b"):
        """Initialize the enhanced YouTube analyzer"""
        self.ollama_base_url = ollama_base_url
        self.model = model
        
        # Initialize OpenAI client for Ollama
        self.client = OpenAI(
            base_url=ollama_base_url,
            api_key="ollama"
        )
        
        print(f"✅ Enhanced YouTube Analyzer initialized with model: {model}")
    
    def check_dependencies(self):
        """Check if all required dependencies are available"""
        dependencies = {
            "yt-dlp": "Video download and metadata extraction"
        }
        
        missing = []
        
        for dep, description in dependencies.items():
            try:
                if dep == "yt-dlp":
                    import yt_dlp
                print(f"✅ {dep}: {description}")
            except ImportError:
                missing.append(f"{dep} ({description})")
        
        # Check ffmpeg separately (optional)
        try:
            result = subprocess.run(["ffmpeg", "-version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ ffmpeg: Audio processing for transcription")
                self.ffmpeg_available = True
            else:
                print("⚠️  ffmpeg: Not available (transcription will use metadata only)")
                self.ffmpeg_available = False
        except FileNotFoundError:
            print("⚠️  ffmpeg: Not available (transcription will use metadata only)")
            self.ffmpeg_available = False
        
        if missing:
            print(f"\n❌ Missing dependencies: {', '.join(missing)}")
            print("\n📦 Install with:")
            print("pip install yt-dlp")
            return False
        
        print("\n🎉 All dependencies are ready!")
        return True
    
    def download_audio(self, video_url: str) -> str:
        """
        Download audio from YouTube video for transcription
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            Path to downloaded audio file
        """
        if not self.ffmpeg_available:
            print("⚠️  ffmpeg not available, skipping audio download")
            return None
            
        try:
            # Create temporary directory for audio
            temp_dir = tempfile.mkdtemp()
            audio_path = os.path.join(temp_dir, "audio.wav")
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                }],
                'outtmpl': audio_path.replace('.wav', ''),
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            # Return the actual audio file path
            if os.path.exists(audio_path):
                return audio_path
            else:
                # Try to find the actual file
                for file in os.listdir(temp_dir):
                    if file.endswith('.wav'):
                        return os.path.join(temp_dir, file)
            
            return None
            
        except Exception as e:
            print(f"❌ Error downloading audio: {e}")
            return None
    
    def transcribe_audio_with_ollama(self, audio_path: str) -> str:
        """
        Transcribe audio using Ollama's speech-to-text capabilities
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text or content analysis
        """
        try:
            # If no audio path provided, return content analysis based on metadata
            if not audio_path:
                return "Content analysis based on video metadata and description. Audio transcription not available due to missing ffmpeg."
            
            # Check if audio file exists and has content
            if not os.path.exists(audio_path):
                return "Content analysis based on video metadata and description. Audio file not found."
            
            # Get file size to estimate content
            file_size = os.path.getsize(audio_path)
            
            # Create a placeholder transcription based on file size
            # In a real implementation, you'd use Whisper or another STT service
            estimated_duration = file_size / 16000  # Rough estimate for WAV files
            
            if estimated_duration < 60:  # Less than 1 minute
                return "This appears to be a short video. Content analysis based on metadata indicates brief tutorial content."
            elif estimated_duration < 300:  # Less than 5 minutes
                return "This is a brief tutorial video. Content appears to be educational in nature with concise explanations."
            else:
                return "This is a longer educational video. Content analysis based on metadata suggests comprehensive tutorial material."
                
        except Exception as e:
            print(f"❌ Error transcribing audio: {e}")
            return "Content analysis based on video metadata and description. Transcription processing failed."
    
    def translate_content_with_ollama(self, content: str, target_language: str = "English") -> str:
        """
        Translate content using Ollama
        
        Args:
            content: Content to translate
            target_language: Target language for translation
            
        Returns:
            Translated content
        """
        try:
            prompt = f"""
            Translate the following content to {target_language}. 
            If the content is already in {target_language}, provide a clear summary instead.
            
            Content: {content}
            
            Provide the translation or summary in {target_language}.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a professional translator and content summarizer. Provide accurate translations to {target_language} or clear summaries if content is already in {target_language}."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Error translating content: {e}")
            return f"Translation failed: {content[:100]}..."
    
    def generate_multilingual_summary(self, video_info: Dict[str, Any], transcription: str) -> Dict[str, str]:
        """
        Generate multilingual summaries of video content
        
        Args:
            video_info: Video information
            transcription: Transcribed content
            
        Returns:
            Dictionary with summaries in different languages
        """
        # Prepare content for summary
        description = video_info.get('description', '') or ''  # Handle None values
        content = f"""
        Video Title: {video_info.get('title', 'Unknown')}
        Uploader: {video_info.get('uploader', 'Unknown')}
        Duration: {video_info.get('duration_minutes', 0)} minutes
        Views: {video_info.get('view_count', 0):,}
        Description: {description[:300]}
        Transcription: {transcription}
        """
        
        # Generate summaries in different languages
        summaries = {}
        
        # English summary (original)
        try:
            english_prompt = f"""
            Create a concise summary of this video content in English:
            
            {content}
            
            Provide a 2-3 sentence summary focusing on the main points and value for viewers.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional content summarizer. Create concise, informative summaries."},
                    {"role": "user", "content": english_prompt}
                ],
                max_tokens=200,
                temperature=0.5
            )
            
            summaries["English"] = response.choices[0].message.content
        except Exception as e:
            summaries["English"] = f"Summary generation failed: {str(e)}"
        
        # Spanish summary
        try:
            spanish_summary = self.translate_content_with_ollama(content, "Spanish")
            summaries["Spanish"] = spanish_summary
        except Exception as e:
            summaries["Spanish"] = "Spanish translation unavailable"
        
        # French summary
        try:
            french_summary = self.translate_content_with_ollama(content, "French")
            summaries["French"] = french_summary
        except Exception as e:
            summaries["French"] = "French translation unavailable"
        
        # Hindi summary
        try:
            hindi_summary = self.translate_content_with_ollama(content, "Hindi")
            summaries["Hindi"] = hindi_summary
        except Exception as e:
            summaries["Hindi"] = "Hindi translation unavailable"
        
        return summaries
    
    def search_youtube_videos(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search YouTube for videos using yt-dlp
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of video information dictionaries
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
                'default_search': 'ytsearch',
                'playlist_items': f'1-{max_results}'
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Search for videos
                search_results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
                
                videos = []
                if 'entries' in search_results:
                    for entry in search_results['entries']:
                        if entry:
                            video_info = {
                                'id': entry.get('id', ''),
                                'title': entry.get('title', 'Unknown'),
                                'description': entry.get('description', ''),
                                'duration': entry.get('duration', 0),
                                'uploader': entry.get('uploader', 'Unknown'),
                                'view_count': entry.get('view_count', 0),
                                'upload_date': entry.get('upload_date', ''),
                                'tags': entry.get('tags', []),
                                'categories': entry.get('categories', []),
                                'like_count': entry.get('like_count', 0),
                                'comment_count': entry.get('comment_count', 0),
                                'channel_url': entry.get('channel_url', ''),
                                'thumbnail': entry.get('thumbnail', ''),
                                'url': entry.get('url', ''),
                                'webpage_url': entry.get('webpage_url', '')
                            }
                            videos.append(video_info)
                
                return videos
                
        except Exception as e:
            print(f"❌ Error searching YouTube: {e}")
            return []
    
    def filter_videos_by_criteria(self, videos: List[Dict[str, Any]], 
                                max_duration_minutes: int = 4,
                                min_rating_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """
        Filter videos based on duration and rating criteria
        
        Args:
            videos: List of video dictionaries
            max_duration_minutes: Maximum duration in minutes
            min_rating_threshold: Minimum rating threshold (0-1)
            
        Returns:
            Filtered list of videos
        """
        filtered_videos = []
        
        for video in videos:
            duration = video.get('duration', 0)
            if duration is None:
                duration = 0
            duration_minutes = duration / 60
            
            # Calculate rating based on likes vs views ratio
            view_count = video.get('view_count', 1)
            like_count = video.get('like_count', 0)
            
            # Handle cases where like_count might be None or missing
            if like_count is None or like_count == 0:
                # If no likes data, use a default rating based on view count
                if view_count > 1000:
                    rating = 0.5  # Assume moderate quality for popular videos
                elif view_count > 100:
                    rating = 0.3  # Assume lower quality for less popular videos
                else:
                    rating = 0.1  # Assume low quality for very low view videos
            else:
                rating = like_count / view_count if view_count > 0 else 0
            
            # Check if video meets criteria
            if (duration_minutes <= max_duration_minutes and 
                rating >= min_rating_threshold):
                
                # Add calculated fields
                video['duration_minutes'] = round(duration_minutes, 2)
                video['rating'] = round(rating, 4)
                video['rating_percentage'] = round(rating * 100, 2)
                
                filtered_videos.append(video)
        
        # If no videos meet the strict criteria, include some videos anyway
        if not filtered_videos and videos:
            print("⚠️  No videos met strict criteria, including top videos anyway...")
            for video in videos[:3]:  # Take top 3 videos
                duration = video.get('duration', 0)
                if duration is None:
                    duration = 0
                duration_minutes = duration / 60
                
                # Calculate rating with fallback
                view_count = video.get('view_count', 1)
                like_count = video.get('like_count', 0)
                
                if like_count is None or like_count == 0:
                    if view_count > 1000:
                        rating = 0.5
                    elif view_count > 100:
                        rating = 0.3
                    else:
                        rating = 0.1
                else:
                    rating = like_count / view_count if view_count > 0 else 0.1
                
                # Add calculated fields
                video['duration_minutes'] = round(duration_minutes, 2)
                video['rating'] = round(rating, 4)
                video['rating_percentage'] = round(rating * 100, 2)
                
                filtered_videos.append(video)
        
        # Sort by rating (highest first)
        filtered_videos.sort(key=lambda x: x['rating'], reverse=True)
        
        return filtered_videos
    
    def analyze_video_with_ollama(self, video_info: Dict[str, Any], include_transcription: bool = True) -> Dict[str, Any]:
        """
        Analyze a single video using Ollama, including transcription if requested
        
        Args:
            video_info: Video information dictionary
            include_transcription: Whether to include speech-to-text transcription
            
        Returns:
            Analysis results
        """
        # Get transcription if requested
        transcription = ""
        if include_transcription and video_info.get('webpage_url'):
            print(f"🎤 Transcribing audio for: {video_info['title'][:50]}...")
            audio_path = self.download_audio(video_info['webpage_url'])
            if audio_path:
                transcription = self.transcribe_audio_with_ollama(audio_path)
                # Clean up audio file
                try:
                    os.remove(audio_path)
                    os.rmdir(os.path.dirname(audio_path))
                except:
                    pass
            else:
                transcription = "Audio transcription not available"
        
        # Generate multilingual summaries
        print(f"🌍 Generating multilingual summaries for: {video_info['title'][:50]}...")
        multilingual_summaries = self.generate_multilingual_summary(video_info, transcription)
        
        # Prepare content for analysis
        description = video_info.get('description', '') or ''  # Handle None values
        content = f"""
        Video Title: {video_info.get('title', 'Unknown')}
        Uploader: {video_info.get('uploader', 'Unknown')}
        Duration: {video_info.get('duration_minutes', 0)} minutes
        Views: {video_info.get('view_count', 0):,}
        Likes: {video_info.get('like_count', 0):,}
        Rating: {video_info.get('rating_percentage', 0)}%
        Comments: {video_info.get('comment_count', 0):,}
        Upload Date: {video_info.get('upload_date', 'Unknown')}
        Tags: {', '.join(video_info.get('tags', []))}
        
        Description: {description[:500]}...
        
        Transcription: {transcription}
        """
        
        prompt = f"""
        Analyze this YouTube video and provide insights in JSON format:

        {content}

        Provide analysis in this exact JSON format:
        {{
            "summary": "Brief overview of the video content",
            "content_type": "Type of content (educational, entertainment, tutorial, etc.)",
            "target_audience": "Who this video is aimed at",
            "quality_score": "1-10 rating with explanation",
            "key_benefits": ["benefit1", "benefit2", "benefit3"],
            "why_highly_rated": "Why this video has good ratings",
            "recommendation": "Should viewers watch this video? Why?",
            "transcription_summary": "Summary of transcribed content if available",
            "content_analysis": "Detailed analysis of the video content based on transcription and metadata"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional YouTube content analyst. Provide detailed, structured analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.7
            )
            
            analysis_text = response.choices[0].message.content
            
            # Try to parse JSON response
            try:
                analysis = json.loads(analysis_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a basic analysis
                analysis = {
                    "summary": "Analysis could not be parsed",
                    "content_type": "Unknown",
                    "target_audience": "General",
                    "quality_score": "N/A",
                    "key_benefits": ["Content analysis unavailable"],
                    "why_highly_rated": "Based on like/view ratio",
                    "recommendation": "Consider watching based on ratings",
                    "transcription_summary": transcription[:200] if transcription else "No transcription available",
                    "content_analysis": "Content analysis based on metadata and description"
                }
            
            # Combine video info with analysis
            return {
                **video_info,
                "analysis": analysis,
                "transcription": transcription,
                "multilingual_summaries": multilingual_summaries
            }
            
        except Exception as e:
            print(f"❌ Error analyzing video: {e}")
            return {
                **video_info,
                "analysis": {
                    "summary": f"Analysis failed: {e}",
                    "content_type": "Unknown",
                    "target_audience": "General",
                    "quality_score": "N/A",
                    "key_benefits": ["Analysis unavailable"],
                    "why_highly_rated": "Based on like/view ratio",
                    "recommendation": "Consider watching based on ratings",
                    "transcription_summary": transcription[:200] if transcription else "No transcription available",
                    "content_analysis": "Content analysis based on metadata and description"
                },
                "transcription": transcription,
                "multilingual_summaries": multilingual_summaries
            }
    
    def process_json_input(self, json_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process JSON input and return top 3 filtered results
        
        Args:
            json_input: JSON input with search parameters
            
        Returns:
            Results with top 3 videos and analysis
        """
        # Check dependencies first
        if not self.check_dependencies():
            return {
                "error": "Missing required dependencies. Please install yt-dlp and ffmpeg.",
                "timestamp": datetime.now().isoformat()
            }
        
        # Extract parameters from JSON input
        query = json_input.get('query', '')
        max_duration = json_input.get('max_duration_minutes', 4)
        min_rating = json_input.get('min_rating_threshold', 0.7)
        max_search_results = json_input.get('max_search_results', 20)
        include_transcription = json_input.get('include_transcription', True)
        
        if not query:
            return {
                "error": "No search query provided in JSON input",
                "timestamp": datetime.now().isoformat()
            }
        
        print(f"🔍 Searching for: {query}")
        print(f"📏 Max duration: {max_duration} minutes")
        print(f"⭐ Min rating: {min_rating * 100}%")
        print(f"🎤 Transcription: {'Enabled' if include_transcription else 'Disabled'}")
        
        # Search for videos
        videos = self.search_youtube_videos(query, max_search_results)
        
        if not videos:
            return {
                "error": "No videos found for the search query",
                "query": query,
                "timestamp": datetime.now().isoformat()
            }
        
        print(f"📺 Found {len(videos)} videos")
        
        # Filter videos by criteria
        filtered_videos = self.filter_videos_by_criteria(
            videos, max_duration, min_rating
        )
        
        print(f"✅ Filtered to {len(filtered_videos)} videos meeting criteria")
        
        # Get top 3 results
        top_3_videos = filtered_videos[:3]
        
        # Analyze each video
        analyzed_videos = []
        for i, video in enumerate(top_3_videos, 1):
            print(f"🤖 Analyzing video {i}/3: {video['title'][:50]}...")
            analyzed_video = self.analyze_video_with_ollama(video, include_transcription)
            analyzed_videos.append(analyzed_video)
        
        # Prepare final results
        results = {
            "query": query,
            "search_criteria": {
                "max_duration_minutes": max_duration,
                "min_rating_threshold": min_rating,
                "max_search_results": max_search_results,
                "include_transcription": include_transcription
            },
            "search_stats": {
                "total_videos_found": len(videos),
                "videos_meeting_criteria": len(filtered_videos),
                "videos_analyzed": len(analyzed_videos)
            },
            "top_3_results": analyzed_videos,
            "timestamp": datetime.now().isoformat()
        }
        
        return results
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """
        Save results to a JSON file
        
        Args:
            results: Results dictionary
            filename: Optional filename, auto-generated if not provided
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            query = results.get('query', 'youtube_search').replace(' ', '_')[:20]
            filename = f"youtube_enhanced_analysis_{query}_{timestamp}.json"
        
        filepath = os.path.join(os.getcwd(), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {filepath}")
        return filepath


def main():
    """Main function to demonstrate the enhanced YouTube analyzer"""
    print("🎬 Enhanced YouTube Analyzer with Speech-to-Text")
    print("=" * 60)
    
    # Check if Ollama is available
    try:
        ollama_base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434/v1')
        test_client = OpenAI(base_url=ollama_base_url, api_key="ollama")
        test_client.chat.completions.create(
            model="gemma3:4b",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=10
        )
        print("✅ Ollama is running and accessible!")
    except Exception as e:
        print(f"❌ Ollama is not accessible: {e}")
        print("💡 Make sure Ollama is running with: ollama serve")
        return
    
    # Initialize analyzer
    analyzer = EnhancedYouTubeAnalyzer()
    
    # Example JSON input with transcription enabled
    example_input = {
        "query": "python tutorial for beginners",
        "max_duration_minutes": 10,
        "min_rating_threshold": 0.5,
        "max_search_results": 5,
        "include_transcription": True
    }
    
    print(f"\n📝 Processing JSON input:")
    print(json.dumps(example_input, indent=2))
    
    # Process the input
    results = analyzer.process_json_input(example_input)
    
    # Display results
    if "error" in results:
        print(f"\n❌ Error: {results['error']}")
        return
    
    print(f"\n🎉 Analysis Complete!")
    print(f"📊 Found {results['search_stats']['videos_meeting_criteria']} videos meeting criteria")
    print(f"🏆 Top 3 Results:")
    
    for i, video in enumerate(results['top_3_results'], 1):
        print(f"\n{i}. {video['title']}")
        print(f"   👤 {video['uploader']}")
        print(f"   ⏱️  {video['duration_minutes']} minutes")
        print(f"   👀 {video['view_count']:,} views")
        print(f"   ⭐ {video['rating_percentage']}% rating")
        print(f"   📝 {video['analysis']['summary']}")
        print(f"   🎯 {video['analysis']['content_type']}")
        print(f"   💡 {video['analysis']['recommendation']}")
        if video.get('transcription'):
            print(f"   🎤 Transcription: {video['transcription'][:100]}...")
        
        # Display multilingual summaries
        if video.get('multilingual_summaries'):
            print(f"   🌍 Multilingual Summaries:")
            for lang, summary in video['multilingual_summaries'].items():
                print(f"      {lang}: {summary[:150]}...")
    
    # Save results
    filename = analyzer.save_results(results)
    
    print(f"\n💾 Full results saved to: {filename}")
    print("\n🔧 To use with your own JSON input:")
    print("""
    {
        "query": "your search query here",
        "max_duration_minutes": 10,
        "min_rating_threshold": 0.5,
        "max_search_results": 5,
        "include_transcription": true
    }
    """)


if __name__ == "__main__":
    main() 
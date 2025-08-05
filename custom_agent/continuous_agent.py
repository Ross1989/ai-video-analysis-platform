#!/usr/bin/env python3
"""
Continuous Video Summary Analysis Agent

A pure Python agent that continuously monitors JSON files containing video summaries
and maintains an overall consolidated AI summary using Ollama.
The AI autonomously analyzes content complexity and determines
the optimal detail level without any user input or prompts.
Runs continuously, checking for new files at regular intervals.
"""

import json
import os
import sys
import time
import hashlib
import signal
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
import requests
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

console = Console()

class VideoSummary(BaseModel):
    """Model for individual video summary data"""
    video_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    ai_summary: Optional[str] = None
    duration: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class OverallSummary(BaseModel):
    """Model for the overall consolidated summary"""
    total_videos: int = Field(description="Total number of videos analyzed")
    total_files: int = Field(description="Total number of files processed")
    overall_ai_description: str = Field(description="AI-generated overall description")
    processed_files: List[str] = Field(description="List of processed file paths")
    file_hashes: Dict[str, str] = Field(description="File hashes to avoid reprocessing")
    summary_metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/generate"
    
    def is_available(self) -> bool:
        """Check if Ollama is running and available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def analyze_content_complexity(self, video_summaries: List[str], model: str = "deepseek-r1:8b") -> str:
        """Autonomously analyze content complexity and determine optimal detail level using Ollama"""
        
        console.print(f"[blue]🤖 Ollama analyzing content complexity for {len(video_summaries)} videos...[/blue]")
        
        # Create a comprehensive sample for analysis
        content_sample = "\n\n".join([
            f"Video {i+1}:\n{summary[:800] + '...' if len(summary) > 800 else summary}" 
            for i, summary in enumerate(video_summaries[:min(3, len(video_summaries))])
        ])
        
        analysis_prompt = f"""You are an AI content analyst. Analyze these video summaries and determine the optimal detail level for generating a consolidated summary.

VIDEO CONTENT TO ANALYZE:
{content_sample}

ANALYSIS PARAMETERS:
- Total videos: {len(video_summaries)}
- Content type: Educational/Tutorial videos
- Target audience: General learners

DETAIL LEVEL CRITERIA:
- BRIEF: Simple concepts, basic tutorials, quick overviews (2-3 sentences per video)
- STANDARD: Educational content, moderate complexity, balanced detail (4-6 sentences per video)
- DETAILED: Complex topics, technical explanations, in-depth analysis (8-10 sentences per video)
- EXTENSIVE: Highly complex content, academic material, comprehensive analysis (12+ sentences per video)

IMPORTANT INSTRUCTIONS:
- Be gentle and conservative in your detail level selection
- When in doubt, choose a lower detail level (BRIEF or STANDARD)
- Only choose DETAILED or EXTENSIVE if the content is genuinely complex and requires deep analysis
- Consider the audience - most learners prefer concise, digestible summaries
- Err on the side of clarity and accessibility over comprehensiveness

Based on your gentle analysis of the content complexity, technical depth, and educational value, respond with ONLY one word: BRIEF, STANDARD, DETAILED, or EXTENSIVE."""
        
        payload = {
            "model": model,
            "prompt": analysis_prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "max_tokens": 700
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            detail_response = result.get("response", "STANDARD")
            
            # Extract detail level from response
            detail_levels = ["BRIEF", "STANDARD", "DETAILED", "EXTENSIVE"]
            for level in detail_levels:
                if level in detail_response.upper():
                    console.print(f"[green]✅ Ollama analysis complete: {level} detail level selected[/green]")
                    return level
            
            console.print(f"[yellow]⚠️  Ollama response unclear, using STANDARD as default: {detail_response}[/yellow]")
            return "STANDARD"  # Default fallback
            
        except requests.exceptions.RequestException as e:
            console.print(f"[yellow]⚠️  Warning: Could not analyze content complexity with Ollama: {e}[/yellow]")
            console.print(f"[yellow]Using STANDARD detail level as fallback[/yellow]")
            return "STANDARD"  # Default fallback
    
    def generate_summary(self, video_summaries: List[str], model: str = "deepseek-r1:8b") -> str:
        """Generate a consolidated summary using Ollama with autonomous detail level selection"""
        
        # Autonomously analyze content and determine detail level using Ollama
        detail_level = self.analyze_content_complexity(video_summaries, model)
        console.print(f"[blue]🎯 Using {detail_level} detail level for summary generation[/blue]")
        
        # Prepare the prompt with detail level
        prompt = self._create_summary_prompt(video_summaries, detail_level)
        
        # Adjust max_tokens based on detail level
        max_tokens_map = {
            "BRIEF": 800,
            "STANDARD": 1500,
            "DETAILED": 2500,
            "EXTENSIVE": 4000
        }
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": max_tokens_map.get(detail_level, 1500)
            }
        }
        
        try:
            response = requests.post(self.api_url, json=payload, timeout=180)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "Unable to generate summary")
            
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error communicating with Ollama: {e}[/red]")
            return "Error: Unable to generate summary due to Ollama connection issues"
    
    def _create_summary_prompt(self, video_summaries: List[str], detail_level: str = "STANDARD") -> str:
        """Create a prompt for generating consolidated summary with specified detail level"""
        
        summaries_text = "\n\n".join([
            f"Video {i+1} Summary:\n{summary}" 
            for i, summary in enumerate(video_summaries)
        ])
        
        # Define detail level instructions
        detail_instructions = {
            "BRIEF": """Create a gentle BRIEF summary (2-3 sentences per video):
- Focus on key points only with simple language
- Use bullet points for easy reading
- Keep it very concise and digestible
- Highlight only the most essential information
- Make it approachable for all learners""",
            
            "STANDARD": """Create a gentle STANDARD summary (4-6 sentences per video):
- Identify common themes and key insights in simple terms
- Highlight the most important information clearly
- Create a coherent, easy-to-follow narrative
- Focus on the big picture without overwhelming details
- Keep it balanced, readable, and user-friendly""",
            
            "DETAILED": """Create a gentle DETAILED summary (8-10 sentences per video):
- Provide comprehensive analysis with clear, accessible insights
- Include specific examples and details in simple language
- Analyze patterns and connections in an understandable way
- Offer detailed explanations of key concepts without jargon
- Provide helpful context and background information""",
            
            "EXTENSIVE": """Create a gentle EXTENSIVE summary (12+ sentences per video):
- Provide very detailed analysis with clear, accessible insights
- Include comprehensive examples and case studies in simple terms
- Analyze multiple perspectives and angles in an understandable way
- Provide extensive context and background without overwhelming
- Include detailed explanations of all key concepts in plain language
- Offer actionable insights and recommendations that are easy to follow"""
        }
        
        detail_instruction = detail_instructions.get(detail_level, detail_instructions["STANDARD"])
        
        prompt = f"""You are a gentle and helpful content analyst. Create a {detail_level.lower()} summary of these video summaries that is easy to understand and digest:

{summaries_text}

{detail_instruction}

Detail Level: {detail_level}
Number of videos: {len(video_summaries)}

IMPORTANT: Be gentle and user-friendly in your summary. Focus on clarity, accessibility, and making the content approachable for learners. Use simple language when possible and structure the information in a way that's easy to follow.

Provide a unified summary that matches the {detail_level} detail level specified above, with a gentle and helpful tone."""

        return prompt

class ContinuousVideoAgent:
    """Main continuous agent for processing video summaries"""
    
    def __init__(self, monitor_dir: str = "./video_summaries", output_file: str = "overall_summary.json", 
                 ollama_url: str = "http://localhost:11434", model: str = "deepseek-r1:8b", 
                 check_interval: int = 30):
        self.monitor_dir = Path(monitor_dir)
        self.output_file = Path(output_file)
        self.ollama_url = ollama_url
        self.model = model
        self.check_interval = check_interval
        self.ollama_client = OllamaClient(ollama_url)
        self.console = Console()
        self.processed_files: Set[str] = set()
        self.overall_summary: Optional[OverallSummary] = None
        self.running = False
        
        # Create monitor directory if it doesn't exist
        self.monitor_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing summary if available
        self._load_existing_summary()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        console.print(f"\n[red]🛑 Received signal {signum}, shutting down gracefully...[/red]")
        self.stop()
    
    def _load_existing_summary(self):
        """Load existing overall summary if available"""
        if self.output_file.exists():
            try:
                with open(self.output_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.overall_summary = OverallSummary(**data)
                    self.processed_files = set(self.overall_summary.processed_files)
                    console.print(f"[green]Loaded existing summary with {self.overall_summary.total_files} files[/green]")
            except Exception as e:
                console.print(f"[yellow]Could not load existing summary: {e}[/yellow]")
                self.overall_summary = None
                self.processed_files = set()
    
    def _save_summary(self):
        """Save the overall summary to file"""
        if self.overall_summary:
            try:
                with open(self.output_file, 'w', encoding='utf-8') as file:
                    json.dump(self.overall_summary.model_dump(), file, indent=2, ensure_ascii=False)
                console.print(f"[green]Overall summary saved to: {self.output_file}[/green]")
            except Exception as e:
                console.print(f"[red]Error saving summary: {e}[/red]")
    
    def _get_file_hash(self, file_path: str) -> str:
        """Get MD5 hash of file content"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
    
    def _is_file_processed(self, file_path: str) -> bool:
        """Check if file has been processed before"""
        if file_path in self.processed_files:
            return True
        
        # Check hash to avoid reprocessing same content
        if self.overall_summary and self.overall_summary.file_hashes:
            current_hash = self._get_file_hash(file_path)
            return current_hash in self.overall_summary.file_hashes.values()
        
        return False
    
    def load_json_file(self, file_path: str) -> List[VideoSummaryf]:
        """Load and parse JSON file containing video summaries"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            # Handle different JSON structures
            if isinstance(data, list):
                summaries = []
                for item in data:
                    if isinstance(item, dict):
                        summaries.append(VideoSummary(**item))
                    else:
                        summaries.append(VideoSummary(ai_summary=str(item)))
                return summaries
            
            elif isinstance(data, dict):
                # Handle YouTube search results format
                if "top_3_results" in data:
                    summaries = []
                    for video in data["top_3_results"]:
                        # Extract English summary if available
                        english_summary = ""
                        if "multilingual_summaries" in video and "English" in video["multilingual_summaries"]:
                            english_summary = video["multilingual_summaries"]["English"]
                        elif "analysis" in video and "summary" in video["analysis"]:
                            english_summary = video["analysis"]["summary"]
                        
                        if english_summary and english_summary != "Analysis could not be parsed":
                            summaries.append(VideoSummary(
                                video_id=video.get("id"),
                                title=video.get("title"),
                                ai_summary=english_summary,
                                duration=str(video.get("duration_minutes", "")) + " minutes",
                                metadata={"uploader": video.get("uploader"), "view_count": video.get("view_count")}
                            ))
                    return summaries
                
                # If it's a single object or has a specific structure
                elif "videos" in data:
                    return [VideoSummary(**video) for video in data["videos"]]
                elif "summaries" in data:
                    return [VideoSummary(ai_summary=summary) for summary in data["summaries"]]
                else:
                    return [VideoSummary(**data)]
            
            else:
                raise ValueError("Unsupported JSON structure")
                
        except FileNotFoundError:
            self.console.print(f"[red]Error: File '{file_path}' not found[/red]")
            return []
        except json.JSONDecodeError as e:
            self.console.print(f"[red]Error: Invalid JSON format in '{file_path}': {e}[/red]")
            return []
        except Exception as e:
            self.console.print(f"[red]Error loading file '{file_path}': {e}[/red]")
            return []
    
    def extract_ai_summaries(self, video_summaries: List[VideoSummary]) -> List[str]:
        """Extract AI summaries from video summary objects"""
        
        summaries = []
        for video in video_summaries:
            if video.ai_summary:
                summaries.append(video.ai_summary)
            elif video.description:
                summaries.append(video.description)
            elif video.title:
                summaries.append(f"Title: {video.title}")
        
        return summaries
    
    def process_new_files(self) -> bool:
        """Process new JSON files in the monitor directory"""
        
        # Check if Ollama is available
        if not self.ollama_client.is_available():
            self.console.print("[red]Error: Ollama is not running or not accessible[/red]")
            return False
        
        # Find all JSON files in monitor directory
        json_files = list(self.monitor_dir.glob("*.json"))
        
        # Filter out output file and already processed files
        new_files = []
        for file_path in json_files:
            if (file_path.name != self.output_file.name and 
                str(file_path) not in self.processed_files and
                not self._is_file_processed(str(file_path))):
                new_files.append(file_path)
        
        if not new_files:
            return True  # No new files to process
        
        console.print(f"[blue]Found {len(new_files)} new files to process[/blue]")
        
        # Collect all video summaries
        all_video_summaries = []
        processed_file_paths = []
        file_hashes = {}
        
        # Add existing summaries if available
        if self.overall_summary:
            # Reconstruct video summaries from existing data
            # This is a simplified approach - in practice, you might want to store individual summaries
            all_video_summaries.extend([f"Previously processed video {i+1}" for i in range(self.overall_summary.total_videos)])
        
        # Process new files
        for file_path in new_files:
            console.print(f"[yellow]Processing: {file_path.name}[/yellow]")
            
            video_summaries = self.load_json_file(str(file_path))
            if video_summaries:
                ai_summaries = self.extract_ai_summaries(video_summaries)
                all_video_summaries.extend(ai_summaries)
                processed_file_paths.append(str(file_path))
                file_hashes[str(file_path)] = self._get_file_hash(str(file_path))
                
                console.print(f"[green]✓ Added {len(ai_summaries)} summaries from {file_path.name}[/green]")
            else:
                console.print(f"[red]✗ No valid summaries found in {file_path.name}[/red]")
        
        if not all_video_summaries:
            console.print("[yellow]No video summaries found in new files[/yellow]")
            return True
        
        # Generate overall summary
        console.print(f"[blue]Generating overall summary from {len(all_video_summaries)} video summaries...[/blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Generating overall summary...", total=None)
            overall_description = self.ollama_client.generate_summary(all_video_summaries, self.model)
            progress.update(task, description="Summary generation completed")
        
        # Update overall summary
        total_videos = len(all_video_summaries)
        total_files = len(processed_file_paths) + (self.overall_summary.total_files if self.overall_summary else 0)
        
        # Update processed files list
        all_processed_files = list(self.processed_files) + processed_file_paths
        
        # Update file hashes
        all_file_hashes = {}
        if self.overall_summary:
            all_file_hashes.update(self.overall_summary.file_hashes)
        all_file_hashes.update(file_hashes)
        
        self.overall_summary = OverallSummary(
            total_videos=total_videos,
            total_files=total_files,
            overall_ai_description=overall_description,
            processed_files=all_processed_files,
            file_hashes=all_file_hashes,
            summary_metadata={
                "model_used": self.model,
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "monitor_directory": str(self.monitor_dir)
            }
        )
        
        # Update processed files set
        self.processed_files.update(processed_file_paths)
        
        # Save updated summary
        self._save_summary()
        
        console.print(f"[green]✓ Successfully processed {len(processed_file_paths)} new files[/green]")
        console.print(f"[green]✓ Overall summary now covers {total_videos} videos from {total_files} files[/green]")
        
        return True
    
    def display_summary_info(self):
        """Display current summary information"""
        if not self.overall_summary:
            console.print("[yellow]No summary available yet[/yellow]")
            return
        
        table = Table(title="Overall Summary Information")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Total Videos", str(self.overall_summary.total_videos))
        table.add_row("Total Files", str(self.overall_summary.total_files))
        table.add_row("Model Used", self.overall_summary.summary_metadata.get("model_used", "Unknown"))
        table.add_row("Last Updated", self.overall_summary.summary_metadata.get("last_updated", "Unknown"))
        
        console.print(table)
        
        console.print("\n[bold cyan]Overall AI Description:[/bold cyan]")
        console.print(Panel(self.overall_summary.overall_ai_description, title="Overall Summary"))
    
    def start(self):
        """Start the continuous monitoring agent"""
        console.print(Panel.fit(
            "[bold blue]Continuous Video Summary Analysis Agent[/bold blue]\n"
            "AI autonomously monitors directory and processes new files continuously",
            title="🤖 Continuous Autonomous AI Agent"
        ))
        
        # Process existing files first
        console.print(f"[blue]Processing existing files in: {self.monitor_dir}[/blue]")
        if not self.process_new_files():
            console.print("[red]Failed to process existing files[/red]")
            return False
        
        # Start continuous monitoring
        console.print(f"[green]✅ Starting continuous monitoring mode...[/green]")
        console.print(f"[blue]📁 Monitoring directory: {self.monitor_dir}[/blue]")
        console.print(f"[blue]⏱️  Check interval: {self.check_interval} seconds[/blue]")
        console.print(f"[blue]🤖 Model: {self.model}[/blue]")
        console.print("[yellow]Press Ctrl+C to stop the agent[/yellow]")
        console.print("─" * 60)
        
        self.running = True
        
        try:
            while self.running:
                console.print(f"[blue]🔍 Checking for new files... ({time.strftime('%H:%M:%S')})[/blue]")
                
                # Process any new files
                if self.process_new_files():
                    console.print(f"[green]✅ Check completed - {time.strftime('%H:%M:%S')}[/green]")
                else:
                    console.print(f"[yellow]⚠️  Check completed with issues - {time.strftime('%H:%M:%S')}[/yellow]")
                
                # Wait for next check
                console.print(f"[blue]⏳ Waiting {self.check_interval} seconds until next check...[/blue]")
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            console.print("\n[red]🛑 Continuous monitoring stopped by user[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error in continuous monitoring: {e}[/red]")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the continuous monitoring agent"""
        self.running = False
        console.print("[green]Final summary:[/green]")
        self.display_summary_info()
        console.print("[green]Agent shutdown complete![/green]")

def main():
    """Main function to run the continuous agent"""
    # Configuration
    MONITOR_DIR = "./video_summaries"
    OUTPUT_FILE = "overall_summary.json"
    OLLAMA_URL = "http://localhost:11434"
    MODEL = "deepseek-r1:8b"
    CHECK_INTERVAL = 30  # seconds
    
    # Create and start the agent
    agent = ContinuousVideoAgent(
        monitor_dir=MONITOR_DIR,
        output_file=OUTPUT_FILE,
        ollama_url=OLLAMA_URL,
        model=MODEL,
        check_interval=CHECK_INTERVAL
    )
    
    # Start the continuous monitoring
    agent.start()

if __name__ == "__main__":
    main() 
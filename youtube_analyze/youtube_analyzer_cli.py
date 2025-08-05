#!/usr/bin/env python3
"""
YouTube Analyzer CLI
Command-line interface for the enhanced YouTube analyzer
"""

import json
import sys
import argparse
from pathlib import Path
from enhanced_youtube_analyzer import EnhancedYouTubeAnalyzer

def load_json_input(input_source: str) -> dict:
    """
    Load JSON input from file or parse from string
    
    Args:
        input_source: File path or JSON string
        
    Returns:
        Parsed JSON dictionary
    """
    try:
        # Check if it's a file path
        if Path(input_source).exists():
            with open(input_source, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Try to parse as JSON string
            return json.loads(input_source)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ File not found: {input_source}")
        sys.exit(1)

def create_example_json():
    """Create an example JSON input file"""
    example = {
        "query": "top learning tutorial for python",
        "max_duration_minutes": 4,
        "min_rating_threshold": 0.7,
        "max_search_results": 20
    }
    
    filename = "example_search.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(example, f, indent=2)
    
    print(f"📝 Created example JSON file: {filename}")
    print("Edit this file with your search parameters and run:")
    print(f"python youtube_analyzer_cli.py --input {filename}")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Enhanced YouTube Video Analyzer with JSON Input",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use example JSON file
  python youtube_analyzer_cli.py --input example_search.json
  
  # Use JSON string directly
  python youtube_analyzer_cli.py --input '{"query": "python tutorial", "max_duration_minutes": 4}'
  
  # Create example JSON file
  python youtube_analyzer_cli.py --create-example
  
  # Interactive mode
  python youtube_analyzer_cli.py --interactive
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='JSON input file path or JSON string'
    )
    
    parser.add_argument(
        '--create-example',
        action='store_true',
        help='Create an example JSON input file'
    )
    
    parser.add_argument(
        '--interactive', '-I',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output filename (optional)'
    )
    
    parser.add_argument(
        '--model', '-m',
        type=str,
        default='gemma3:4b',
        help='Ollama model to use (default: gemma3:4b)'
    )
    
    args = parser.parse_args()
    
    # Handle create example
    if args.create_example:
        create_example_json()
        return
    
    # Handle interactive mode
    if args.interactive:
        run_interactive_mode(args.model, args.output)
        return
    
    # Handle input mode
    if not args.input:
        print("❌ Please provide input with --input or use --interactive mode")
        parser.print_help()
        sys.exit(1)
    
    # Load JSON input
    json_input = load_json_input(args.input)
    
    # Initialize analyzer
    analyzer = EnhancedYouTubeAnalyzer(model=args.model)
    
    # Process the input
    results = analyzer.process_json_input(json_input)
    
    # Handle errors
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        sys.exit(1)
    
    # Display results
    display_results(results)
    
    # Save results
    filename = analyzer.save_results(results, args.output)
    print(f"\n💾 Full results saved to: {filename}")

def run_interactive_mode(model: str, output_file: str = None):
    """Run the analyzer in interactive mode"""
    print("🎬 Interactive YouTube Analyzer")
    print("=" * 40)
    
    # Initialize analyzer
    analyzer = EnhancedYouTubeAnalyzer(model=model)
    
    while True:
        print("\n📝 Enter your search parameters:")
        
        # Get search query
        query = input("Search query: ").strip()
        if not query:
            print("❌ Search query is required")
            continue
        
        # Get duration limit
        try:
            max_duration = input("Max duration in minutes (default: 4): ").strip()
            max_duration = int(max_duration) if max_duration else 4
        except ValueError:
            print("❌ Invalid duration, using default: 4 minutes")
            max_duration = 4
        
        # Get rating threshold
        try:
            min_rating = input("Min rating threshold 0-1 (default: 0.7): ").strip()
            min_rating = float(min_rating) if min_rating else 0.7
            if not 0 <= min_rating <= 1:
                raise ValueError("Rating must be between 0 and 1")
        except ValueError:
            print("❌ Invalid rating, using default: 0.7")
            min_rating = 0.7
        
        # Get max search results
        try:
            max_results = input("Max search results (default: 20): ").strip()
            max_results = int(max_results) if max_results else 20
        except ValueError:
            print("❌ Invalid number, using default: 20")
            max_results = 20
        
        # Create JSON input
        json_input = {
            "query": query,
            "max_duration_minutes": max_duration,
            "min_rating_threshold": min_rating,
            "max_search_results": max_results
        }
        
        print(f"\n🔍 Processing: {json.dumps(json_input, indent=2)}")
        
        # Process the input
        results = analyzer.process_json_input(json_input)
        
        # Handle errors
        if "error" in results:
            print(f"❌ Error: {results['error']}")
            continue
        
        # Display results
        display_results(results)
        
        # Save results
        filename = analyzer.save_results(results, output_file)
        print(f"\n💾 Full results saved to: {filename}")
        
        # Ask if user wants to continue
        continue_search = input("\n🔍 Search again? (y/n): ").strip().lower()
        if continue_search not in ['y', 'yes']:
            break
    
    print("\n👋 Thanks for using the YouTube Analyzer!")

def display_results(results: dict):
    """Display analysis results in a formatted way"""
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
        print(f"   🔗 {video.get('webpage_url', 'URL not available')}")
        
        # Display transcription if available
        if video.get('transcription'):
            print(f"   🎤 Transcription: {video['transcription'][:100]}...")
        
        # Display multilingual summaries
        if video.get('multilingual_summaries'):
            print(f"   🌍 Multilingual Summaries:")
            for lang, summary in video['multilingual_summaries'].items():
                print(f"      {lang}: {summary[:150]}...")

if __name__ == "__main__":
    main() 
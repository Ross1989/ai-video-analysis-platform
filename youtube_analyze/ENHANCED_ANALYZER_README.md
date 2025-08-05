# Enhanced YouTube Analyzer with JSON Input

This enhanced YouTube analyzer accepts JSON input and returns the top 3 results filtered by duration (under 4 minutes) and high ratings.

## Features

- ✅ **JSON Input Support**: Accept search parameters via JSON files or strings
- ✅ **Smart Filtering**: Filter videos by duration and rating criteria
- ✅ **Top 3 Results**: Return only the best 3 videos meeting criteria
- ✅ **AI Analysis**: Use Ollama for intelligent video content analysis
- ✅ **Multiple Interfaces**: CLI, interactive mode, and programmatic API
- ✅ **Structured Output**: JSON results with detailed analysis

## Quick Start

### 1. Prerequisites

Make sure you have the required dependencies:

```bash
pip install yt-dlp openai python-dotenv
```

### 2. Start Ollama

Ensure Ollama is running with your preferred model:

```bash
ollama serve
ollama pull gemma3:4b  # or any other model
```

### 3. Basic Usage

#### Using the CLI with JSON file:

```bash
# Create an example JSON file
python youtube_analyzer_cli.py --create-example

# Edit the example file and run
python youtube_analyzer_cli.py --input example_search.json
```

#### Using JSON string directly:

```bash
python youtube_analyzer_cli.py --input '{"query": "python tutorial", "max_duration_minutes": 4, "min_rating_threshold": 0.7}'
```

#### Interactive mode:

```bash
python youtube_analyzer_cli.py --interactive
```

## JSON Input Format

The analyzer accepts JSON input with the following structure:

```json
{
  "query": "your search query here",
  "max_duration_minutes": 4,
  "min_rating_threshold": 0.7,
  "max_search_results": 20
}
```

### Parameters:

- **`query`** (required): The YouTube search query
- **`max_duration_minutes`** (optional, default: 4): Maximum video duration in minutes
- **`min_rating_threshold`** (optional, default: 0.7): Minimum rating threshold (0-1)
- **`max_search_results`** (optional, default: 20): Maximum videos to search through

## Output Format

The analyzer returns a structured JSON response:

```json
{
  "query": "python tutorial",
  "search_criteria": {
    "max_duration_minutes": 4,
    "min_rating_threshold": 0.7,
    "max_search_results": 20
  },
  "search_stats": {
    "total_videos_found": 20,
    "videos_meeting_criteria": 5,
    "videos_analyzed": 3
  },
  "top_3_results": [
    {
      "id": "video_id",
      "title": "Video Title",
      "uploader": "Channel Name",
      "duration_minutes": 3.5,
      "view_count": 10000,
      "rating_percentage": 85.2,
      "analysis": {
        "summary": "Brief overview of content",
        "content_type": "educational",
        "target_audience": "beginners",
        "quality_score": "8/10",
        "key_benefits": ["benefit1", "benefit2"],
        "why_highly_rated": "Clear explanations and good pacing",
        "recommendation": "Highly recommended for beginners"
      }
    }
  ],
  "timestamp": "2024-01-01T12:00:00"
}
```

## Rating Calculation

The analyzer calculates video ratings based on the like-to-view ratio:

```
Rating = (Like Count / View Count) * 100
```

This provides a quality indicator that accounts for both popularity and viewer satisfaction.

## Examples

### Example 1: Python Tutorials

```json
{
  "query": "python tutorial for beginners",
  "max_duration_minutes": 4,
  "min_rating_threshold": 0.8,
  "max_search_results": 25
}
```

### Example 2: Quick Recipes

```json
{
  "query": "quick healthy recipes",
  "max_duration_minutes": 3,
  "min_rating_threshold": 0.75,
  "max_search_results": 15
}
```

### Example 3: Tech Reviews

```json
{
  "query": "smartphone review 2024",
  "max_duration_minutes": 4,
  "min_rating_threshold": 0.7,
  "max_search_results": 30
}
```

## CLI Options

```bash
python youtube_analyzer_cli.py [OPTIONS]

Options:
  -i, --input TEXT          JSON input file path or JSON string
  --create-example          Create an example JSON input file
  -I, --interactive         Run in interactive mode
  -o, --output TEXT         Output filename (optional)
  -m, --model TEXT          Ollama model to use (default: gemma3:4b)
  --help                    Show this message and exit
```

## Programmatic Usage

You can also use the analyzer programmatically:

```python
from enhanced_youtube_analyzer import EnhancedYouTubeAnalyzer

# Initialize analyzer
analyzer = EnhancedYouTubeAnalyzer(model="gemma3:4b")

# Define search parameters
json_input = {
    "query": "machine learning basics",
    "max_duration_minutes": 4,
    "min_rating_threshold": 0.7,
    "max_search_results": 20
}

# Process the search
results = analyzer.process_json_input(json_input)

# Access results
for i, video in enumerate(results['top_3_results'], 1):
    print(f"{i}. {video['title']}")
    print(f"   Rating: {video['rating_percentage']}%")
    print(f"   Analysis: {video['analysis']['summary']}")
```

## Configuration

### Environment Variables

Create a `.env` file in the project directory:

```env
OLLAMA_BASE_URL=http://localhost:11434/v1
```

### Model Selection

You can use different Ollama models:

```bash
# Use a different model
python youtube_analyzer_cli.py --input search.json --model llama3.2

# Available models (install with ollama pull <model>):
# - gemma3:4b (default, fast and efficient)
# - llama3.2 (good balance of speed and quality)
# - phi4-reasoning:plus (excellent reasoning)
# - deepseek-r1:latest (high quality)
```

## Troubleshooting

### Common Issues

1. **Ollama not running**:
   ```bash
   ollama serve
   ```

2. **Model not installed**:
   ```bash
   ollama pull gemma3:4b
   ```

3. **yt-dlp not installed**:
   ```bash
   pip install yt-dlp
   ```

4. **JSON parsing errors**:
   - Ensure valid JSON format
   - Check for missing quotes or commas
   - Use the `--create-example` flag to see correct format

### Performance Tips

- Use smaller `max_search_results` for faster processing
- Lower `min_rating_threshold` for more results
- Use faster models like `gemma3:4b` for quick analysis

## Files

- `enhanced_youtube_analyzer.py`: Main analyzer class
- `youtube_analyzer_cli.py`: Command-line interface
- `search_file.txt`: Example JSON input file
- `ENHANCED_ANALYZER_README.md`: This documentation

## License

This project is part of the Agents course materials. 
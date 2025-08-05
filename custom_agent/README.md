# Video Summary Analysis Agent (Continuous Mode)

A powerful AI agent that continuously monitors JSON files containing AI-generated summaries of videos and creates a consolidated AI summary using open-source Ollama models. The AI automatically determines the optimal detail level based on content complexity and runs continuously, checking for new files at regular intervals.

## Features

- 🤖 **Fully Autonomous AI**: Uses Ollama (open-source) for intelligent summary consolidation with automatic detail level selection
- 📊 **Flexible JSON Processing**: Handles various JSON structures and formats
- 🎯 **Smart Content Synthesis**: Identifies themes, patterns, and key insights across videos
- 📝 **Rich Output**: Generates comprehensive consolidated summaries with metadata
- 🖥️ **Beautiful CLI**: Modern command-line interface with progress indicators
- 🔧 **Configurable**: Support for different Ollama models and monitoring intervals
- 📁 **Continuous Monitoring**: Runs continuously, checking for new JSON files at regular intervals
- 🔄 **Overall Summary**: Maintains a single comprehensive summary of all processed content
- 🚫 **No Reprocessing**: Avoids processing the same files multiple times using file hashes
- 🧠 **Autonomous Analysis**: AI automatically determines optimal detail level based on content complexity
- ⏱️ **Real-time Processing**: Automatically processes new files as they appear

## Prerequisites

### 1. Install Ollama

First, install Ollama on your system:

**Windows:**
```bash
# Download from https://ollama.ai/download
# Or use winget
winget install Ollama.Ollama
```

**macOS:**
```bash
# Download from https://ollama.ai/download
# Or use Homebrew
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Start Ollama and Pull a Model

```bash
# Start Ollama service
ollama serve

# In another terminal, pull a model (llama2 is recommended)
ollama pull llama2
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Continuous Monitoring (Recommended)

```bash
# Start continuous monitoring (default: 30-second intervals)
python continuous_agent.py

# To stop the agent, press Ctrl+C in the terminal
```

This will:
- Monitor the specified directory for new JSON files
- Process new files automatically as they appear
- Maintain an overall summary of all processed content
- Avoid reprocessing the same files
- Save the overall summary to `overall_summary.json`

### Configuration

To customize the agent behavior, edit the configuration section in `continuous_agent.py`:

```python
# Configuration
MONITOR_DIR = "./video_summaries"      # Directory to monitor
OUTPUT_FILE = "overall_summary.json"   # Output file
OLLAMA_URL = "http://localhost:11434"  # Ollama server
MODEL = "deepseek-r1:8b"              # AI model to use
CHECK_INTERVAL = 30                   # Check interval in seconds
```

## Input JSON Format

The agent supports various JSON structures:

### Array of Video Objects (Recommended)
```json
[
  {
    "video_id": "vid_001",
    "title": "Video Title",
    "description": "Video description",
    "ai_summary": "AI-generated summary of the video content",
    "duration": "45:30",
    "metadata": {
      "category": "Education",
      "tags": ["tag1", "tag2"]
    }
  }
]
```

### Object with Videos Array
```json
{
  "videos": [
    {
      "ai_summary": "AI-generated summary"
    }
  ]
}
```

### Object with Summaries Array
```json
{
  "summaries": [
    "AI-generated summary 1",
    "AI-generated summary 2"
  ]
}
```

## Output Format

### Directory Monitoring Output

The directory monitor generates an overall summary with the following structure:

```json
{
  "total_videos": 15,
  "total_files": 3,
  "overall_ai_description": "Comprehensive AI-generated summary of all video content from multiple files...",
  "processed_files": [
    "/path/to/file1.json",
    "/path/to/file2.json",
    "/path/to/file3.json"
  ],
  "file_hashes": {
    "/path/to/file1.json": "abc123...",
    "/path/to/file2.json": "def456...",
    "/path/to/file3.json": "ghi789..."
  },
  "summary_metadata": {
    "model_used": "llama2",
    "last_updated": "2024-01-15 14:30:25",
    "monitor_directory": "./video_summaries"
  }
}
```

## Available Ollama Models

You can use any model available in Ollama. Popular options include:

- `llama2` - General purpose (recommended)
- `codellama` - Code-focused
- `mistral` - Fast and efficient
- `llama2:13b` - Larger model for better quality
- `llama2:7b` - Smaller, faster model

To see available models:
```bash
ollama list
```

To pull a new model:
```bash
ollama pull model_name
```

## Example Workflows

### Directory Monitoring

1. **Set up monitoring**: Create a directory for your JSON files
2. **Start Ollama**: Ensure Ollama is running with your preferred model
3. **Start monitoring**: Run the directory monitor agent
4. **Add files**: Drop JSON files into the monitored directory
5. **Watch updates**: The overall summary updates automatically

```bash
# Example workflow
ollama serve
ollama pull llama2
python video_summary_monitor.py --monitor-dir ./my_videos --watch

# In another terminal, add files to ./my_videos/ directory
# The agent will automatically process them and update the overall summary
```



## Troubleshooting

### Ollama Connection Issues

If you get connection errors:

1. **Check if Ollama is running**:
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Start Ollama service**:
   ```bash
   ollama serve
   ```

3. **Verify model is available**:
   ```bash
   ollama list
   ```

### JSON Format Issues

- Ensure your JSON file is valid (use a JSON validator)
- Check that at least one video has an `ai_summary` field
- The agent will try to extract summaries from `ai_summary`, `description`, or `title` fields

### Performance Tips

- Use smaller models (like `llama2:7b`) for faster processing
- For large datasets, consider processing in batches
- Ensure sufficient RAM for the chosen model

## Development

### Project Structure

```
custom_agent/
├── continuous_agent.py         # Main continuous monitoring agent
├── requirements.txt            # Python dependencies
├── overall_summary.json        # Generated overall summary
├── video_summaries/            # Directory to monitor for JSON files
└── README.md                  # This file
```

### Key Components

#### Continuous Agent
- **ContinuousVideoAgent**: Main continuous monitoring class
- **OllamaClient**: Handles communication with Ollama API
- **OverallSummary**: Data model for overall consolidated summary
- **VideoSummary**: Data model for individual video summaries
- **File hash tracking**: Prevents reprocessing of same files
- **Signal handling**: Graceful shutdown with Ctrl+C support

### Extending the Agent

You can extend the agent by:

1. **Adding new JSON formats**: Modify the `load_json_file` method in `ContinuousVideoAgent`
2. **Customizing prompts**: Edit the `_create_summary_prompt` method in `OllamaClient`
3. **Adding new models**: The agent supports any Ollama model
4. **Enhancing output**: Modify the `OverallSummary` model
5. **Changing configuration**: Edit the configuration section in the `main()` function

## License

This project is open source and uses only open-source components:

- **Ollama**: Apache 2.0 License
- **Python Libraries**: Various open-source licenses
- **This Agent**: MIT License

## Contributing

Feel free to contribute by:

1. Reporting issues
2. Suggesting new features
3. Improving documentation
4. Adding new JSON format support

## Support

For issues and questions:

1. Check the troubleshooting section
2. Verify Ollama is running correctly
3. Ensure your JSON format is valid
4. Check that you have sufficient system resources

---

**Happy summarizing! 🎬📝🤖** 
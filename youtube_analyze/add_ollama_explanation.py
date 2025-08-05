#!/usr/bin/env python3
"""
Add Ollama explanation to the notebook
"""

import json

def add_ollama_explanation():
    """Add explanation about OpenAI import with Ollama"""
    
    # Read the notebook
    with open('1_foundations/1_lab1_ollama.ipynb', 'r', encoding='utf-8') as f:
        notebook_data = json.load(f)
    
    # Create explanation cell
    explanation_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🔧 **Important: Why We Still Use `from openai import OpenAI`**\n",
            "\n",
            "You might be wondering why we're still importing from `openai` when using Ollama. Here's why:\n",
            "\n",
            "### **Ollama Provides OpenAI-Compatible API**\n",
            "- Ollama runs a local server that **mimics the OpenAI API format**\n",
            "- This means we can use the **same Python code** with local models\n",
            "- No need to learn a different library or API format\n",
            "\n",
            "### **How It Works**\n",
            "```python\n",
            "# Instead of this (OpenAI):\n",
            "openai = OpenAI()  # Connects to OpenAI servers\n",
            "\n",
            "# We use this (Ollama):\n",
            "openai = OpenAI(\n",
            "    base_url=\"http://localhost:11434/v1\",  # Local Ollama server\n",
            "    api_key=\"ollama\"  # Any string works\n",
            ")\n",
            "```\n",
            "\n",
            "### **Benefits**\n",
            "- ✅ **Same code** works with both OpenAI and Ollama\n",
            "- ✅ **No API costs** when using Ollama\n",
            "- ✅ **Complete privacy** - data stays on your machine\n",
            "- ✅ **Works offline** - no internet required\n",
            "\n",
            "---\n"
        ]
    }
    
    # Insert after the title cell (first cell)
    notebook_data['cells'].insert(1, explanation_cell)
    
    # Write back the notebook
    with open('1_foundations/1_lab1_ollama.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook_data, f, indent=1, ensure_ascii=False)
    
    print("✅ Ollama explanation added successfully!")

if __name__ == "__main__":
    add_ollama_explanation() 
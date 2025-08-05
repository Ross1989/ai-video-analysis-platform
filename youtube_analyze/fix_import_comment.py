#!/usr/bin/env python3
"""
Fix the import comment in the Ollama notebook
"""

import json

def fix_import_comment():
    """Update the import comment to clarify Ollama usage"""
    
    # Read the notebook
    with open('1_foundations/1_lab1_ollama.ipynb', 'r', encoding='utf-8') as f:
        notebook_data = json.load(f)
    
    # Find and update the import cell
    for cell in notebook_data['cells']:
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if 'from openai import OpenAI' in source and 'all important import statement' in source:
                # Update the comments
                cell['source'] = [
                    "# And now - the all important import statement\n",
                    "# We still use the OpenAI import because Ollama provides an OpenAI-compatible API\n",
                    "# This allows us to use the same code with local models!\n",
                    "\n",
                    "from openai import OpenAI\n"
                ]
                break
    
    # Write back the notebook
    with open('1_foundations/1_lab1_ollama.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook_data, f, indent=1, ensure_ascii=False)
    
    print("✅ Import comment updated successfully!")

if __name__ == "__main__":
    fix_import_comment() 
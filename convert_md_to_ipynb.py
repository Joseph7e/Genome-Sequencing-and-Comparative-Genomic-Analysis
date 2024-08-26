#! /usr/bin/env python3

import nbformat as nbf
import sys
import re

def md_to_ipynb_with_bash(md_file, ipynb_file):
    # Read the Markdown file
    with open(md_file, 'r') as f:
        md_content = f.read()

    # Create a new Jupyter Notebook
    nb = nbf.v4.new_notebook()

    # Split the content into cells based on ``` (bash code) blocks
    # Find all sections with ``` and separate them into Markdown and Code cells
    parts = re.split(r'(```.*?```)', md_content, flags=re.DOTALL)

    for part in parts:
        if part.startswith("```") and part.endswith("```"):
            # It's a code block, get the content and remove the surrounding ```
            code_content = re.sub("bash", "%%bash", part.strip('```').strip())
            # Create a new code cell (bash)
            code_cell = nbf.v4.new_code_cell(code_content, metadata={"language": "bash"})
            nb['cells'].append(code_cell)
        else:
            # It's a markdown content, create a new markdown cell
            md_cell = nbf.v4.new_markdown_cell(part)
            nb['cells'].append(md_cell)

    # Write the notebook to a file
    with open(ipynb_file, 'w') as f:
        nbf.write(nb, f)

# Example usage
md_to_ipynb_with_bash(sys.argv[1], sys.argv[2])

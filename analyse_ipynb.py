#%%
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def lemmatise_text(text):
    pass
    

def analyse_ipynb(file: str) -> dict[str]:
    """Analyses an ipynb file and gives back a dictionary of all of the values of interest
    
    Args:
        file (str): The file to analyse

    Returns:
        dict[str]: A dictionary with the values of interest
    """
    

    # Check if the file exists
    if not Path(file).is_file():
        print(f"File {file} does not exist", file=sys.stderr)
        sys.exit(1)

    # Check if the file is an ipynb file
    if not re.match(r"^.*\.ipynb$", file):
        print(f"File {file} is not an ipynb file", file=sys.stderr)
        sys.exit(1)

    # Read the file
    with open(file, "r") as f:
        data = json.load(f)

    # Get the name of the notebook
    name = os.path.basename(file)
    name = re.sub(r"\.ipynb$", "", name)

    # Get the date of the notebook
    kernelspec_name = data["metadata"]["kernelspec"]["display_name"]
    language_info = data["metadata"]["language_info"]
    language = language_info["name"]
    version = language_info["version"]
    # Get the number of cells
    num_cells = len(data["cells"])

    # Get the number of markdown cells
    num_markdown_cells = 0
    all_text = ""

    # Get the number of code cells
    num_code_cells = 0
    imports = []
    for cell in data["cells"]:
        if cell["cell_type"] == "code":
            num_code_cells += 1
            for line in cell["source"]:
                line = line.replace("\n", "")
                if "import" in line:
                    this_import = line.split(' ')[1]
                    if '.' in this_import:
                        this_import = this_import.split('.')[0]
                    imports.append(this_import) # add the import
        elif cell["cell_type"] == "markdown":
            num_markdown_cells += 1
            all_text += ' ' + ' '.join(cell["source"])

    all_text = all_text.replace("#", "").replace("-","").replace("\n", "")
    output = {
        "name": name,
        "kernel": kernelspec_name,
        "language": language,
        "version": version,
        "num_cells": num_cells,
        "num_markdown_cells": num_markdown_cells,
        "num_code_cells": num_code_cells,
        "imports": imports,
        "all_text": all_text,
    }
    return output

# %%

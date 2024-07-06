#!/usr/bin/env python3
"""This script reads a notebook and add new markdown cell at the top containing a
link to the original notebook on Github."""
import argparse
from pathlib import Path

import nbformat as nbf

# Parse arguments
parser = argparse.ArgumentParser(description='Add header to notebook example')

parser.add_argument('--source', action="store", dest='source')
parser.add_argument('--dest', action="store", dest='destination')

args = parser.parse_args()

notebook_path = Path(args.destination)

# read notebook
nb = nbf.read(notebook_path, as_version=4)

# generate header
text = (
    f"<p>\n"
    f"   <a href=\"{args.source}\"\n"
    f"       style=\"display: inline-flex; align-items: center;\">\n"
    f"       <img src='https://raw.githubusercontent.com/CAREamics/careamics.github.io/3bca810be17b0693503615673418d264d1962dac/docs/overrides/.icons/octicons/mark-github.svg'\n"
    f"           style=\"margin-right: 8px;\">\n"
    f"       <b>Find me on Github</b>\n"
    f"   </a>\n"
    f"</p>"
)

# add cell and save notebook
nb.cells = [nbf.v4.new_markdown_cell(text)] + nb.cells
nbf.write(nb, notebook_path)
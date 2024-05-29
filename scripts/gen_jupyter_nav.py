"""Generate navigation items for the jupyter notebooks.

The script runs in the root folder, but the relative paths need be built
relative to the applications folder. Each call to "mkdocs_gen_files" is
relative to the docs folder.

We want to produce a SUMMARY.md file that looks like the following:
* [Applications](index.md)
* N2V
    * [2D SEM](N2V/2D_SEM.ipynb)
    * [3D SEM](N2V/3D_SEM.ipynb)
* CARE
    * [2D SEM](CARE/2D_SEM.ipynb)
etc.

References:
https://oprypin.github.io/mkdocs-gen-files/
https://oprypin.github.io/mkdocs-literate-nav/reference.html#nav-list-syntax
https://mkdocstrings.github.io/recipes/
"""
from pathlib import Path

import mkdocs_gen_files

def index_text():
    return "---\n" \
            "icon: octicons/file-media-24\n" \
            "description: Applications\n" \
            "---\n" \
            "# Applications\n" \
            "This section contains a list of example applications. These pages were " \
            "automatically generated from the notebooks in [careamics-example](https://github.com/CAREamics/careamics-examples/tree/main/applications)\n\n"

# source folder
APP = Path("docs", "applications")

# create mkdocs navigation
nav = mkdocs_gen_files.Nav()

# create index file (relative to docs because we are calling mkdocs_gen_files)
with mkdocs_gen_files.open(Path("applications", "index.md"), "w") as index_md:
    index_md.write(index_text())
nav[("Applications",)] = "index.md"

# loop over all files, detect *.ipynb files and add them to the nav
for path in APP.rglob("*.ipynb"):
    print(path)

    # get path
    relative_path = path.relative_to(APP)

    # get parts
    parts = tuple(relative_path.parts)

    # name without underscores
    name = relative_path.stem.replace("_", " ")

    # replace the last part with the name
    parts = parts[:-1] + (name,)

    # add to navigation
    nav[parts] = relative_path.as_posix()

# write the navigation as a Markdown list in the literate navigation file
with mkdocs_gen_files.open("applications/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())

# read content of the SUMMARY.md file line by line, ommitting the first line
with mkdocs_gen_files.open("applications/SUMMARY.md", "r") as nav_file:
    lines = nav_file.readlines()[1:]

    for i, line in enumerate(lines):
        # change lines that start with a * to a markdown title
        if line.startswith("*"):
            lines[i] = f"## {line[2:]}\n"
        # remove tab in the others
        elif line.startswith("    "):
            lines[i] = line[4:]

    # write the lines into index.md
    with mkdocs_gen_files.open("applications/index.md", "a") as index_md:
        index_md.writelines(lines)
    

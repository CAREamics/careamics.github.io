"""Generate navigation items for the applications jupyter notebooks.

It scans each notebook in the applications folder and generates a SUMMARY.md
(for the navigation) and an index.md (for nice looking cards).

The script runs in the root folder, but the relative paths need to be built
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

And an index.md with cards for each application, based on notebooks.json.

References:
https://oprypin.github.io/mkdocs-gen-files/
https://oprypin.github.io/mkdocs-literate-nav/reference.html#nav-list-syntax
https://mkdocstrings.github.io/recipes/
"""
from pathlib import Path
import json
from dataclasses import dataclass

import mkdocs_gen_files

def index_text() -> str:
    """Return the introduction text to the index.md page"""
    return (
        "---\n" 
        "icon: octicons/file-media-24\n" 
        "description: Applications\n" 
        "---\n" 
        "# Applications\n" 
        "This page contains a list of examples on how to use CAREamics on real-world "
        "data or synthetic data. The examples are grouped by algorithm. "
        "Every example was generated from a Jupyter notebook, which is linked at the top "
        "of each page.\n"
    )

def bottom_text() -> str:
    """Return the bottom text of the index.md page"""
    return (
        "To add notebooks to this section, refer to "
        "[the guide](../guides/dev_resources/website.md#jupyter-notebook-applications)."
    )

def open_section(title: str) -> str:
    """Open the tags of a new card grid section."""
    return (
        f"## {title}\n"
        f"<div class=\"md-container secondary-section\">\n"
        f"  <div class=\"g\">\n"
        f"      <div class=\"section\">\n"
        f"          <div class=\"component-wrapper\" style=\"display: block;\">\n"
    )

def close_section() -> str:
    """Close the tags of a card grid section."""
    return (
        "          </div>\n"
        "      </div>\n"
        "  </div>\n"
        "</div>\n"
    )

def open_row() -> str:
    """Open the tags of a new row of cards."""
    return (
        "               <div class=\"responsive-grid\">\n"
    )

def close_row() -> str:
    """Close the tags of a row of cards."""
    return (
        "               </div>\n"
    )

def add_card(title: str, description: str, link: str, cover: str) -> str:
    """Return the html code for a card.
    
    Parameters
    ----------
    title : str
        Title of the card.
    description : str
        Description of the card.
    link : str
        Relative path to the notebook.
    cover : str
        Cover name.
    """
    return (
        f"              <a class=\"card-wrapper\" href=\"{link}\">\n"
        f"                  <div class=\"card\">\n"
        f"                      <div class=\"cover\">\n"
        f"                          <img src=\"{cover}\">\n"
        f"                      </div>\n"
        f"                      <div class=\"card-content\">\n"
        f"                          <h5>{title}</h5>\n"
        f"                          <p>\n"
        f"                              {description}\n"
        f"                          </p>\n"
        f"                      </div>\n"
        f"                  </div>\n"
        f"              </a>\n"
    )

@dataclass
class Card:
    page_title: str
    card: str


###########################
## Build navigation file ##
###########################

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


##########################
## Build the index file ##
##########################

# load notebooks.json
with open("scripts/notebooks.json", "r") as f:
    notebooks = json.load(f)

# group notebooks by application
n_notebooks = 0
applications = {}
for notebook in notebooks["applications"]:
    
    # get details
    name = notebook["name"]
    title = notebook["destination"]
    description = notebook["description"]
    cover = "../assets/notebook_covers/" + notebook["cover"]

    friendly_title = title.replace("_", " ")
    friendly_name = name.replace("_", " ")
    link = title + "/" + name

    if title not in applications:
        applications[title] = []

    # add card
    applications[title].append(
        Card(
            page_title=friendly_title,
            card=add_card(friendly_name, description, link, cover)
        )
    )

# build index.md
with mkdocs_gen_files.open("applications/index.md", "a") as index_md:

    # loop over applications
    for title, cards in applications.items():
        # open section
        index_md.write(open_section(cards[0].page_title))

        # write rows
        count = 0
        for card in cards:

            if count % 2 == 0:
                index_md.write(open_row())
                index_md.write(card.card)
            else:
                index_md.write(card.card)
                index_md.write(close_row())

            count += 1

        if count % 2 != 0:
            index_md.write(close_row())

        index_md.write(close_section())
    
    # add bottom text
    index_md.write(bottom_text())

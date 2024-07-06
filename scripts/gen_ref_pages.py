"""Generate the code reference pages and navigation.

adapted from: https://mkdocstrings.github.io/recipes/
"""
from pathlib import Path

import mkdocs_gen_files


def format_name(module_name: str):
    module_name = module_name.replace("_", " ")
    module_name = module_name.replace("careamics", "CAREamics")
    return module_name

def format_name_no_space(module_name: str):
    module_name = module_name.replace("_", "-")
    module_name = module_name.replace("careamics", "CAREamics")
    return module_name

def project_index_text(module_name):
    """Text in the index of each project."""
    return f"# {format_name(module_name)} \n" \
            f"Use the navigation index on the left to explore the documentation." \


def main_index_text():
    index_text = "---\n" \
                "icon: octicons/code-24 \n" \
                "description: Code documentation \n" \
                "--- \n" \
                "# Code Reference\n\n"
    return index_text


def open_card_block():
    return "<div class=\"md-container secondary-section\">" \
            "<div class=\"g\">" \
                "<div class=\"section\">" \
                    "<div class=\"component-wrapper\" style=\"display: block;\">"


def close_card_block():
    return "</div></div></div></div>"

def open_row():
    return "<div class=\"responsive-grid\">"

def close_row():
    return "</div>\n"

def new_card(module_name):
    return (
        f"<a class=\"card-wrapper\" href=\"{module_name}\">"
        f"<div class=\"card\">\n" 
        f"<div class=\"card-body\">\n" 
        f"<div class=\"logo\">\n" 
        f"<span class=\"twemoji\">" 
        f"<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" width=\"24\" height=\"24\"><path d=\"M15.22 4.97a.75.75 0 0 1 1.06 0l6.5 6.5a.75.75 0 0 1 0 1.06l-6.5 6.5a.749.749 0 0 1-1.275-.326.749.749 0 0 1 .215-.734L21.19 12l-5.97-5.97a.75.75 0 0 1 0-1.06Zm-6.44 0a.75.75 0 0 1 0 1.06L2.81 12l5.97 5.97a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215l-6.5-6.5a.75.75 0 0 1 0-1.06l6.5-6.5a.75.75 0 0 1 1.06 0Z\"></path></svg>"
        f"</span>" 
        f"</div>" 
        f"<div class=\"card-content\">" 
        f"<h5>{format_name(module_name)}</h5>" 
        f"</div>" 
        f"</div>" 
        f"</div></a>"
    )

# create mkdocs navigation
nav = mkdocs_gen_files.Nav()

# add index page to the navigation 
modules_index = Path("index.md")
nav[tuple(modules_index.parts)] = modules_index.as_posix()

# create source folder relative to this script
src = Path(__file__).parent.parent / "src" 

# iterate over packages (directories in src/)
module_list = []
if src.exists():
    for path in sorted(src.iterdir()):

        # if it is a python module
        if Path(path, "__init__.py").exists():
            # add to list
            module_list.append(path.name)

            # set up relative path to its own module index
            # e.g. careamics/index.md
            module_path = Path(path.name, "index.md")

            # add to navigation
            # e.g. ["careamic"]= careamics/index.md
            nav[tuple(module_path.parts)] = module_path.as_posix()

            # create module index
            # e.g. careamics/index.md
            with mkdocs_gen_files.open(Path("reference", module_path), "w") as md_file:
                md_file.write(project_index_text(path.name))

    # write a card for each package in the main reference index
    with mkdocs_gen_files.open(Path("reference", "index.md"), "w") as index_md:
        index_md.write(main_index_text())

        index_md.write(open_card_block())
        for i, name in enumerate(module_list):
            if i%2 == 0:
                index_md.write(open_row())
                index_md.write(new_card(name))
            else:
                index_md.write(new_card(name))
                index_md.write(close_row())
            
        index_md.write(close_card_block())

    # build docstring references
    for path in sorted(Path("src").rglob("*.py")):
        if path.name != "__init__.py":
            # set up paths
            module_path = path.relative_to("src").with_suffix("")
            doc_path = path.relative_to("src").with_suffix(".md")
            full_doc_path = Path("reference", doc_path)

            # folder structure of the python module
            parts = tuple(module_path.parts)

            # remove __init__.py
            if parts[-1] == "__init__":
                parts = parts[:-1]
                doc_path = doc_path.with_name("index.md")
                full_doc_path = full_doc_path.with_name("index.md")
            elif parts[-1] == "__main__":
                continue

            # progressively build the navigation index
            nav[parts] = doc_path.as_posix()

            # add doc to mkdocs
            with mkdocs_gen_files.open(full_doc_path, "w") as fd:
                ident = ".".join(parts)
                fd.write(f"::: {ident}")

            # set the edit_uri on the pages
            mkdocs_gen_files.set_edit_path(full_doc_path, path)

    # Write the navigation as a Markdown list in the literate navigation file
    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
        nav_file.writelines(nav.build_literate_nav())

# Website

The website is built using [mkdocs](https://www.mkdocs.org/), more specifically the 
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme. Modifications to
the theme were greatly inspired from [pydev-guide](https://github.com/pydev-guide/pydev-guide.github.io).

In this page, we describe some of the technical details on how to maintain this website.

## Environement

The `requirements.txt` file contains all the packages used to generate this website.

### Build the pages locally

In order to build the pages locally, follow these steps:

1. Fork this repository and clone it.
2. Create a new environment and install the dependencies:
    ```bash
    conda create -n careamics-docs python=3.11
    pip install -r requirements.txt
    ```
4. Run the following scripts (which are normally run by the CI):
    ```bash
    python scripts/check_out_repos.sh
    python scripts/check_out_notebooks.sh
    ```
3. Build the pages:
    ```bash
    mkdocs serve
    ```
4. Open the local link in your browser.

**Note**: This will not show you the version mechanism. For this, check out the 
**Version release** section.


## Code snippets

Code snippets are all automatically tested in [careamics-example](https://github.com/CAREamics/careamics-examples/tree/main/applications)
and are currently manually added to the markdown pages in the guides.


## Jupyter notebooks applications

The pages in the application section are automatically generated from the Jupyter
notebooks in [careamics-example](https://github.com/CAREamics/careamics-examples/tree/main/applications) 
using [mkdocs-jupyter](https://github.com/danielfrg/mkdocs-jupyter).
A bash script (`scripts/check_out_notebooks.sh`) checks out the repository and copies 
all the notebooks referenced in a text files into the correct path in the application 
folder. Finally, the script `scripts/gen_jupyter_nav.py` creates entries for each notebook 
in the navigation file of mkdocs.


### Adding a new notebook

1. Add the notebook to `scripts/notebooks.csv`, without using spaces. The third column
  specifies the path to the page in the application section, while the last column is used 
  as title.
2. You can test the notebook by running `sh scripts/notebooks.sh` then `mkdocs serve`.


!!! info title="Cell tags"

    By default, all cell outputs are shown. To hide the output of a particular cell,
    add the tag `remove_output` to the cell. The `mkdocs.ynml` specifies that this 
    tag is used to hide cell outputs.


!!! info title="CSV ending on a new line"

    In is important to end the `.csv` file with a new line, otherwise the last line might
    be ignored.

## Code reference

The code reference is generated using [mkdocstrings](https://mkdocstrings.github.io/), 
the script `scripts/checkout_repos.sh` and the page building script `scripts/gen_ref_pages.py`. 
To include a new package, simply add it to the `scripts/git_repositories.txt` file.

```
https://github.com/CAREamics/careamics
https://github.com/CAREamics/careamics-portfolio
<new project here>
```

## Updating the website version


In principle, when a new release of CAREamics is made, the state of the documentation
is saved into the corresponding version, and the documentation is tagged with the
next (ongoing) version.

For instance, the documentation is showing version `0.4`, upon release of verson 
`0.4`, the state of the documentation is saved. The latest documentation is then 
tagged with version `0.5` (the next version) until this one is released.

In order to keep track of versions, we use [mike](https://github.com/jimporter/mike). 
We apply the following procedure:

1. Release version MAJOR.MINOR of CAREamics
2. Tag the latest documentation with version MAJOR.(MINOR+1)
  ```bash
  git tag MAJOR.(MINOR+1)
  git push --tags
  ```

To visualize the pages with the versions, you can use:

```bash
mike serve
```

### Correcting a version error

All the versions are stored in the `gh-pages` branch. If you made a mistake in the version
tagging, you can correct it by deleting the tag and pushing the changes.

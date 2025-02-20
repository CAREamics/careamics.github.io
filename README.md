<p align="center">
  <a href="https://careamics.github.io/">
    <img src="https://github.com/CAREamics/.github/blob/main/profile/images/banner_careamics.png">
  </a>
</p>

[![Build](https://github.com/CAREamics/careamics.github.io/actions/workflows/deploy-pages.yml/badge.svg)](https://github.com/CAREamics/careamics.github.io/actions/workflows/deploy-pages.yml)
[![Deployment](https://github.com/CAREamics/careamics.github.io/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/CAREamics/careamics.github.io/actions/workflows/pages/pages-build-deployment)

# Welcome to CAREamics docs

This repository contains the source code for the [CAREamics](https://github.com/CAREamics/careamics) documentation website. The 
website is built using [MkDocs](https://www.mkdocs.org/) and the 
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme, with a few
modifications to the theme inherited from 
the [PyDev Guide project](https://github.com/pydev-guide/pydev-guide.github.io).

Beside the static pages, the website automatically checks out repositories listed in
[git_repositories.txt](scripts/git_repositories.txt) and generates documentation for
the corresponding projects, all thanks to [mkdocstring](https://mkdocstrings.github.io/)
, [mkdocs-gen-files](https://oprypin.github.io/mkdocs-gen-files/) and 
[mkdocs-literate-nav](https://oprypin.github.io/mkdocs-literate-nav/reference.html).
Similarly, it also uses [mkdocs-jupyter](https://pypi.org/project/mkdocs-jupyter/) to
add Jupyter notebooks to the documentation from the list in 
[notebooks.csv](scripts/notebooks.csv).

## How to build the pages locally

In order to build the pages locally, follow these steps:

1. Fork this repository and clone it.
2. Create a new environment and install the dependencies:
    ```bash
    conda create -n careamics-docs python=3.11
    conda activate careamics-docs
    pip install -r requirements.txt
    ```
4. Run the following scripts (which are normally run by the CI):
    ```bash
    sh scripts/check_out_repos.sh
    sh scripts/check_out_examples.sh
    ```
3. Build the pages:
    ```bash
    mkdocs serve
    ```
4. Open the local link in your browser.

**Note**: This will not show you the version mechanism. For this, check out the 
**Version release** section.

## How to add a new project to the documentation

In order to add a new project to the documentation, simply edit 
[git_repositories.txt](scripts/git_repositories.txt):

```
https://github.com/CAREamics/careamics
https://github.com/CAREamics/careamics-portfolio
<new project here>
```

## How to add a new notebook to the documentation

In order to add a new notebook to the documentation, simply edit
[notebooks.csv](scripts/notebooks.csv):

```
repository url, path in repository, destination in docs, title
https://github.com/CAREamics/careamics.git,examples/2D/example_SEM.ipynb,N2V,2D_SEM
<reference repository>,<relative path to the notebook>,<destination in applications>,<title>
<new line>
```

Add the new notebook data in place of the chevrons.

The script clones the repository, copy the notebook to the relative destination (with
respect to `docs/applications`) and change the name of the notebook. The name of the 
notebook will be used as title in the documentation navigation sidebar (with 
underscores replaced by spaces).

In is important to end the `.csv` file with a new line.

## How to update the pages without any commit

This can be useful when one of the project has changed and we need to update the API
doc. In such a case, click on the `Deploy to GitHub Pages` in the `Actions` tab, and
run the workflow.

## Version release

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
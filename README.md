<p align="center">
  <a href="https://careamics.github.io/">
    <img src="https://github.com/CAREamics/.github/blob/main/profile/images/banner_careamics.png">
  </a>
</p>

[![Build](https://github.com/CAREamics/careamics.github.io/actions/workflows/docs.yml/badge.svg)](https://github.com/CAREamics/careamics.github.io/actions/workflows/docs.yml)
[![Deployment](https://github.com/CAREamics/careamics.github.io/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/CAREamics/careamics.github.io/actions/workflows/pages/pages-build-deployment)

# Welcome to CAREamics docs

This repository contains the source code for the [CAREamics](https://github.com/CAREamics/careamics) documentation website. The 
website is built using [Zensical](https://zensical.org/).


## Website automation

At build time, the CI runs a script to copy the latest stable release of [CAREamics](https://github.com/CAREamics/careamics) into a local folder. From there on, it extracts the version number and generates the API reference pages. Finally, it edits `zensical.toml` with the navigation page.

Two scripts are called for this purpose:
- `pull_from_repos.sh` handles the cloning/updating of the repositories, copying the relevant files, and updating `zensical.toml` with the navigation entries corresponding to the guides. It also creates a symlink to a local version of the repo if the `--local` option is used (see below), and version files used to indicate for which version the website is currently built and record new versions with `mike` in the CI.
- `gen_ref_pages.py` generates the API reference pages based on the copied files and updates `zensical.toml` with the navigation entries corresponding to the API reference.

> [!NOTE]
> Currently, unless using a local repo, the latest stable release of careamics is used to build the website. In the near future, we could use the `--dev` option together with a new CI to build a "dev" version of the website based on the main branch instead.



## How to build the pages locally

In order to build the pages locally, follow these steps:

1. Fork this repository and clone it.
2. Create a new environment and install the dependencies:
    ```bash
    uv sync
    ```
3. Run the script to get the latest release of CAREamics:
    ```bash
    bash scripts/pull_from_repos.sh --write
    ```

    `--write` indicates that the `zensical.toml` will be updated.
4. Generate the reference pages:
    ```bash
    uv run python scripts/gen_ref_pages.py --write
    ```
3. Build the pages:
    ```bash
    zensical serve
    ```
4. Open the local link in your browser.

**Note**: This will not show you the versioning mechanism.

## Working with a local version of CAREamics

In step 3, use instead:

```bash
bash scripts/pull_from_repos.sh  --write --local /path/to/local/careamics
```

## How to update the pages without any commit

This can be useful when one of the project has changed and we need to update the API
doc. In such a case, use the dispatch workflow option of the CI (maintainers only).

## Version release

The version release process is automated using `mike` in the CI. Upon pushing a new tag,
the CI will build the documentation for that version the next time it is triggered.
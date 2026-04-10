#!/usr/bin/env bash
# Usage: pull_from_repos.sh [OPTIONS]
#
# Pull documentation and source files from remote repositories into the website.
#
# Options:
#   --dev          Stay on the main branch instead of checking out the latest
#                  stable release tag (skips checkout_stable_release).
#   --local <path> Use a local repository at <path> instead of cloning/updating
#                  from the remote. Skips all git clone/pull and tag-checkout
#                  steps; version extraction and file copy still run normally.
#
# Examples:
#   pull_from_repos.sh                        # release mode (stable tag)
#   pull_from_repos.sh --dev                  # dev mode (main branch)
#   pull_from_repos.sh --local ~/code/careamics  # local repo
set -euo pipefail # fail fast

# -- Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
FROM_GIT_DIR="$ROOT_DIR/from_git"
GUIDES_DIR="$ROOT_DIR/docs/content/guides"
CAREAMICS_REPO_DIR="$FROM_GIT_DIR/careamics"

# Add repositories here (one per line)
REPOS=(
  "https://github.com/CAREamics/careamics.git"
)

# -- Helpers

# extract the repo name from a git URL (necessary for pulling if it exists)
repo_name_from_url() {
  basename "$1" .git
}

# clone or update a repository
clone_or_update_repo() {
  local url="$1"
  local name
  name="$(repo_name_from_url "$url")"
  local dest="$FROM_GIT_DIR/$name"

  if [[ -d "$dest/.git" ]]; then
    echo "Updating '$name' ..."
    git -C "$dest" checkout main
    git -C "$dest" pull --ff-only
  else
    echo "Cloning '$name' ..."
    git clone "$url" "$dest"
  fi
}

# checkout the latest stable tag in the careamics repo so the source code
# matches the released version (used for API reference generation).
# Skipped in --dev mode to stay on main.
checkout_stable_release() {
  local repo_dir="$CAREAMICS_REPO_DIR"

  if [[ ! -d "$repo_dir/.git" ]]; then
    echo "Error: $repo_dir is not a git repo, skipping checkout."
    return 1
  fi

  local tag
  tag="$(git -C "$repo_dir" tag --list 'v[0-9]*' --sort=-v:refname | grep -v -E '(rc|alpha|beta|dev)' | head -1 || true)"

  if [[ -z "$tag" ]]; then
    echo "Warning: no stable git tag found in $repo_dir, skipping checkout."
    return 1
  fi

  echo "Checking out $tag in $repo_dir"
  git -C "$repo_dir" checkout "$tag"
}

# extract the current version from the repo (latest stable tag) and write it
# to docs/extras/version.txt and docs/extras/version.md
extract_version() {
  local repo_dir="$CAREAMICS_REPO_DIR"
  local version_file="$ROOT_DIR/docs/extras/version.txt"

  if [[ ! -d "$repo_dir/.git" ]]; then
    echo "Error: $repo_dir is not a git repo, skipping version extraction."
    return 1
  fi

  # hatch-vcs uses git tags; grab the latest stable one (e.g. v0.1.0)
  # Skip pre-release tags (rc, alpha, beta, dev)
  local tag
  tag="$(git -C "$repo_dir" tag --list 'v[0-9]*' --sort=-v:refname | grep -v -E '(rc|alpha|beta|dev)' | head -1 || true)"

  if [[ -z "$tag" ]]; then
    echo "Warning: no stable git tag found in $repo_dir, skipping version extraction."
    return 1
  fi

  echo "Writing version $tag to $version_file"
  mkdir -p "$(dirname "$version_file")"
  echo "$tag" > "$version_file"

  # Also generate version.md with a full markdown link
  local version_md="$ROOT_DIR/docs/extras/version.md"
  echo "Documentation for version [$tag](https://github.com/CAREamics/careamics/releases/tag/$tag)." > "$version_md"
  echo "Writing version link to $version_md"
}

# copy docs from careamics/docs:
#   .md  -> docs/content/guides  (preserving relative paths)
#   .py  -> docs/snippets        (preserving relative paths)
copy_careamics_docs_v2() {
  local src="$CAREAMICS_REPO_DIR/docs"
  local snippets_dir="$ROOT_DIR/docs/snippets"

  if [[ ! -d "$src" ]]; then
    echo "Error: $src not found, skipping copy."
    return 1
  fi

  # Copy .md files to docs/content/guides
  echo "Copying .md files to $GUIDES_DIR ..."
  mkdir -p "$GUIDES_DIR"
  (cd "$src" && find . -name '*.md' -print0 | while IFS= read -r -d '' f; do
    mkdir -p "$GUIDES_DIR/$(dirname "$f")"
    cp "$f" "$GUIDES_DIR/$f"
  done)

  # Copy .py files to docs/snippets
  echo "Copying .py files to $snippets_dir ..."
  mkdir -p "$snippets_dir"
  (cd "$src" && find . -name '*.py' -print0 | while IFS= read -r -d '' f; do
    mkdir -p "$snippets_dir/$(dirname "$f")"
    cp "$f" "$snippets_dir/$f"
  done)
}


# merge navigation entries from nav.toml (in the careamics docs) into
# zensical.toml, replacing empty list placeholders marked with
# "# filled by pull_from_repos.sh".
#
# nav.toml format: a valid TOML file with a top-level `nav` array whose
# elements are the same inline-table blocks used in zensical.toml, e.g.:
#   nav = [
#     {"Using CAREamics" = ["file.md", ...]},
#     {"Tutorials"       = [...]},
#   ]
merge_nav() {
  local nav_file="$CAREAMICS_REPO_DIR/docs/nav.toml"
  local zensical_file="$ROOT_DIR/zensical.toml"

  if [[ ! -f "$nav_file" ]]; then
    echo "Warning: $nav_file not found, skipping nav merge."
    return 0
  fi

  echo "Merging nav entries from $nav_file into zensical.toml ..."
  python3 "$SCRIPT_DIR/update_nav.py" --nav "$nav_file" --toml "$zensical_file" --write
}


# -- Main

main() {
  local dev_mode=false
  local local_path=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dev) dev_mode=true; shift ;;
      --local)
        [[ -n "${2:-}" ]] || { echo "Error: --local requires a path."; exit 1; }
        local_path="$(cd "$2" && pwd)"
        shift 2
        ;;
      *) echo "Unknown option: $1"; exit 1 ;;
    esac
  done

  mkdir -p "$FROM_GIT_DIR"

  if [[ -n "$local_path" ]]; then
    echo "Using local repo at '$local_path' ..."
    CAREAMICS_REPO_DIR="$local_path"
  else
    for url in "${REPOS[@]}"; do
      clone_or_update_repo "$url"
    done

    # in release mode, checkout the stable tag for API reference generation
    if [[ "$dev_mode" == false ]]; then
      checkout_stable_release
    fi
  fi

  # extract and write the version (always based on the latest stable tag)
  extract_version

  # copy docs from the same version as the exported one
  # (otherwise there will be a mismatch between docs and version)
  copy_careamics_docs_v2

  # merge nav.toml entries into zensical.toml
  merge_nav
}

main "$@"

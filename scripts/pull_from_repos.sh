#!/usr/bin/env bash
set -euo pipefail # fail fast

# -- Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
FROM_GIT_DIR="$ROOT_DIR/from_git"
GUIDES_DIR="$ROOT_DIR/docs/content/guides"

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

# copy docs from careamics/docs into docs/content/guides
copy_careamics_docs_v2() {
  local src="$FROM_GIT_DIR/careamics/docs"

  if [[ ! -d "$src" ]]; then
    echo "Error: $src not found, skipping copy."
    return 1
  fi

  echo "Copying careamics docs to $GUIDES_DIR ..."
  mkdir -p "$GUIDES_DIR"
  cp -R "$src"/. "$GUIDES_DIR"/
}

copy_careamics_docs_v1() {
  local src="$FROM_GIT_DIR/careamics/docs/v0.1"

  if [[ ! -d "$src" ]]; then
    echo "Error: $src not found, skipping copy."
    return 1
  fi

  echo "Copying careamics docs to $GUIDES_DIR ..."
  mkdir -p "$GUIDES_DIR"
  cp -R "$src"/. "$GUIDES_DIR"/
}


# write the careamics version (from its latest git tag) to docs/extras/version.txt
write_version() {
  local repo_dir="$FROM_GIT_DIR/careamics"
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

  # Checkout the stable tag so the source code matches the version label.
  # This ensures the API reference is built from the tagged release,
  # not from main (which may contain pre-release changes).
  echo "Checking out $tag in $repo_dir"
  git -C "$repo_dir" checkout "$tag"

  echo "Writing version $tag to $version_file"
  mkdir -p "$(dirname "$version_file")"
  echo "$tag" > "$version_file"

  # Also generate version.md with a full markdown link
  local version_md="$ROOT_DIR/docs/extras/version.md"
  echo "Documentation for version [$tag](https://github.com/CAREamics/careamics/releases/tag/$tag)." > "$version_md"
  echo "Writing version link to $version_md"
}

# -- Main

main() {
  mkdir -p "$FROM_GIT_DIR"

  for url in "${REPOS[@]}"; do
    clone_or_update_repo "$url"
  done

  # copy_careamics_docs_v2

  write_version
}

main "$@"

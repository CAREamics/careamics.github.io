#!/bin/bash

# This script clone the example repository, and copy some notebooks into
# the docs. The rest is kept for snippets.
#
# requires installing `jq`

# optional argument to specify a branch
if [ -z "$1" ]; then
    BRANCH="main"
else
    BRANCH="$1"
fi

JSON="scripts/notebooks.json"
DEST="docs/"
TEMP="temp/"
REPO="https://github.com/CAREamics/careamics-examples.git"
ALGO="algorithms"
APP="applications"

# create temporary repo folder
if [ ! -d "$TEMP" ]; then
    # If it doesn't exist, create it and its parent directories if needed
    mkdir -p "$TEMP"
fi

# clone the repo in temp
repository_name=$(echo $REPO | sed 's/.*\///' | sed 's/.git//')

if git clone -b $BRANCH $REPO "$TEMP$repository_name"; then
    echo "Cloned branch $BRANCH of $REPO to $TEMP$repository_name"
else
    echo "Cloning branch $BRANCH of $REPO failed, cloning main."
    git clone $REPO "$TEMP$repository_name"
fi


# Process all algorithms
echo "Copy algorithms"
count=$(jq ".${ALGO} | length" "$JSON")
for i in $(seq 0 $(($count - 1))); do
    path_in_repo=$(jq -r ".${ALGO}[$i].source" "$JSON")
    title=$(jq -r ".${ALGO}[$i].name" "$JSON")

    # extract notebook file name (including extension)
    notebook_name=$(echo $path_in_repo | sed 's/.*\///')

    # add ".ipynb" extension to the title
    title_ext="$title.ipynb"

    # source of the notebook
    source="$TEMP$repository_name/$path_in_repo"

    # copy the notebook to DEST
    NB_DEST="$DEST$ALGO/$title_ext"
    cp $source $NB_DEST
    echo "Copying from $source to $NB_DEST"

    if [ -f $NB_DEST ]; then
        echo "Copied $repository_name/$path_in_repo to $NB_DEST"
    else
        echo "Copying $repository_name/$path_in_repo/$notebook_name failed"
    fi
done

# Process all applications
echo "Copy applications"
count=$(jq ".${APP} | length" "$JSON")
for i in $(seq 0 $(($count - 1))); do
    path_in_repo=$(jq -r ".${APP}[$i].source" "$JSON")
    destination=$(jq -r ".${APP}[$i].destination" "$JSON")
    title=$(jq -r ".${APP}[$i].name" "$JSON")

    # extract notebook file name (including extension)
    notebook_name=$(echo $path_in_repo | sed 's/.*\///')

    # add ".ipynb" extension to the title
    title_ext="$title.ipynb"

    # create the destination folder if it doesn't exist
    directory="$DEST$APP/$destination"
    if [ ! -d "$directory" ]; then
        # If it doesn't exist, create it and its parent directories if needed
        mkdir -p "$directory"
    fi

    # source of the notebook
    source="$TEMP$repository_name/$path_in_repo"

    # copy the notebook to DEST
    NB_DEST="$DEST$APP/$destination/$title_ext"
    cp $source $NB_DEST
    echo "Copying from $source to $NB_DEST"

    if [ -f $NB_DEST ]; then
        echo "Copied $repository_name/$path_in_repo to $NB_DEST"

        # remove ".git" from the repository name
        REPO_STEM="${REPO%.git}"

        # link to notebook
        NB_LINK="$REPO_STEM/blob/main/$path_in_repo"

        # add header to the notebook
        echo $NB_LINK
        python "scripts/add_notebook_header.py" --source $NB_LINK --dest $NB_DEST
    else
        echo "Copying $repository_name/$path_in_repo/$notebook_name failed"
    fi
done

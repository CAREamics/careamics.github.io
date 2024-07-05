#!/bin/bash

# This python script clone the example repository, and copy some notebooks into
# the docs. The rest is kept for snippets.

# optional argument to specify a branch
if [ -z "$1" ]; then
    BRANCH="main"
else
    BRANCH="$1"
fi

LIST="scripts/notebooks.csv"
DEST="docs/"
TEMP="temp/"
REPO="https://github.com/CAREamics/careamics-examples.git"

# create repos folder
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

# loop over the list starting from lin 2, clone the repository and copy the notebook
tail -n +2 "$LIST" | while IFS=, read -r path_in_repo destination_in_docs title; do
    # extract notebook file name (including extension)
    notebook_name=$(echo $path_in_repo | sed 's/.*\///')

    # replace spaces in the title with underscores, and add ".ipynb" extension
    title=$(echo $title | sed 's/ /_/g')
    title_ext="$title.ipynb"

    # create the destination folder if it doesn't exist
    directory="$DEST$destination_in_docs"
    if [ ! -d "$directory" ]; then
        # If it doesn't exist, create it and its parent directories if needed
        mkdir -p "$directory"
    fi

    # source of the notebook
    source="$TEMP""$repository_name"/"$path_in_repo"

    # copy the notebook to DEST
    NB_DEST="$DEST$destination_in_docs/$title_ext"
    cp $source $NB_DEST

    # if the copy was successful, print new path and update notebook with header
    if [ -f $NB_DEST ]; then
        echo "Copied $repository_name/$path_in_repo to $NB_DEST"

        # if it was copied in the applications folder, update notebook
        if [[ $destination_in_docs == "applications"* ]]; then
            # remove ".git" from the repository name
            REPO_STEM="${REPO%.git}"

            # link to notebook
            NB_LINK="$REPO_STEM/blob/main/$path_in_repo"

            # add header to the notebook
            echo $NB_LINK
            python "scripts/add_notebook_header.py" --source $NB_LINK --dest $NB_DEST
        fi
    else
        echo "Copying $repository_name/$path_in_repo/$notebook_name failed"
    fi
done

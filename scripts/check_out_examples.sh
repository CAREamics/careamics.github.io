#!/bin/bash

# This python script clone the example repository, and copy some notebooks into
# the docs. The rest is kept for snippets.

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
git clone $REPO "$TEMP""$repository_name"

# loop over the list starting from lin 2, clone the repository and copy the notebook
tail -n +2 "$LIST" | while IFS=, read -r path_in_repo destination_in_docs title; do
    # extract notebook file name (including extension)
    notebook_name=$(echo $path_in_repo | sed 's/.*\///')

    # replace spaces in the title with underscores, and add ".ipynb" extension
    title=$(echo $title | sed 's/ /_/g')
    title_ext="$title"".ipynb"

    # create the destination folder if it doesn't exist
    directory="$DEST""$destination_in_docs"
    if [ ! -d "$directory" ]; then
        # If it doesn't exist, create it and its parent directories if needed
        mkdir -p "$directory"
    fi

    # source of the notebook
    source="$TEMP""$repository_name"/"$path_in_repo"

    # copy the notebook to DEST
    cp $source "$DEST""$destination_in_docs"/"$title_ext"

    # if the copy was successful, print new path
    if [ -f "$DEST""$destination_in_docs"/"$title_ext" ]; then
        echo "Copied $repository_name/$path_in_repo to $DEST$destination_in_docs"/"$title_ext"
    else
        echo "Copying $repository_name/$path_in_repo/$notebook_name failed"
    fi
done

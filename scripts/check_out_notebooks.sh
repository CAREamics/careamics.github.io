#!/bin/bash

# This python script is currently not used and kept as legacy for now.
exit 0

LIST="scripts/notebooks.csv"
DEST="docs/applications/"
REPOS="temp/"

# create repos folder
if [ ! -d "$REPOS" ]; then
    # If it doesn't exist, create it and its parent directories if needed
    mkdir -p "$REPOS"
fi

# loop over the list, clone the repository and copy the notebook
tail -n +2 "$LIST" | while IFS=, read -r repository_url path_in_repo destination_in_docs title; do
    # extract the name of the repository
    repository_name=$(echo $repository_url | sed 's/.*\///' | sed 's/.git//')
    echo $repository_name
    
    # clone the repository in REPOS
    git clone $repository_url "$REPOS""$repository_name"

    # extract notebook file name (including extension)
    notebook_name=$(echo $path_in_repo | sed 's/.*\///')

    # replace spaces in the title with underscores, and add ".ipynb" extension
    title=$(echo $title | sed 's/ /_/g')
    title_ext="$title"".ipynb"

    # crete the destination folder if it doesn't exist
    directory="$DEST""$destination_in_docs"
    if [ ! -d "$directory" ]; then
        # If it doesn't exist, create it and its parent directories if needed
        mkdir -p "$directory"
    fi

    # copy the notebook to DEST
    cp "$REPOS""$repository_name"/"$path_in_repo" "$DEST""$destination_in_docs"/"$title_ext"

    # if the copy was successful, print new path
    if [ -f "$DEST""$destination_in_docs"/"$title_ext" ]; then
        echo "Copied $repository_name/$path_in_repo to $DEST$destination_in_docs"/"$title_ext"
    else
        echo "Copying $repository_name/$path_in_repo/$notebook_name failed"
    fi
done

# delete repos folder if it exists
if [ -d "$REPOS" ]; then
    # If it exists, delete it
    rm -rf "$REPOS"
fi
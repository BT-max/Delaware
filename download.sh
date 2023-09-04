#!/bin/bash

# Create the downloads directory if it does not already exist
mkdir -p downloads

# Loop through each line in the urls.txt file
while read -r url; do
    # Extract the id from the url
    id=$(echo "$url" | sed -n 's/.*id=\([0-9]*\)/\1/p')

    # Download the file and save it with the id as the filename
    curl -o "downloads/${id}.pdf" "$url"
done < urls.txt

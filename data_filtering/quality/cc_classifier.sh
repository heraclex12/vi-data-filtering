#!/bin/bash

# Check if the data folder is given as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 data/"
  exit 1
fi

# Check if jq and zstd are installed
if ! command -v jq &> /dev/null; then
  echo "jq is not installed. Please install it first."
  exit 3
fi

if ! command -v zstd &> /dev/null; then
  echo "zstd is not installed. Please install it first."
  exit 4
fi


for file in "$1"/*.gz; do
  if [ -f "$file" ]; then
    # Get the base name of the input file without extension
    base_name=${file%.gz}

    # Create a temporary file for filtered output
    temp_file=$(mktemp)

    # Filter out the entries with wiki_prob < 0.25 using jq
    gunzip -c "$file" | jq -c 'select(.wiki_prob >= 0.25)' > "$temp_file"

    # Compress the output file using zstd with .jsonl.zst extension
    zstd -c "$temp_file" > "$base_name.jsonl.zst"

    # Remove the temporary file
    rm "$temp_file"

    # Print a success message
    echo "Done. Output file: $base_name.jsonl.zst"
  else
    echo "Warning: no .gz file in directory: $1"
  fi
done

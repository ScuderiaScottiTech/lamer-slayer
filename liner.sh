#!/bin/bash

# Input file containing the lines
input_file="remaining_80_percent.txt"

# Ensure the input file exists
if [[ ! -f "$input_file" ]]; then
  echo "File not found: $input_file"
  exit 1
fi

# Initialize line counter
i=0

# Read each line from the input file
while IFS= read -r line || [[ -n "$line" ]]; do
  # Increment line number counter
  ((i++))

  # Generate an alphanumerical file name
  file_name=$(printf "file_%05d.txt" "$i")

  # Create a new file and write the line to it
  echo "$line" > "$file_name"

  # Optional: echo the file name created
  echo "Created $file_name"

done < "$input_file"

echo "All lines have been processed."


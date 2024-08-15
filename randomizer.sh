#!/bin/bash

# Check if a file was provided as an argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <filename>"
  exit 1
fi

# Input file
input_file="$1"

# Check if the file exists
if [ ! -f "$input_file" ]; then
  echo "File not found!"
  exit 1
fi

# Calculate the total number of lines in the file
total_lines=$(wc -l < "$input_file")

# Calculate 20% of the total lines
num_lines_to_select=$((total_lines * 20 / 100))

# Generate random line numbers, sort them, and save to a temp file
shuf -i 1-"$total_lines" -n "$num_lines_to_select" | sort -n > random_lines.txt

# Extract the selected lines and save to a new file
sed -n -f <(sed 's/$/p/' random_lines.txt) "$input_file" > "random_20_percent.txt"

# Extract the remaining 80% lines
# First, invert the selection and output to remaining_80_percent.txt
awk 'NR==FNR {a[$1]; next} !(FNR in a)' random_lines.txt "$input_file" > "remaining_80_percent.txt"

# Clean up the temporary file
rm random_lines.txt

# Notify the user
echo "Random 20% of lines extracted to random_20_percent.txt"
echo "Remaining 80% of lines extracted to remaining_80_percent.txt"

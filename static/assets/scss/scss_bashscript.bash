#!/bin/bash

# Set the directory containing your SCSS files
SCSS_DIR="."

# Loop through each .scss file in the directory
for file in "$SCSS_DIR"/*.scss; do
    # Check if the file exists to prevent errors if no .scss files are found
    if [[ -f "$file" ]]; then
        # Get the filename without the directory path
        filename=$(basename -- "$file")
        
        # Remove the .scss extension to point to the corresponding .css file
        css_filename="${filename%.scss}.scss"
        
        # Print the <link> tag with the appropriate format
        echo "<link rel=\"stylesheet\" href=\"{% static 'assets/scss/$css_filename' %}\" >"
    else
        echo "No .scss files found in $SCSS_DIR"
    fi
done

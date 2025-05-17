#!/bin/bash

# Default values
URL=""
OUTPUT_DIR="."

# Function to display usage
usage() {
    echo "Usage: $0 --url <youtube_url> [--output <output_directory>]"
    echo "Example: $0 --url 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'"
    echo "Example with output directory: $0 --url 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' --output /path/to/output"
    exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --url)
            URL="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Check if URL is provided
if [ -z "$URL" ]; then
    echo "Error: URL is required"
    usage
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Run the Python script with the arguments
python music-download.py "$URL" -o "$OUTPUT_DIR" 
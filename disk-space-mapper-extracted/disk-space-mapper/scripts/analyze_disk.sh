#!/bin/bash

# Disk Space Analyzer
# Usage: analyze_disk.sh [OPTIONS]
# Options:
#   -d <dir>     Base directory to analyze (default: current dir)
#   -m <days>    Minimum age in days to filter (default: 0, no filter)
#   -s <mb>      Minimum size in MB to filter (default: 0, no filter)
#   -o <file>    Output file for results (default: stdout)
#   -h           Show this help message

set -e

# Default values
BASE_DIR="."
MIN_DAYS=0
MIN_SIZE_MB=0
OUTPUT_FILE=""
DEPTH=1

# Parse arguments
while getopts "d:m:s:o:h" opt; do
  case $opt in
    d) BASE_DIR="$OPTARG" ;;
    m) MIN_DAYS="$OPTARG" ;;
    s) MIN_SIZE_MB="$OPTARG" ;;
    o) OUTPUT_FILE="$OPTARG" ;;
    h)
      head -n 15 "$0"
      exit 0
      ;;
    *) echo "Invalid option: -$OPTARG"; exit 1 ;;
  esac
done

# Validate base directory
if [ ! -d "$BASE_DIR" ]; then
  echo "Error: Directory '$BASE_DIR' does not exist"
  exit 1
fi

# Get current timestamp
NOW=$(date +%s)
SIX_MONTHS=$((6 * 30 * 24 * 60 * 60))

# Create output
{
  echo "Directory|Size (MB)|Last Modified|Days Since Change"
  echo "=================================================="

  # Find all directories at depth 1
  find "$BASE_DIR" -maxdepth $DEPTH -type d ! -name '.' 2>/dev/null | while read -r dir; do
    [ "$dir" = "$BASE_DIR" ] && continue

    # Calculate size
    size_kb=$(du -sk "$dir" 2>/dev/null | awk '{print $1}')
    size_mb=$((size_kb / 1024))

    # Get modification time
    mod_time=$(stat -f %m "$dir" 2>/dev/null || echo "0")
    age_seconds=$((NOW - mod_time))
    age_days=$((age_seconds / 86400))

    # Get last modified date string
    last_modified=$(stat -f %Sm "$dir" 2>/dev/null || echo "N/A")

    # Apply filters
    if [ "$MIN_DAYS" -gt 0 ] && [ "$age_days" -lt "$MIN_DAYS" ]; then
      continue
    fi
    if [ "$MIN_SIZE_MB" -gt 0 ] && [ "$size_mb" -lt "$MIN_SIZE_MB" ]; then
      continue
    fi

    echo "$dir|$size_mb MB|$last_modified|$age_days days"
  done | sort -t'|' -k2 -rn

} | tee /tmp/disk_analysis_temp.txt

# Output to file if specified
if [ -n "$OUTPUT_FILE" ]; then
  cat /tmp/disk_analysis_temp.txt > "$OUTPUT_FILE"
  echo "Results saved to: $OUTPUT_FILE"
fi

/bin/rm -f /tmp/disk_analysis_temp.txt

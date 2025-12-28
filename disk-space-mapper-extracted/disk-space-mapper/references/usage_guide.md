# Disk Space Mapper - Usage Guide

## Table of Contents

- [Quick Start](#quick-start)
- [Common Scenarios](#common-scenarios)
- [Script Options](#script-options)
- [Output Format](#output-format)
- [Filtering Examples](#filtering-examples)

## Quick Start

Analyze a directory for disk usage:

```bash
# Python version (recommended)
python3 analyze_disk.py -d /path/to/analyze

# Bash version
./analyze_disk.sh -d /path/to/analyze
```

Both produce sorted output (largest directories first) with:
- Directory path
- Size in MB
- Last modification date
- Days since last change

## Common Scenarios

### Find old directories taking up space

Identify directories not modified in 6 months that are larger than 20 MB:

```bash
python3 analyze_disk.py -d /Users/tonytam/git -m 180 -s 20 -o old_large_dirs.txt
```

- `-m 180`: Directories older than 180 days (6 months)
- `-s 20`: Directories larger than 20 MB
- `-o old_large_dirs.txt`: Save results to file

### Clean up workspace

Find anything larger than 100 MB:

```bash
python3 analyze_disk.py -d /path/to/dir -s 100
```

### Identify recent changes

Find directories modified in last 30 days:

```bash
# All directories, automatically sorted by size
python3 analyze_disk.py -d /path/to/dir
```

Then look for entries with "< 30 days" in output.

## Script Options

### Python Version (`analyze_disk.py`)

```
-d, --dir DIR           Base directory to analyze (default: current dir)
-m, --min-days DAYS     Minimum age in days (0 = no filter)
-s, --min-size SIZE_MB  Minimum size in MB (0 = no filter)
-o, --output FILE       Save results to file
-h, --help              Show help message
```

### Bash Version (`analyze_disk.sh`)

```
-d <dir>     Base directory to analyze
-m <days>    Minimum age in days
-s <mb>      Minimum size in MB
-o <file>    Output file path
-h           Show help
```

## Output Format

Results are pipe-delimited for easy parsing:

```
Directory|Size (MB)|Last Modified|Days Since Change
==================================================
/path/to/dir1|554 MB|Feb 23 13:34:56 2025|307 days
/path/to/dir2|242 MB|Mar 28 15:34:02 2025|274 days
```

## Filtering Examples

### Example 1: Budget cuts
Find anything over 200 MB not changed in 3 months:

```bash
python3 analyze_disk.py -d /git -m 90 -s 200
```

### Example 2: Old test projects
Find directories over 50 MB older than a year:

```bash
python3 analyze_disk.py -d /projects -m 365 -s 50 -o cleanup_candidates.txt
```

### Example 3: Just show everything
See all directories with sizes (for overview):

```bash
python3 analyze_disk.py -d /data
```

Output automatically sorted by size (largest first).

## Notes

- **Performance**: For very large directory trees, the scan may take 30+ seconds
- **Permissions**: Script reports directories it can access; permission-denied directories are skipped with warning
- **Output**: Always sorted by size in descending order (largest first)
- **Temporary Files**: Python version uses only in-memory data; Bash version cleans up temp files automatically

# Disk Space Mapper Skill

A Claude skill for analyzing disk usage across directories, identifying space hogs, and generating storage reports. Perfect for storage audits, cleanup projects, and finding which directories are consuming the most disk space.

## Overview

The Disk Space Mapper skill provides quick analysis of disk usage across your filesystem with intelligent filtering and sorting. Use it to:

- **Audit storage**: See what's consuming disk space in any directory tree
- **Find cleanup candidates**: Identify old directories (older than N days) that are large (larger than M MB)
- **Track active projects**: Find recently modified directories sorted by size
- **Generate reports**: Export analysis results to files for later review

## Features

✓ **Two implementations**: Python (recommended) or lightweight Bash script
✓ **Intelligent filtering**: Filter by age (days) and/or size (MB)
✓ **Automatic sorting**: Results always sorted by size (largest first)
✓ **Multiple output formats**: Console output or file export
✓ **Permission-aware**: Handles permission-denied directories gracefully
✓ **Fast performance**: Most directory trees scan in under 30 seconds
✓ **Safe**: Read-only analysis, no files are deleted

## Installation

The skill is packaged as `disk-space-mapper.skill`. To use it with Claude Code:

```bash
# The skill is ready to use directly
# Both Python and Bash scripts are included in the package
```

## Quick Start

### Analyze a directory for disk usage:

```bash
python3 analyze_disk.py -d /path/to/analyze
```

### Find old (180+ days) and large (20+ MB) directories:

```bash
python3 analyze_disk.py -d /path/to/analyze -m 180 -s 20 -o report.txt
```

## Usage

### Python Version (Recommended)

Full-featured implementation with comprehensive filtering and error handling.

**Command:**
```bash
python3 analyze_disk.py [OPTIONS]
```

**Options:**
- `-d, --dir DIR` — Base directory to analyze (default: current directory)
- `-m, --min-days DAYS` — Filter: only directories older than N days
- `-s, --min-size SIZE_MB` — Filter: only directories larger than N MB
- `-o, --output FILE` — Save results to file
- `-h, --help` — Show help message

**Examples:**

```bash
# Storage audit - see everything sorted by size
python3 analyze_disk.py -d /Users/tonytam/git

# Find cleanup candidates
python3 analyze_disk.py -d /data -m 180 -s 20 -o old_large.txt

# Find anything over 100 MB
python3 analyze_disk.py -d /projects -s 100

# Find old directories (1+ year)
python3 analyze_disk.py -d /archive -m 365
```

### Bash Version

Lightweight alternative using standard Unix tools (`du`, `stat`, `find`).

**Command:**
```bash
./analyze_disk.sh [OPTIONS]
```

**Options:**
- `-d <dir>` — Base directory to analyze
- `-m <days>` — Minimum age in days
- `-s <mb>` — Minimum size in MB
- `-o <file>` — Output file path
- `-h` — Show help

**Example:**
```bash
./analyze_disk.sh -d /git -m 180 -s 20 -o old_large.txt
```

## Common Use Cases

### 1. Storage Audit

See what's consuming disk space in your entire git directory:

```bash
python3 analyze_disk.py -d /Users/tonytam/git
```

Output shows each directory with:
- Path
- Size in MB
- Last modification date
- Days since last change

### 2. Find Cleanup Candidates

Identify directories not touched in 6 months that exceed 20 MB:

```bash
python3 analyze_disk.py -d /Users/tonytam/git -m 180 -s 20 -o candidates.txt
```

### 3. Identify Recent Changes

View directories modified recently (largest first):

```bash
python3 analyze_disk.py -d /active/projects
```

Look for entries with low "Days Since Change" values.

### 4. Budget Cuts

Find anything over 200 MB not changed in 3 months:

```bash
python3 analyze_disk.py -d /data -m 90 -s 200
```

### 5. Archive Analysis

Find old test projects (1+ year, 50+ MB):

```bash
python3 analyze_disk.py -d /projects -m 365 -s 50 -o cleanup_candidates.txt
```

## Output Format

Results are displayed in pipe-delimited format for easy parsing or importing:

```
Directory|Size (MB)|Last Modified|Days Since Change
==================================================
/path/to/large_dir|554 MB|Feb 23 13:34:56 2025|307 days
/path/to/medium_dir|242 MB|Mar 28 15:34:02 2025|274 days
/path/to/small_dir|37 MB|Dec  2 08:05:07 2023|756 days
```

**Key points:**
- Always sorted by size in descending order (largest first)
- Pipe-delimited columns for easy parsing with `cut`, `grep`, etc.
- Can be redirected to file with `-o` option

## Filtering Explained

### Minimum Days (`-m`)

Only include directories modified **longer than N days ago**:

```bash
# Find directories not touched in 6 months (180 days)
python3 analyze_disk.py -d /data -m 180
```

### Minimum Size (`-s`)

Only include directories **larger than N MB**:

```bash
# Find directories exceeding 100 MB
python3 analyze_disk.py -d /data -s 100
```

### Combined Filters

Use both to find directories matching **both conditions** (AND logic):

```bash
# Find old AND large: older than 6 months AND larger than 20 MB
python3 analyze_disk.py -d /data -m 180 -s 20
```

### No Filters

Run without `-m` or `-s` to see all directories:

```bash
python3 analyze_disk.py -d /data
```

## Advanced Usage

### Parse Results with Unix Tools

Since output is pipe-delimited, you can combine with standard tools:

```bash
# Show only paths and sizes
python3 analyze_disk.py -d /data | cut -d'|' -f1,2

# Find directories over 1GB
python3 analyze_disk.py -d /data | grep -E '[0-9]{4,} MB'

# Count matching directories
python3 analyze_disk.py -d /data -m 180 -s 20 | wc -l
```

### Combine with Other Commands

```bash
# Analyze and immediately sort by age
python3 analyze_disk.py -d /data | sort -t'|' -k4 -rn

# Generate timestamped report
python3 analyze_disk.py -d /data -o "report_$(date +%Y%m%d_%H%M%S).txt"
```

## Performance Notes

- **Typical performance**: Most directory trees scan in under 30 seconds
- **Large trees**: May take longer for very large directory structures with thousands of subdirectories
- **Permission handling**: Script reports accessible directories; permission-denied directories are skipped with warnings
- **Memory usage**: Python version uses in-memory data structures; Bash version streams results

## Troubleshooting

### "Permission denied" warnings

The script skips directories it cannot access and continues analysis. This is normal and safe.

```bash
# To minimize warnings, run with elevated privileges if needed
sudo python3 analyze_disk.py -d /restricted/path
```

### No results found

If no directories match your criteria:

```bash
# Try without filters to verify directories exist
python3 analyze_disk.py -d /path/to/dir

# Check if filters are too strict
python3 analyze_disk.py -d /path/to/dir -m 30   # Last 30 days
python3 analyze_disk.py -d /path/to/dir -s 10   # At least 10 MB
```

### Slow analysis on large trees

For very large directory structures with thousands of subdirectories:

```bash
# Consider analyzing subdirectories separately
python3 analyze_disk.py -d /data/subdir1
python3 analyze_disk.py -d /data/subdir2
```

## Tips

- **Start broad**: Begin with no filters to understand your disk usage
- **Refine gradually**: Add filters (`-m`, `-s`) to narrow results
- **Export for review**: Use `-o` to save results for later analysis
- **Combine smartly**: Use grep, cut, or sort with output for custom filtering
- **Verify before cleanup**: Always review results before deleting anything

## Files Included

- `scripts/analyze_disk.py` — Python implementation (recommended)
- `scripts/analyze_disk.sh` — Bash implementation
- `SKILL.md` — Detailed skill description
- `references/usage_guide.md` — Extended usage examples

## License

This skill is provided as-is for local analysis use. No files are modified or deleted; analysis is read-only.

## Questions?

For detailed examples and scenarios, see the included `references/usage_guide.md` documentation.

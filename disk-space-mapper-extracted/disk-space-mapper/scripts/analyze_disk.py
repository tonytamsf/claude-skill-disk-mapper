#!/usr/bin/env python3
"""
Disk Space Analyzer
Analyzes directory disk usage, filters by age/size, and generates reports.

Usage:
  python3 analyze_disk.py -d /path/to/dir [-m DAYS] [-s SIZE_MB] [-o OUTPUT_FILE]
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

def get_dir_size_mb(path):
    """Get directory size in MB using du -sk"""
    try:
        result = subprocess.run(['du', '-sk', str(path)],
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            size_kb = int(result.stdout.split()[0])
            return size_kb // 1024
    except Exception:
        pass
    return 0

def get_mod_time(path):
    """Get file modification time"""
    try:
        return os.path.getmtime(path)
    except Exception:
        return None

def days_since_change(mod_time):
    """Calculate days since file was modified"""
    if mod_time is None:
        return None
    now = datetime.now().timestamp()
    seconds_ago = now - mod_time
    return int(seconds_ago / 86400)

def format_date(timestamp):
    """Format timestamp as readable date"""
    return datetime.fromtimestamp(timestamp).strftime("%b %d %H:%M:%S %Y")

def analyze_directories(base_dir, min_days=0, min_size_mb=0, depth=1):
    """Analyze directories and return sorted results"""
    results = []

    if not os.path.isdir(base_dir):
        print(f"Error: Directory '{base_dir}' does not exist", file=sys.stderr)
        return []

    try:
        entries = os.listdir(base_dir)
    except PermissionError:
        print(f"Warning: Permission denied reading {base_dir}", file=sys.stderr)
        return []

    for entry in entries:
        full_path = os.path.join(base_dir, entry)

        if not os.path.isdir(full_path):
            continue

        size_mb = get_dir_size_mb(full_path)
        mod_time = get_mod_time(full_path)
        days = days_since_change(mod_time) if mod_time else 0

        # Apply filters
        if min_days > 0 and days < min_days:
            continue
        if min_size_mb > 0 and size_mb < min_size_mb:
            continue

        last_modified = format_date(mod_time) if mod_time else "N/A"

        results.append({
            'path': full_path,
            'size_mb': size_mb,
            'days_old': days,
            'last_modified': last_modified
        })

    # Sort by size descending
    results.sort(key=lambda x: x['size_mb'], reverse=True)
    return results

def print_results(results, output_file=None):
    """Print results in formatted table"""
    output_lines = []
    output_lines.append("Directory|Size (MB)|Last Modified|Days Since Change")
    output_lines.append("=" * 70)

    for item in results:
        line = f"{item['path']}|{item['size_mb']} MB|{item['last_modified']}|{item['days_old']} days"
        output_lines.append(line)

    output = '\n'.join(output_lines)
    print(output)

    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(output)
            print(f"\nResults saved to: {output_file}")
        except Exception as e:
            print(f"Error writing to file: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze disk usage by directory',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Analyze current directory
  python3 analyze_disk.py -d .

  # Find old (>180 days) and large (>20MB) directories
  python3 analyze_disk.py -d /path/to/dir -m 180 -s 20

  # Save results to file
  python3 analyze_disk.py -d /path/to/dir -m 180 -s 20 -o results.txt
        '''
    )

    parser.add_argument('-d', '--dir', default='.',
                       help='Base directory to analyze (default: current dir)')
    parser.add_argument('-m', '--min-days', type=int, default=0,
                       help='Minimum age in days to include (default: 0)')
    parser.add_argument('-s', '--min-size', type=int, default=0,
                       help='Minimum size in MB to include (default: 0)')
    parser.add_argument('-o', '--output',
                       help='Output file to save results')

    args = parser.parse_args()

    results = analyze_directories(
        args.dir,
        min_days=args.min_days,
        min_size_mb=args.min_size
    )

    if not results:
        print("No directories matching criteria found.")
        return 1

    print_results(results, args.output)
    return 0

if __name__ == '__main__':
    sys.exit(main())

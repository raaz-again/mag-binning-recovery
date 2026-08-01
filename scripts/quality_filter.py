#!/usr/bin/env python3
"""
quality_filter.py

Filter metagenome-assembled genomes (MAGs) by completeness and contamination
thresholds, using a CheckM-style quality report, and classify each bin
according to the MIMAG draft genome quality standard.

Expected input (tab-separated):
    bin_id    completeness    contamination

Usage:
    python quality_filter.py --checkm checkm_output.tsv --output high_quality_bins.tsv --min-completeness 90 --max-contamination 5
"""

import argparse
import csv
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Filter MAGs by completeness/contamination thresholds."
    )
    parser.add_argument("--checkm", required=True, help="CheckM-style TSV: bin_id, completeness, contamination.")
    parser.add_argument("--output", required=True, help="Output TSV file with bins passing the thresholds.")
    parser.add_argument("--min-completeness", type=float, default=90.0, help="Minimum completeness percentage (default: 90).")
    parser.add_argument("--max-contamination", type=float, default=5.0, help="Maximum contamination percentage (default: 5).")
    return parser.parse_args()


def classify_mimag(completeness, contamination):
    """Classify a bin according to the MIMAG draft genome quality standard."""
    if completeness >= 90 and contamination < 5:
        return "high-quality"
    if completeness >= 50 and contamination < 10:
        return "medium-quality"
    return "low-quality"


def load_checkm(path):
    rows = []
    with open(path) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required_cols = {"bin_id", "completeness", "contamination"}
        if not required_cols.issubset(reader.fieldnames or []):
            sys.exit(f"CheckM file must contain columns: {sorted(required_cols)}. Found: {reader.fieldnames}")
        for row in reader:
            rows.append({
                "bin_id": row["bin_id"],
                "completeness": float(row["completeness"]),
                "contamination": float(row["contamination"]),
            })
    return rows


def main():
    args = parse_args()

    if not Path(args.checkm).exists():
        sys.exit(f"CheckM file not found: {args.checkm}")

    rows = load_checkm(args.checkm)
    passing = []
    for row in rows:
        row["mimag_quality"] = classify_mimag(row["completeness"], row["contamination"])
        if row["completeness"] >= args.min_completeness and row["contamination"] <= args.max_contamination:
            passing.append(row)

    with open(args.output, "w", newline="") as handle:
        fieldnames = ["bin_id", "completeness", "contamination", "mimag_quality"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(passing)

    print(f"{len(passing)}/{len(rows)} bins passed completeness >= {args.min_completeness} "
          f"and contamination <= {args.max_contamination}. Written to {args.output}")


if __name__ == "__main__":
    main()

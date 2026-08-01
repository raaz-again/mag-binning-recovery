#!/usr/bin/env python3
"""
bin_summary.py

Compute basic per-bin summary statistics (contig count, total length,
average contig length) from a contig-to-bin assignment table, as produced
by binning tools such as MetaBAT2, CONCOCT, or MaxBin2.

Expected input (tab-separated):
    contig_id    bin_id    length

Usage:
    python bin_summary.py --assignments contig_bins.tsv --output bin_summary.tsv
"""

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Summarize contig-to-bin assignments into per-bin statistics."
    )
    parser.add_argument("--assignments", required=True, help="TSV file: contig_id, bin_id, length.")
    parser.add_argument("--output", required=True, help="Output TSV file with per-bin summary stats.")
    return parser.parse_args()


def load_assignments(path):
    bins = defaultdict(list)
    with open(path) as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        required_cols = {"contig_id", "bin_id", "length"}
        if not required_cols.issubset(reader.fieldnames or []):
            sys.exit(f"Assignments file must contain columns: {sorted(required_cols)}. Found: {reader.fieldnames}")
        for row in reader:
            bins[row["bin_id"]].append(int(row["length"]))
    return bins


def summarize(bins):
    summary = []
    for bin_id, lengths in bins.items():
        total_length = sum(lengths)
        num_contigs = len(lengths)
        avg_length = total_length / num_contigs if num_contigs else 0
        summary.append({
            "bin_id": bin_id,
            "num_contigs": num_contigs,
            "total_length": total_length,
            "avg_contig_length": round(avg_length, 1),
        })
    return sorted(summary, key=lambda r: r["total_length"], reverse=True)


def write_summary(summary, output_path):
    fieldnames = ["bin_id", "num_contigs", "total_length", "avg_contig_length"]
    with open(output_path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(summary)


def main():
    args = parse_args()

    if not Path(args.assignments).exists():
        sys.exit(f"Assignments file not found: {args.assignments}")

    bins = load_assignments(args.assignments)
    summary = summarize(bins)
    write_summary(summary, args.output)

    print(f"Summarized {len(summary)} bins from {args.assignments}. Report written to {args.output}")


if __name__ == "__main__":
    main()

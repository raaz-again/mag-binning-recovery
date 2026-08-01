# mag-binning-recovery

Workflows for genome binning and recovery of metagenome-assembled genomes (MAGs) from metagenomic assemblies, including quality assessment and dereplication.

## Overview

This repository provides two command-line tools that work downstream of a binning tool such as MetaBAT2, CONCOCT, or MaxBin2: a bin summary script that computes contig counts and total length per bin, and a quality filter that classifies and filters bins using CheckM-style completeness and contamination scores according to the MIMAG draft genome quality standard.

## Installation

```
pip install -r requirements.txt
```

## Usage

Bin summary statistics:

```
python scripts/bin_summary.py --assignments examples/example_contig_bins.tsv --output bin_summary.tsv
```

Quality filtering and MIMAG classification:

```
python scripts/quality_filter.py --checkm examples/example_checkm.tsv --output high_quality_bins.tsv --min-completeness 90 --max-contamination 5
```

## Input format

Contig-to-bin assignments (tab-separated): contig_id, bin_id, length.
CheckM-style quality report (tab-separated): bin_id, completeness, contamination.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

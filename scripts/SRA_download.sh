#!/bin/bash

# Usage: ./download_sra.sh sra_list.txt /path/to/output_dir

sra_list="$1"
output_dir="$2"

mkdir -p "$output_dir"

while read -r accession; do
    echo "Downloading $accession..."
    fastq-dump --outdir "$output_dir" --gzip --skip-technical --readids --read-filter pass --dumpbase --split-3 --clip "$accession"
done < "$sra_list"

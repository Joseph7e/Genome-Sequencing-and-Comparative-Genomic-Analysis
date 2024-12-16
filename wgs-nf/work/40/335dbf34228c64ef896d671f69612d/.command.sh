#!/bin/bash -ue
# Run SPAdes and redirect errors
spades.py -1 trimmed_R1.fastq.gz -2 trimmed_R2.fastq.gz -o output-spades --threads 24

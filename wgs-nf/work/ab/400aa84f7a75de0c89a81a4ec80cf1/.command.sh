#!/bin/bash -ue
echo "Processing: testagain_1.fastq.gz testagain_2.fastq.gz"

fastp -i testagain_1.fastq.gz -I testagain_2.fastq.gz         -o trimmed_R1.fastq.gz -O trimmed_R2.fastq.gz         --thread 24

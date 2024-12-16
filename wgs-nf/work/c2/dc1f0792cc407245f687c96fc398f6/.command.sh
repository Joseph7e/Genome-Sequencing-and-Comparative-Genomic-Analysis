#!/bin/bash -ue
echo "Processing: testagain2_1.fastq.gz testagain2_2.fastq.gz"

fastp -i testagain2_1.fastq.gz -I testagain2_2.fastq.gz         -o trimmed_R1.fastq.gz -O trimmed_R2.fastq.gz         --thread 24

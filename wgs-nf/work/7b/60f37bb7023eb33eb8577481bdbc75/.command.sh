#!/bin/bash -ue
bwa index contigs.fasta

bwa mem contigs.fasta trimmed_R1.fastq.gz trimmed_R2.fastq.gz -t 24         | samtools view -bS -@ 24 - |         samtools sort -@ 24 -o mapped.bam

# index output file
samtools index mapped.bam

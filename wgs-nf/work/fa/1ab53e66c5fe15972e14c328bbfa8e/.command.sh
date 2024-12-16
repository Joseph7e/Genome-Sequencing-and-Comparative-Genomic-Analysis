#!/bin/bash -ue
mkdir -p "output-fastqc/"
fastqc testagain_1.fastq.gz testagain_2.fastq.gz --outdir output-fastqc/ --threads 24

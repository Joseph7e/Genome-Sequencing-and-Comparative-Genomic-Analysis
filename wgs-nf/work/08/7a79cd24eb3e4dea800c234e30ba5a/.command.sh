#!/bin/bash -ue
mkdir -p "output-fastqc/"
fastqc testagain2_1.fastq.gz testagain2_2.fastq.gz --outdir output-fastqc/ --threads 24

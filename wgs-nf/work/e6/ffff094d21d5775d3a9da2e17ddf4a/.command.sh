#!/bin/bash -ue
busco -i contigs.fasta         -o output-busco         -l bacteria_odb10         --mode genome         --cpu 24         --offline         --download_path /home/users/jlsevigny1/nextflow-workflows/nigms-wgs/databases/busco_downloads/

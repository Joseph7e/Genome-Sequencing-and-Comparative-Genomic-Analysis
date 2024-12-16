#!/bin/bash -ue
blastn         -task megablast         -query contigs.fasta         -db /home/users/jlsevigny1/nextflow-workflows/nigms-wgs/databases/blast_db/small_db         -outfmt '6 qseqid staxids bitscore std'         -max_target_seqs 1         -max_hsps 1         -num_threads 24         -evalue 1e-25         -out genome.vs.nt.mts1.hsp1.1e25.megablast.out

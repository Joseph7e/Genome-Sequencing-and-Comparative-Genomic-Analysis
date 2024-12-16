#!/usr/bin/env nextflow

params.reads = './raw-reads/*_{1,2}.fastq.gz'
params.output_dir = './output'
params.threads = 24
params.blast_db = "${launchDir}/databases/blast_db/small_db"
params.busco_db = "${launchDir}/databases/busco_downloads/"



// Step 1: Quality control with FastQC
process run_fastqc {
//     container 'quay.io/biocontainers/fastqc:0.11.9--hdfd78af_1'

    input:
    tuple val(sampleid), file(fq1), file(fq2)

    output:
    file("output-fastqc/")

    script:
    """
    mkdir -p "output-fastqc/"
    fastqc ${fq1} ${fq2} --outdir output-fastqc/ --threads ${params.threads}
    """
}


// Step 2: Trim paired-end reads with FASTP
process run_fastp {
    input:
    tuple val(sampleid), file(fq1), file(fq2)
    
    output:
    tuple file("trimmed_R1.fastq.gz"), file("trimmed_R2.fastq.gz")
    
    script:
    """
    echo "Processing: $fq1 $fq2"

    fastp -i $fq1 -I $fq2 \
        -o trimmed_R1.fastq.gz -O trimmed_R2.fastq.gz \
        --thread ${params.threads}
    """
}


process run_spades {
    input:
    tuple file(fq1), file(fq2)

    output:
    file("output-spades/contigs.fasta")

    script:
    """
    # Run SPAdes and redirect errors
    spades.py -1 $fq1 -2 $fq2 -o output-spades --threads ${params.threads}
    """
}


process run_bwa {
    input:
    tuple file(fq1), file(fq2), file(genome)

    output:
    file("mapped.bam")
    
    script:
    """
    bwa index $genome

    bwa mem $genome $fq1 $fq2 -t ${params.threads} \
        | samtools view -bS -@ ${params.threads} - | \
        samtools sort -@ ${params.threads} -o mapped.bam

    # index output file
    samtools index mapped.bam
    """
}

process run_busco {
    input:
    file(genome)

    output:
    file 'output-busco/short_summary.specific.bacteria_odb10.output-busco.txt'

    script:
    """
    busco -i $genome \
        -o output-busco \
        -l bacteria_odb10 \
        --mode genome \
        --cpu ${params.threads} \
        --offline \
        --download_path ${params.busco_db}
    """
}

process run_quast {
    input:
    file(genome)

    output:
    file('quast_output/report.txt')

    script:
    """
    quast.py $genome -o quast_output
    """
}

process run_blast {
    input:
    file genome

    output:
    file('genome.vs.nt.mts1.hsp1.1e25.megablast.out')

    script:
    """
        blastn \
        -task megablast \
        -query $genome \
        -db ${params.blast_db} \
        -outfmt '6 qseqid staxids bitscore std' \
        -max_target_seqs 1 \
        -max_hsps 1 \
        -num_threads ${params.threads} \
        -evalue 1e-25 \
        -out genome.vs.nt.mts1.hsp1.1e25.megablast.out
    """
}

process run_blobtools {
    input:
    file contigs
    file bam
    file blast_out

    output:
    file 'blobtools_output'

    script:
    """
    blobtools create -i $contigs -b $bam -t $blast_out -o blobtools_output
    """
}

process contamination_check {
    input:
    file blobtools_output

    output:
    file 'contamination_report'

    script:
    """
    blobtools view -i blobtools_output -o contamination_report
    """
}

process run_bakta {
    input:
    file genome

    output:
    file 'bakta_output/*.faa'
    file 'bakta_output/'


    script:
    """
    prokka --outdir prokka_output --prefix annotated $contigs
    """
}

process finalizeResults {
    input:
    tuple val(sample_id), file(fastqc_results), file(contigs), file(quast_results)

    output:
    file("${sample_id}_final_report.txt") into final_output

    publishDir "./output", mode: 'copy'

    script:
    """
    echo "Sample ID: $sample_id" > ${sample_id}_final_report.txt
    echo "FASTQC Results: $fastqc_results" >> ${sample_id}_final_report.txt
    echo "Contigs: $contigs" >> ${sample_id}_final_report.txt
    echo "QUAST Results: $quast_results" >> ${sample_id}_final_report.txt
    """
}


// Process to Create a Final Summary Table
// process createFinalTable {
//     input:
//     file(final_reports) from final_output.collect()
//
//     output:
//     file("final_results_table.txt")
//
//     script:
//     """
//     # Create the header for the table
//     echo -e "SampleID\tFASTQCResults\tContigs\tQUASTResults" > final_results_table.txt
//
//     # Loop through all final report files and append the necessary data to the table
//     for report in ${final_reports}; do
//         sample_id=\$(basename \$report _final_report.txt)
//         fastqc_result=\$(grep -oP 'FASTQC Results: \K.+' \$report)
//         contigs=\$(grep -oP 'Contigs: \K.+' \$report)
//         quast_result=\$(grep -oP 'QUAST Results: \K.+' \$report)
//
//         echo -e "\$sample_id\t\$fastqc_result\t\$contigs\t\$quast_result" >> final_results_table.txt
//     done
//     """
// }


workflow {
    fastq_files = Channel
    .fromFilePairs(params.reads, flat: false)
    .map { sample_id, files -> tuple(sample_id, files[0], files[1]) }

    fastq_files.view()

    // Step 1: Run FASTQC
    fastqc_report = fastq_files | run_fastqc

    // Step 2: Trim reads with FASTP
    trimmed_fastq = fastq_files | run_fastp

    // Step 3: Assemble genome with SPADES
    genome = trimmed_fastq | run_spades

    // Step 4.1: Map reads back to genome
    bwa_input = trimmed_fastq.combine(genome)
    bam = bwa_input | run_bwa

    // Step 4.2: Run BUSCO
    busco_results = genome | run_busco

    // Step 4.3: Run QUAST
    quast_report = genome | run_quast

    // Step 4.4: Run BLAST
    blast_results = genome | run_blast

//     // Step 7: Run Blobtools
//     blob_output = blobtools(assembly, mapped_bam, blast_results)

//     // Step 8: Contamination checking
//     contamination_check(blob_output)
//
//     // Step 9: Annotate genome with Prokka
//     annotated_proteome = annotate(assembly)
//
//     // Final output: Prokka annotated proteome FAA file
//     annotated_proteome.view { it -> println("Final FAA file: ${it}") }

    fastqc_report.view { println("FASTQC results: $it") }
    trimmed_fastq.view { println("FASTP results: $it") }
    genome.view { println("Assembly results: $it") }
    quast_report.view { println("QUAST report: $it") }

    // Merge results for finalization
//     finalize_input = fastqc_results
//     .zip(assembly) { fastqc, asm -> tuple(fastqc[0], fastqc[1], asm[1]) }
//     .zip(quast_report) { data, quast -> tuple(data[0], data[1], data[2], quast[1]) }


//     finalize_input.view { println "Final input to finalizeResults: $it" }


//     finalize_input | finalizeResults
}

// workflow.onComplete {
//     println "Workflow completed successfully!"
//     println "Reports generated: report.html, timeline.html, trace.txt"
//     println "Final results available in the 'output/' directory."
// }
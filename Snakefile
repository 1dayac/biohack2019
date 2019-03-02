configfile: "config.json"
configfile: "path_to_executables_config.json"


R1=config["r1"]
R2=config["r2"]
SAMPLE=config["sample"]
GIT_ROOT=config["root"]
GMAP=config["gmap"]
STAR=config["star"]
GMAP_GENOME_DIR=config["gmap_genome_dir"]
STAR_INDEX=config["star_index"]
SAMTOOLS=config["samtools"]
RNASPADES=config["rnaspades"]
THREADS=config["threads"]
MEMORY=config["memory"]


rule all:
    input:
        expand("{sample}.vcf", sample=SAMPLE)

rule align_reads_with_star:
    input:
        r1='sample/{sample}_1.fastq.gz',
        r2='sample/{sample}_2.fastq.gz'
    output:
        star_bam='star/{sample}.bam'
    shell:
        """
        mkdir -p star
        {STAR} --runThreadN {THREADS} --genomeDir {STAR_INDEX} --readFilesIn {input.r1} {input.r2} ---outFileNamePrefix star/{wildcards.sample} --outSAMstrandField intronMotif --chimSegmentMin 20 --readFilesCommand zcat --outSAMmapqUnique 50
        """

rule extract_poorly_mapped:
    input:
        star_bam='star/{sample}.bam'
    output:
        unmapped_left='unmapped_reads/{sample}_unmapped_R1.fastq',
        unmapped_right='unmapped_reads/{sample}_unmapped_R2.fastq'
    shell:
        """
        {GIT_ROOT}/bxtools/bin/bxtools filter {input.star_bam} -b -s 0.05 -q 10 >star/{wildcards.sample}_unmapped.bam
        mkdir -p unmapped_reads
        {GIT_ROOT}/bxtools/bin/bxtools bamtofastq star/{wildcards.sample}_unmapped.bam unmapped_reads
        """

rule assemble_poorly_mapped:
    input:
        unmapped_left='unmapped_reads/{sample}_unmapped_R1.fastq',
        unmapped_right='unmapped_reads/{sample}_unmapped_R2.fastq'
    output:
        transcripts='{sample}.fasta'
    shell:
        """
        {RNASPADES} --pe1-1 {input.unmapped_left} --pe1-2 {input.unmapped_right} -o assembly
        {GIT_ROOT}/contig_length_filter.py 300 assembly/transcripts.fasta {output.transcripts}
        """

rule map_contigs:
    input:
        transcripts='{sample}.fasta'
    output:
        alignments='gmap/{sample}.sam'
    shell:
        """
        mkdir -p gmap
        {GMAP} -D {GMAP_GENOME_DIR} -d {GMAP_GENOME_DIR}/index/ {input.transcripts} --format=samse -t {THREADS} -O >{output.alignments}
        """

rule sam_to_vcf:
    input:
            transcripts='gmap/{sample}.sam'
    output:
            vcf='{sample}.vcf'
    shell:
        """
        python {GIT_ROOT}/sam_to_vcf.py {input.transcripts} {output.vcf}
        """
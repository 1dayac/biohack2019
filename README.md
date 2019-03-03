RNA Torch
======

RNA Torch aims to detect INDELS in RNA-Seq data

# Table of contents
1. [Installation](#installation)
2. [Commands Options](#commands-options)
3. [Output Formats](#output-formats)
4. [Command](#command)

## Installation

To start working with RNA Torch please clone this repository recursively:

```
git clone --recursive git@github.com:1dayac/biohack2019.git
```

If you clone repository non-recursively RNA Torch will not work. To fix this run:

```
git submodule update --init --recursive
```

RNA Torch is a pipeline based on a popular Snakemake workflow management system and consists of several steps and requires some external sofware.

Python dependencies are listed in requrements.txt file. The can be downloded and installed with following command:

```
pip install -r requirements.txt
```

Following software also should be installed:

* STAR (version >= 2.5) - [Download Page](https://github.com/alexdobin/STAR)
* GMAP - [Download Page](http://research-pub.gene.com/gmap/)
* Velvet - [GitHub Page](https://github.com/dzerbino/velvet) - outdated but still useful assembler with minimal assumptions about the data
* Samtools - [Project Page](http://www.htslib.org/)
* SPAdes - [Project Page](http://cab.spbu.ru/software/spades/)

Some of these programms can be installed with conda package. Highly recommended. 
Path to executables should be provided in path_to_executables_config.json file.
Inside bxtools folder run following commands:

```
./configure
make
make install
```

Then you are ready to go.


## Commands Options

RNA Torch can be run with rnatorch.py script with two modes:

* run - run pipeline from the scratch
* restart - if previous pipeline was not finished for some reason you can try to catch up with rnatorch.py restart command.

A typical command to start RNA Torch is 
```
python rnatorch.py run --r1 sample_1.fastq.gz --r2 sample_2.fastq.gz --star <path_to_star_index> --gmap <path_to_gmap_genome_dir> --outdir my_dir
```

You can invoke help message by typing:

```
python rnatorch.py run --help
```
or

```
python rnatorch.py restart --help
```
## Output Formats

RNA Torch write results into vcf-file. It will be stored inside the output folder.


## Command

This software was written during 48-hour hackathon BioHack2019. It wouldn't be possible without our team:

* Dmitrii Meleshko
* Alexey Zarubin
* Alexander Fyodorov
* Daria Vedernikova
* Galiya Eshmagambetova
* Guriev Victor

Feel free to drop any inquiry to [dmitrii.meleshko@gmail.com]() 

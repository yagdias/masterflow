#!/usr/bin/python3
# -*- coding: utf-8 -*-


######IMPORT_MODULES######

import argparse
import os
import re
import shutil
from scripts.quality_control import QualityControl
from scripts.align import Aligner
from scripts.assembler import Assembler

########ARGUMENTS#######

parser = argparse.ArgumentParser(description='This tool aims to assemble virus genomes of Ilumina reads')
parser.add_argument("-r1", "--reads1", help="reads1 fastq", required=True)
parser.add_argument("-r2", "--reads2", help="reads2 fastq", required=True)
parser.add_argument("-p", "--threads", help="threads to be used in analisys", required=False, default=1)
parser.add_argument("-q", "--quality_threshold", help="phred quality threshhold for fastp", required=False, default=30)
parser.add_argument("-r", "--reference_genome", help="Reference genome for Bowtie2", required=True)
parser.add_argument("-omh", "--outputmh", help="Output for megahit", required=True)
parser.add_argument("-pr", "--prefix", help="Write the prefix name for output files", required=False)
parser.add_argument("-o","--output", help="Output directory", required=False, default="output")
parser.add_argument("-rm", "--removetmp", help="Remove temporary files generated through analysis? default = True.", default=True, choices=['True', 'False'])


args = parser.parse_args()
reads1 = args.reads1
reads2 = args.reads2
threads = args.threads
quality_threshold = args.quality_threshold
reference = args.reference_genome
outputmh = args.outputmh
prefix = args.prefix
output = args.output
remove_tmp = args.removetmp

if prefix == None:
    prefix = re.sub("_.*", "", reads1)

# Run Quality Control #
if __name__ == '__main__':
# Quality control
    quality_control = QualityControl(reads1, reads2, quality_threshold)
    quality_control.run_quality_control()

# Alignment step
    aligner = Aligner(reference, f"{reads1}.fastp", f"{reads2}.fastp", threads)
    aligner.run_build_index()
    aligner.run_alignment()
    os.rename("un-conc-mate.1", f"{prefix}_1.fastq.gz.fastp.bowtie")
    os.rename("un-conc-mate.2", f"{prefix}_2.fastq.gz.fastp.bowtie")

# Assembly
    if os.path.isdir(outputmh) == True:
        shutil.rmtree(outputmh)
    assembler = Assembler(f"{prefix}_2.fastq.gz.fastp.bowtie", f"{prefix}_2.fastq.gz.fastp.bowtie", threads, outputmh)
    assembler.run_assembly()

# Organize outputs
    if os.path.isdir(output) == False:
        os.mkdir(output)
    os.rename(f"{prefix}_1.fastq.gz.fastp", f"{output}/{prefix}_1.fastq.gz.fastp")
    os.rename(f"{prefix}_2.fastq.gz.fastp", f"{output}/{prefix}_2.fastq.gz.fastp")
    os.rename(f"{prefix}_1.fastq.gz.fastp.bowtie", f"{output}/{prefix}_1.fastq.gz.fastp.bowtie")
    os.rename(f"{prefix}_2.fastq.gz.fastp.bowtie", f"{output}/{prefix}_2.fastq.gz.fastp.bowtie")
    os.rename(f"{outputmh}/final.contigs.fa", f"{output}/{prefix}.fastq.gz.fastp.bowtie.megahit")
    os.rename("fastp.html", f"{output}/fastp.html")
    os.rename("fastp.json", f"{output}/fastp.json")
    if remove_tmp == True:
        os.remove(f"{output}/{prefix}_1.fastq.gz.fastp")
        os.remove(f"{output}/{prefix}_2.fastq.gz.fastp")
        os.remove(f"{output}/{prefix}_1.fastq.gz.fastp.bowtie")
        os.remove(f"{output}/{prefix}_2.fastq.gz.fastp.bowtie")
        os.remove(f"{output}/fastp.html")
        os.remove(f"{output}/fastp.json")

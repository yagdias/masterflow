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
from scripts.utils import check_outdir

########ARGUMENTS#######

parser = argparse.ArgumentParser(description='This tool aims to assemble virus genomes of Ilumina reads')
parser.add_argument("-r1", "--reads1", help="reads1 fastq", required=True)
parser.add_argument("-r2", "--reads2", help="reads2 fastq", required=True)
parser.add_argument("-p", "--threads", help="threads to be used in analisys", required=False, default=1)
parser.add_argument("-q", "--quality_threshold", help="phred quality threshhold for fastp", required=False, default=30)
parser.add_argument("-r", "--reference_genome", help="Reference genome for Bowtie2", required=True)
parser.add_argument("-pr", "--prefix", help="Write the prefix name for output files", required=False)
parser.add_argument("-o","--outdir", help="Output directory", required=False, default="output")
parser.add_argument("-rm", "--removetmp", help="Remove temporary files generated through analysis? default = True.", default=True, choices=['True', 'False'])


args = parser.parse_args()
reads1 = args.reads1
reads2 = args.reads2
threads = args.threads
quality_threshold = args.quality_threshold
reference = args.reference_genome
prefix = args.prefix
outdir = args.outdir
remove_tmp = args.removetmp

# Run Quality Control #
if __name__ == '__main__':

    print(f"prefix name is {prefix}")    
    if prefix is None:
            prefix = reads1   
            prefix = re.sub(".*/", "", prefix) 
            prefix = re.sub("_1.*", "", prefix).rstrip("\n")

    outdir = check_outdir(outdir)
# Quality control
    quality_control = QualityControl(reads1, reads2, quality_threshold, prefix, outdir)
    quality_control.run_quality_control()

# Alignment step
    aligner = Aligner(reference, f"{outdir}/{prefix}_1.fastq.gz.fastp", f"{outdir}/{prefix}_1.fastq.gz.fastp", threads, outdir)
    aligner.run_build_index()
    aligner.run_alignment()
    os.rename(f"{outdir}/un-conc-mate.1", f"{outdir}/{prefix}_1.fastq.gz.fastp.bowtie")
    os.rename(f"{outdir}/un-conc-mate.2", f"{outdir}/{prefix}_2.fastq.gz.fastp.bowtie")

# Assembly
    assembler = Assembler(f"{outdir}/{prefix}_2.fastq.gz.fastp.bowtie", f"{outdir}/{prefix}_2.fastq.gz.fastp.bowtie", threads, outdir)
    assembler.run_assembly()
    os.rename(f"{outdir}/megahit_outdir/final.contigs.fa", f"{outdir}/{prefix}.fastq.gz.fastp.bowtie.megahit")

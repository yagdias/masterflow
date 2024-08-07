#!/usr/bin/python3
# -*- coding: utf-8 -*-


######IMPORT_MODULES######

import argparse
from masterflow.pipelinefunctions import PipelineFunctions
import masterflow.sample
import masterflow.host


########ARGUMENTS#######

parser = argparse.ArgumentParser(description='This tool aims to assemble virus genomes of Ilumina reads')
parser.add_argument("-r", "--reads_dir", help="reads directory must be with _R1.fastq.gz or _R1.fq.gz", required=True)
parser.add_argument("-p", "--threads", help="threads to be used in analisys", required=False, default=1)
parser.add_argument("-q", "--quality_threshold", help="phred quality threshhold for fastp", required=False, default=30)
parser.add_argument("-rg", "--reference_genome", help="Reference genome for Bowtie2", required=True)
parser.add_argument("-bi", "--build_index", help="Build index, default=true", default=True, choices=['True', 'False'])
parser.add_argument("-pr", "--prefix", help="Write the prefix name for output files", required=False)
parser.add_argument("-o","--outdir", help="Output directory", required=False, default="output")
parser.add_argument("-rm", "--removetmp", help="Remove temporary files generated through analysis? default = True.", default=True, choices=['True', 'False'])


args = parser.parse_args()
reads_dir = args.reads_dir
threads = args.threads
quality_threshold = args.quality_threshold
reference = args.reference_genome
build_index = args.build_index
prefix = args.prefix
outdir = args.outdir
remove_tmp = args.removetmp

########MAIN#######
# Run Quality Control #

def main():
    outdir = PipelineFunctions.check_outdir(outdir)
    sample_dict = masterflow.sample.sampleloader(reads_dir)
    sample_list = masterflow.sample.createsample(sample_dict)

    for sample in sample_list:
        PipelineFunctions.fastp(sample.r1, sample.r2, quality_threshold, sample.id, outdir)

    print("############# QUALITY CONTROL DONE #############")

# # Alignment step
    host_index = masterflow.host.build_index(reference, threads, build_index)
    host = masterflow.host.create_host(host_index)

    print("############# INDEX DONE #############")

    for sample in sample_list:
        PipelineFunctions.bowtie2_align(host.host_dir, sample.r1, sample.r2, threads, outdir, sample.id)

    print("############# MAPPING DONE #############")
    
    for sample in sample_list:
        PipelineFunctions.megahit(sample.r1, sample.r2, threads, outdir, sample.id)

    print("############# ASSEMBLY DONE #############")
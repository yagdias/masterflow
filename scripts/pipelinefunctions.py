import subprocess
import shlex
import os
import re
import shutil
from pathlib import Path
from glob import glob

class PipelineFunctions():
    @staticmethod
    def check_outdir(outdir: str) -> str:
        if  outdir.endswith("/"):
            outdir = re.sub("/$", "", outdir)
        
        Path(outdir).mkdir(parents=True, exist_ok=True)
        for file in glob(f"{outdir}/megahit_outdir_*"):
            shutil.rmtree(file)

        return outdir

    @staticmethod
    def fastp(reads1, reads2, quality_threshold, sample_id, outdir):
        """
        Description
        """

        cline = f"fastp --in1 {reads1} --in2 {reads2} --out1 {outdir}/{sample_id}_R1.fastp --out2 {outdir}/{sample_id}_R2.fastp -q {quality_threshold}"
        cline = shlex.split(cline)
        cmd_cline = subprocess.Popen(cline)
        cmd_cline.wait()
    
    @staticmethod
    def bowtie2_align(reference, reads1, reads2, threads, outdir, sample_id):
        cline = f"bowtie2 -x {reference} --un-conc {outdir} -1 {reads1} -2 {reads2} -p {threads}"
        print(cline)
        cline = shlex.split(cline)
        cmd_cline = subprocess.Popen(cline)
        cmd_cline.wait()
        os.rename(f"{outdir}/un-conc-mate.1", f"{outdir}/{sample_id}_R1.bowtie")
        os.rename(f"{outdir}/un-conc-mate.2", f"{outdir}/{sample_id}_R2.bowtie")

    @staticmethod
    def megahit(reads1, reads2, threads, outdir, sample_id):
        cline = f"megahit -1 {reads1} -2 {reads2} -o {outdir}/megahit_outdir_{sample_id} -t {threads}"
        cline = shlex.split(cline)
        cmd_cline = subprocess.Popen(cline)
        cmd_cline.wait()
        os.rename(f"{outdir}/megahit_outdir_{sample_id}/final.contigs.fa", f"{outdir}/{sample_id}.megahit")
    
    @staticmethod
    def bowtie2_build_cobra(reference, threads, sample_id, outdir):
        os.makedirs(f"{outdir}/{sample_id}_cobra", exist_ok=True)
        shutil.copy(reference, f"{outdir}/{sample_id}_cobra/")
        cline = f"bowtie2-build {outdir}/{sample_id}_cobra/{sample_id}.megahit {outdir}/{sample_id}_cobra/{sample_id}.megahit --threads {threads}"
        print(cline)
        cline = shlex.split(cline)
        cmd_cline = subprocess.Popen(cline)
        cmd_cline.wait()

    @staticmethod
    def bowtie2_align_cobra(reads1, reads2, threads, sample_id, outdir):
        cline = f"bowtie2 -p {threads} -x {outdir}/{sample_id}_cobra/{sample_id}.megahit -1 {reads1} -2 {reads2} -S {outdir}/{sample_id}_cobra/{sample_id}.sam"
        cline = shlex.split(cline)
        cmd_cline = subprocess.Popen(cline)
        cmd_cline.wait()
        cline = f"samtools view -bS {outdir}/{sample_id}_cobra/{sample_id}.sam -o {outdir}/{sample_id}_cobra/{sample_id}.bam"
        cline = shlex.split(cline)
        cmd_cline = subprocess.Popen(cline)
        cmd_cline.wait()
        cline = f"samtools sort {outdir}/{sample_id}_cobra/{sample_id}.bam -o {outdir}/{sample_id}_cobra/{sample_id}.bam"
        cline = shlex.split(cline)
        cmd_cline = subprocess.Popen(cline)
        cmd_cline.wait()

    @staticmethod
    def coverm_cobra(reads1, reads2, sample_id, outdir, threads):
        cline = f"coverm contig -1 {reads1} -2 {reads2} --reference {outdir}/{sample_id}_cobra/{sample_id}.megahit -o {outdir}/{sample_id}_cobra/{sample_id}.coverage -t {threads}"
        cline = shlex.split(cline)
        cmd_cline = subprocess.Popen(cline)
        cmd_cline.wait()
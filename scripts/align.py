import subprocess
import shlex

def build_index(reference, threads):
    cline = f"bowtie2-build -f {reference} {reference} --threads {threads}"
    cline = shlex.split(cline)
    cmd_cline = subprocess.Popen(cline)
    cmd_cline.wait()
    print("#############Index built successfully.")

def bowtie2_align(reference, reads1, reads2, threads, outdir):
    cline = f"bowtie2 -x {reference} --un-conc {outdir} -1 {reads1} -2 {reads2} -p {threads}"
    print(cline)
    cline = shlex.split(cline)
    cmd_cline = subprocess.Popen(cline)
    cmd_cline.wait()
    print("###########Alignment completed successfully.")


class Aligner:
    def __init__(self, reference, reads1, reads2, threads, outdir):
        self.reference = reference
        self.reads1 = reads1
        self.reads2 = reads2
        self.threads = threads
        self.outdir = outdir

    def run_build_index(self):
        build_index(self.reference, self.threads)

    def run_alignment(self):
        bowtie2_align(self.reference, self.reads1, self.reads2, self.threads, self.outdir)
        

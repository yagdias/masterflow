import subprocess
import shlex

def megahit(reads1, reads2, threads, outdir):
    cline = f"megahit -1 {reads1} -2 {reads2} -o {outdir}/megahit_outdir -t {threads}"
    cline = shlex.split(cline)
    cmd_cline = subprocess.Popen(cline)
    cmd_cline.wait()
    print("Assembly completed successfully.")

class Assembler:
    def __init__(self, reads1, reads2, threads, outdir):
        self.reads1 = reads1
        self.reads2 = reads2
        self.threads = threads
        self.outdir = outdir

    def run_assembly(self):
        megahit(self.reads1, self.reads2, self.threads, self.outdir)

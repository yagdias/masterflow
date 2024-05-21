import subprocess
import shlex

def megahit(reads1, reads2, threads, output):
    cline = f"megahit -1 {reads1} -2 {reads2} -o {output} -t {threads}"
    cline = shlex.split(cline)
    cmd_cline = subprocess.Popen(cline)
    cmd_cline.wait()
    print("Assembly completed successfully.")

class Assembler:
    def __init__(self, reads1, reads2, threads, output):
        self.reads1 = reads1
        self.reads2 = reads2
        self.threads = threads
        self.output = output

    def run_assembly(self):
        megahit(self.reads1, self.reads2, self.threads, self.output)

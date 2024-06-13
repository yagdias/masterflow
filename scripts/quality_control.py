import subprocess
import shlex


def fastp(reads1, reads2, quality_threshold, prefix, outdir):
    """
    Description
    """

    cline = f"fastp --in1 {reads1} --in2 {reads2} --out1 {outdir}/{prefix}_1.fastq.gz.fastp --out2 {outdir}/{prefix}_2.fastq.gz.fastp -q {quality_threshold}"
    cline = shlex.split(cline)
    cmd_cline = subprocess.Popen(cline)
    cmd_cline.wait()
    print('FASTP DONE')


class QualityControl():
    def __init__(self, reads1, reads2, quality_threshold, prefix, outdir):
        self.reads1 = reads1
        self.reads2 = reads2
        self.quality_threshold = quality_threshold
        self.prefix = prefix
        self.outdir = outdir

    def run_quality_control(self):
        fastp(self.reads1, self.reads2, self.quality_threshold, self.prefix, self.outdir)
import subprocess
import shlex


def fastp(reads1, reads2, quality_threshold):
    """
    Description
    """

    cline = f"fastp --in1 {reads1} --in2 {reads2} --out1 {reads1}.fastp --out2 {reads2}.fastp -q {quality_threshold}"
    cline = shlex.split(cline)
    cmd_cline = subprocess.Popen(cline)
    cmd_cline.wait()
    print('FASTP DONE')


class QualityControl():
    def __init__(self, reads1, reads2, quality_threshold):
        self.reads1 = reads1
        self.reads2 = reads2
        self.quality_threshold = quality_threshold

    def run_quality_control(self):
        fastp(self.reads1, self.reads2, self.quality_threshold)
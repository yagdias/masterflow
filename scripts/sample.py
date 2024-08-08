import os
import re

class Sample:
    def __init__(self, r1, r2, id):
        self.r1 = r1
        self.r2 = r2
        self.id = id

def sampleloader(reads_dir):
    sample_dict = {}
    for file in os.listdir(reads_dir):
            sample_match = re.match(r"(.*)_R1.(fastq|fq).gz", file)
            if sample_match:
                sample_name = sample_match.group(1)
                r1 = f'{reads_dir}/{sample_name}_R1.{sample_match.group(2)}.gz'
                r2 = f'{reads_dir}/{sample_name}_R2.{sample_match.group(2)}.gz'
                prefix = f"{sample_name}"
                sample_dict[sample_name] = (r1, r2)

    return sample_dict

def createsample(sample_dict):
    sample_list = []
    for i,j in sample_dict.items():
        sample = Sample(j[0], j[1], i)
        sample_list.append(sample)
    return sample_list


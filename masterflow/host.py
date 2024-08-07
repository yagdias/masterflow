import subprocess
import shlex



def build_index(reference, threads, build_index):
    if build_index == True:    
        cline = f"bowtie2-build -f {reference} {reference} --threads {threads}"
        cline = shlex.split(cline)
        cmd_cline = subprocess.Popen(cline)
        cmd_cline.wait()
        print("#############Index built successfully.")
    else:
        print("index not build, already provided")
    host_id = reference.split("/")[-1].split(".fa")[0]
    host_dir = reference
    host_index = reference.split("/")[-1]
    host_dict = {host_id:  (host_index, host_dir)}
    return host_dict

class Host:
    def __init__(self, host_id, host_index, host_dir):
        self.host_id = host_id
        self.host_index = host_index
        self.host_dir = host_dir

def create_host(host_dict):
    for key, value in host_dict.items(): 
        host = Host(key, value[0], value[1])
    return host

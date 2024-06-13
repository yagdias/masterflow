import re
from pathlib import Path


def check_outdir(outdir: str) -> str:
    if  outdir.endswith("/"):
        outdir = re.sub("/$", "", outdir)
    
    Path(outdir).mkdir(parents=True, exist_ok=True)

    return outdir

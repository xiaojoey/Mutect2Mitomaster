import os
import subprocess

dir = "GATKDATA"
os.chdir(dir)
for filename in os.listdir():
    if ".bam" in filename and ".bai" not in filename:
        subprocess.call("samtools fasta %s > result/%s.fasta" % (filename, filename), shell=True)
    print (filename)

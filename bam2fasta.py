import os
import sys
import subprocess

dir = sys.argv[1]
os.chdir(dir)
if not os.path.isdir("result"):
    os.mkdir("result")
for filename in os.listdir():
    if ".bam" in filename and ".bai" not in filename:
        subprocess.call("samtools fasta %s > result/%s.fasta" % (filename, filename), shell=True)
    print (filename)

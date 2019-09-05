#!/usr/bin/env python3
import subprocess
import sys
import os

dir = sys.argv[1].rstrip('/')
for filename in os.listdir(dir):
    editedName = dir + '/' + filename
    if ".bam" in filename and ".bai" not in filename:
        subprocess.call("python3.6 GatkScript.py %s" % editedName, shell=True)
    print (editedName)

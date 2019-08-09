#!/usr/bin/env python3
import subprocess
import os

dir = "GATKDATA"
for filename in os.listdir(dir):
    editedName = dir + '/' + filename
    if ".bam" in filename and ".bai" not in filename:
        subprocess.call("python3 GatkScript.py %s" % editedName, shell=True)
    print (editedName)

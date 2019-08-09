# Mutect2Mitomaster
For variant calling, consensus generation, and mitomaster report.

This scripts takes aligned bam files and uses Mutect2 to do variants calling on each file. It generates a VCF with all variants and a VCF with variants above 5%. A consensus sequence is created based on the filtered VCF and is uploaded to Mitomaster. A report from Mitomaster is saved in the results file.

GatkScript.py is the main script and mitoRequest passes bam files in a directory to GatkScript.py.

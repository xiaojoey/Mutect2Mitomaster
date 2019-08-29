# Mutect2Mitomaster
For variant calling, consensus generation, and mitomaster report.

This scripts takes aligned bam files and uses Mutect2 to do variant calling on each file. It generates a VCF with all variants and a VCF with variants above 5%. A consensus sequence is created based on the filtered VCF and is uploaded to Mitomaster. A report from Mitomaster is saved in the results folder.

GatkScript.py is the main script and mitoRequest.py passes bam files in a directory to GatkScript.py.

LRVC.py is a script for PacBio Pbaligned CCS sequences. It modifies the header for the bam file to make the PacBio data compatible with the rest of the pipeline.

bam2fasta.py converts all the bam files in a folder into fasta files. 

Usage:

```
python GatkScript.py bamFile
python mitoRequest.py folderOfBamFiles
python LRVC.py bamFile filterLevel referenceFasta resultDir
python bam2fasta.py folderOfBamFiles
```

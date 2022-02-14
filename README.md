# Mutect2Mitomaster

### Original Publication:

Yang, Z., Slone, J., Wang, X., Zhan, J., Huang, Y., Namjou, B., Kaufman, K. M., Pauciulo, M., Harley, J. B., Muglia, L. J., Chepelev, I., & Huang, T. (2021). Validation of low-coverage whole-genome sequencing for mitochondrial DNA variants suggests mitochondrial DNA as a genetic cause of preterm birth. Human Mutation, 42, 1602– 1614. https://doi.org/10.1002/humu.24279

## Quick Summary

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
python getCoverage.py folderOfFoldersOfBams folderOfFoldersOfFolderMitoMasterReport
```

## Requirements and Dependencies

System Requirement: Unix system or virtual env

There are two sets of dependencies: the system dependencies and the python dependencies. The python depedencies should be installed using pip.

| Dependencies | Version | 
| -----------|----- |
| htslib | 1.9 |
| samtools | 1.9 |
| bcftools | 1.9 |
| tabix | 1.9 |
| bgzip | 1.9 |
| Java | 12 |
| gatk | 4.1.2.0 |
| python | 3.6 |


| Python Dependencies | Version |
| -----------|----- |
| pandas | 0.25.1 |
| requests | 2.22.0 |
| openpyxl | 2.6.2 |

## Setup Instructions

1. Add htslib, samtools, bcftools to PATH
2. Place mitoRequest.py, GatkScript.py, sequence.fasta and associated index/dict files inside gatk4.1.2.0 folder 
3. Setup human genome reference files
   1. Make folder for reference files called hg38 inside gatk4.1.2.0 folder
   2. Reference files can be found at https://console.cloud.google.com/storage/browser/genomics-public-data/resources/broad/hg38/v0/?pli=1
   3. Place resources-broad-hg38-v0-Homo_sapiens_assembly38.fasta  and  resources-broad-hg38-v0-Mills_and_1000G_gold_standard.indels.hg38.vcf inside hg38
   4. Include the associated dictionary and index files

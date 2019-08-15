# False posiitives warning
import subprocess
import requests
import sys
import os

inputBam = sys.argv[1]
filterLevel = float(sys.argv[2])
sampleName = inputBam.split('.bam')[0]
resultDir = sampleName + '_result'
subprocess.call("mkdir %s" % resultDir, shell=True)

mtRef = sys.argv[3]

subprocess.call("samtools view -H %s > %s.sam" %
                (inputBam, sampleName), shell=True)

print("Header extracted")

headerFile = open("%s.sam" % sampleName, "r")

oldHeader = headerFile.read()
start = oldHeader.split('PU:')[0]
end = oldHeader.split('PU:')[1]

newHeader = start + 'SM:Sample\tPU:' + end
print(newHeader)

headerFile = open("%s.sam" % sampleName, "w")
headerFile.write(newHeader)
headerFile.close()

reheaderFile = "%s.reheader.bam" % sampleName

subprocess.call("samtools reheader %s.sam %s.bam > %s ; samtools index %s ; rm %s.sam" %
                (sampleName, sampleName, reheaderFile, reheaderFile, sampleName), shell=True)

subprocess.call("./gatk Mutect2 -R %s -L NC_012920.1 --mitochondria-mode  true -I %s -O %s/%s.raw.vcf; rm %s*" %
                (mtRef, reheaderFile, resultDir, sampleName, reheaderFile), shell=True)

finalVCF = "%s.%s.vcf" % (sampleName, filterLevel)
subprocess.call("bcftools view -i 'MAX(FORMAT/AF)>%s' %s/%s.raw.vcf > %s/%s" %
                (filterLevel, resultDir, sampleName, resultDir, finalVCF), shell=True)

subprocess.call("./gatk VariantsToTable -V %s/%s -F CHROM -F POS -F REF -F ALT -F TYPE -GF AF -O %s/%s.table" %
                (resultDir, finalVCF, resultDir, finalVCF), shell=True)

subprocess.call("cd %s; bgzip %s ; tabix -p vcf %s.gz" %
                (resultDir, finalVCF, finalVCF), shell=True)

print("\tVCF Zipped and indexed\n")

consensusFasta = "%s/%s.%s.consensus.fasta" % (resultDir, sampleName, filterLevel)

subprocess.call("cat %s | bcftools consensus %s/%s.gz > %s" %
                (mtRef, resultDir, finalVCF, consensusFasta), shell=True)

print("\tconsensus generated")

result = open(
    "%s/%s.%s.report.txt" % (resultDir, sampleName, filterLevel), "w")

try:
    response = requests.post("https://mitomap.org/mitomaster/websrvc.cgi", files={"file": open(
        consensusFasta), 'fileType': ('', 'sequences'), 'output': ('', 'detail')})
    print(str(response.content, 'utf-8'))
    result.write(str(response.content, 'utf-8'))
except requests.exceptions.HTTPError as err:
    print("HTTP error: " + err)
except:
    print("Error")
result.close()

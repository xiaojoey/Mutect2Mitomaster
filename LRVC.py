# False posiitives warning
import subprocess
import requests
import sys
import os


def getBamName(fileName):
    splitList = fileName.split('/')
    for i in range(len(splitList) - 1, -1, -1):
        if splitList[i] != "":
            return splitList[i]
    raise Exception("\"%s\" is not a valid file name" % fileName)


inputBam = sys.argv[1]
filterLevel = float(sys.argv[2])
mtRef = sys.argv[3]
resultDir = sys.argv[4]

sampleName = getBamName(inputBam).split('.bam')[0]

versionCounter = 2
while os.path.isdir(resultDir):
    resultDir = "%s%s" % (sys.argv[4], versionCounter)
    versionCounter += 1

subprocess.call("mkdir %s" % resultDir, shell=True)


subprocess.call("samtools view -H %s > %s/%s.sam" %
                (inputBam, resultDir, sampleName), shell=True)

print("Header extracted")

headerName = "%s/%s.sam" % (resultDir, sampleName)

headerFile = open(headerName, "r")

oldHeader = headerFile.read()
start = oldHeader.split('PU:')[0]
end = oldHeader.split('PU:')[1]

newHeader = start + 'SM:Sample\tPU:' + end
print(newHeader)

headerFile = open(headerName, "w")
headerFile.write(newHeader)
headerFile.close()

reheaderFile = "%s/%s.reheader.bam" % (resultDir, sampleName)

subprocess.call("samtools reheader %s %s > %s ; samtools index %s ; rm %s" %
                (headerName, inputBam, reheaderFile, reheaderFile, headerName), shell=True)

rawVCF = "%s/%s.raw.vcf" % (resultDir, sampleName)
subprocess.call("./gatk Mutect2 -R %s -L NC_012920.1 --mitochondria-mode  true -I %s -O %s; rm %s*" %
                (mtRef, reheaderFile, rawVCF, reheaderFile), shell=True)

finalVCF = "%s/%s.%s.vcf" % (resultDir, sampleName, filterLevel)
subprocess.call("bcftools view -i 'MAX(FORMAT/AF)>%s' %s > %s" %
                (filterLevel, rawVCF, finalVCF), shell=True)

variantTable = "%s.table" % finalVCF
subprocess.call("./gatk VariantsToTable -V %s -F CHROM -F POS -F REF -F ALT -F TYPE -GF AF --show-filtered true -O %s" %
                (finalVCF, variantTable), shell=True)

subprocess.call("bgzip %s ; tabix -p vcf %s.gz" %
                (finalVCF, finalVCF), shell=True)

print("\tVCF Zipped and indexed\n")

consensusFasta = "%s/%s.%s.consensus.fasta" % (resultDir, sampleName, filterLevel)

subprocess.call("cat %s | bcftools consensus %s.gz > %s" %
                (mtRef, finalVCF, consensusFasta), shell=True)

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

import subprocess
import requests
import sys
import os

inputBam = sys.argv[1]
sampleName = inputBam.split('.bam')[0].split('/')[1]
if not os.path.isdir("results"):
    os.mkdir("results")

resultDir = "results/%s" % sampleName

subprocess.call("mkdir %s" % resultDir, shell=True)
print(sampleName)

genomeRef = "hg38/resources-broad-hg38-v0-Homo_sapiens_assembly38.fasta"
refSites = "hg38/resources-broad-hg38-v0-Mills_and_1000G_gold_standard.indels.hg38.vcf"
mtRef = "sequence.fasta"

rawVCF = "%s/%s.raw.vcf" % (resultDir, sampleName)
filteredVCF = "%s/%s.filtered.vcf" % (resultDir, sampleName)
f2VCF = "%s/%s.f2.vcf" % (resultDir, sampleName)
outputTable = "%s/%s.rg.table" % (resultDir, sampleName)
rgBam = "%s/%s.rg.bam" % (resultDir, sampleName)
recalBam = "%s/%s.rg.recal.bam" % (resultDir, sampleName)
consensusFasta = "%s/%s_consensus.fasta" % (resultDir, sampleName)
variantTable = "%s/variants.table" % resultDir

subprocess.call(["ls", "-l"])

subprocess.call("./gatk AddOrReplaceReadGroups -I %s -R %s -O %s -LB nextera -PL illumina -PU BKCM7 -SM sample -SO coordinate --CREATE_INDEX true" %
                (inputBam, genomeRef, rgBam), shell=True)

print("\tAddOrReplaceReadGroups Done")


subprocess.call("./gatk Mutect2 -R %s -L chrM --mitochondria-mode true -I %s -O %s" %
                (genomeRef, rgBam, rawVCF), shell=True)


print("\tVariants Called")

subprocess.call("./gatk FilterMutectCalls -R %s -min-allele-fraction .05 -V %s -O %s" %
                (genomeRef, rawVCF, filteredVCF), shell=True)

print("\tFirst Mutect Filter Done")


subprocess.call("bcftools view -i 'MAX(FORMAT/AF)>.05' %s > %s" %
                (filteredVCF, f2VCF), shell=True)

print("\tFive percent filter applied")

subprocess.call("./gatk VariantsToTable -V %s -F POS -F REF -F ALT -F TYPE -GF AF --show-filtered true -O %s" %
                (f2VCF, variantTable), shell=True)

print("\tVariantTable made")

subprocess.call("bgzip %s ; tabix -p vcf %s.gz" %
                (f2VCF, f2VCF), shell=True)

print("\tVCF Zipped and indexed")

subprocess.call("cat %s | bcftools consensus %s.gz > %s" %
                (mtRef, f2VCF, consensusFasta), shell=True)

print("\tconsensus generated")

result = open(
    "%s/%s_report.txt" % (resultDir, sampleName), "w")
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

os.chdir(resultDir)

subprocess.call("pwd; rm *.rg.*; rm *.raw*", shell=True)

import subprocess
import sys
import os
import csv


class sample:
    def __init__(self, coverage, name):
        self.coverage = coverage
        self.name = name

    def row(self):
        result = [self.name, self.coverage]
        return result


class hap:
    def __init__(self, group, name):
        self.group = group
        self.name = name

    def row(self):
        result = [self.name, self.group]
        return result


class final:
    def __init__(self, group, name, coverage):
        self.group = group
        self.name = name
        self.coverage = coverage

    def row(self):
        result = [self.name, self.coverage, self.group]
        return result


sampleArr = []
hapArr = []
finalArr = []

dir = sys.argv[1].rstrip('/')
hapDir = sys.argv[2].rstrip('/')

for filename in os.listdir(dir):
    editedName = dir + '/' + filename
    sampleName = editedName.split('/')[-1].split('-')[0]
    if ".bam" in filename and ".bai" not in filename:
        command = "samtools depth %s | awk '{sum+=$3} END {print sum}'" % editedName
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        resultStr = result.stdout.decode('utf-8')
        resultNum = (int(resultStr.rstrip()) / 16569)
        newSample = sample(resultNum, sampleName)
        sampleArr.append(newSample)
        # print("The average depth at %s is %s" % (sampleName, resultNum))

for largeDir in os.listdir(hapDir):
    newLargeDir = hapDir + '/' + largeDir
    if os.path.isdir(newLargeDir):
        for fileDir in os.listdir(newLargeDir):
            newFileDir = newLargeDir + '/' + fileDir
            if os.path.isdir(newFileDir):
                for file in os.listdir(newFileDir):
                    if "report.txt" in file:
                        filePath = newFileDir + '/' + file
                        sampleName = filePath.split('/')[-1].split('-')[0]
                        with open(filePath) as hap_file:
                            hap_reader = csv.reader(hap_file, delimiter='\t')
                            firstRow = next(hap_reader)
                            target_column = 0
                            i = 0
                            for col in firstRow:
                                if "verbose_haplogroup" in col:
                                    target_column = i
                                i += 1
                            secondRow = next(hap_reader)
                            group_name = secondRow[target_column]
                            hapSample = hap(group_name, sampleName)
                            hapArr.append(hapSample)


# for hap in hapArr:
#     print(hap.row())

for samp in sampleArr:
    combined = final("a", "a", "a")
    for hap in hapArr:
        if samp.name == hap.name:
            combined.name = samp.name
            combined.coverage = samp.coverage
            combined.group = hap.group
    finalArr.append(combined)

# for i in finalArr:
#     print(i.row())
with open('results.csv', 'w') as f:
    writer = csv.writer(f, dialect='excel')
    writer.writerow(["Sample Name", "Coverage", "verbose_haplogroup"])
    for sample in finalArr:
        writer.writerow(sample.row())

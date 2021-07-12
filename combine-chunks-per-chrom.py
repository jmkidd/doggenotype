# run-chunk.py

# program to make genomicsDB from GVCF and call genotypes
# for a given chunk of the genome

import doggenotype
import os
import sys
import argparse
import gzip

# SETUP

parser = argparse.ArgumentParser(description='combine genome chunks')

parser.add_argument('--chunkdir', type=str,help='directory of chunks',required=True)
parser.add_argument('--chunklist', type=str,help='file of chunks in order',required=True)
parser.add_argument('--chrm', type=str,help='chromosome to do',required=True)
parser.add_argument('--out', type=str,help='name of output .vcf.gz file for chromosome',required=True)



args = parser.parse_args()

#####################################################################

myData = {} # dictionary for keeping and passing information

myData['chunkDir'] = args.chunkdir
myData['chunkList'] = args.chunklist
myData['chrom'] = args.chrm
myData['outFileName'] = args.out

myData['outFileNameComplete'] = myData['outFileName'] + '.complete'



if myData['chunkDir'][-1] != '/':
   myData['chunkDir'] += '/'

# read in chunks to do
chunksToDo = []
inFile = open(myData['chunkList'],'r')
for line in inFile:
    line = line.rstrip()
    line = line.split()
    c = line[0]
    b = int(line[1])
    e = int(line[2])    
    r = line[0] + ':' + line[1] + '-' + line[2]
    if c == myData['chrom']:
        chunksToDo.append([c,b,e,r])
inFile.close()
print('read in %i chunks to do' % len(chunksToDo))

print('checking that all chunks are complete...',flush=True)

for chunk in chunksToDo:
    r = chunk[3]
    completeToken = myData['chunkDir'] + r + '.complete'
    if os.path.isfile(completeToken) is False:
        print('ERROR!! Could not find %s' % completeToken)
        sys.exit()
print('all complete! ready to merge!', flush = True)



print('opening output file %s' % myData['outFileName'], flush=True)
outFile = doggenotype.open_bgzip_write(myData['outFileName'],threads=3)

for i in range(len(chunksToDo)):
    if i == 0:
        s = chunksToDo[i][1]
    else:
        s = chunksToDo[i][1] + 1000 + 1 # the overlap..    
    if i == len(chunksToDo):
        e = chunksToDo[i][2]
    else:
        e = chunksToDo[i][2] - 1000

    print('doing...',i,chunksToDo[i],s,e,flush=True)
    
    f = myData['chunkDir'] + chunksToDo[i][3]  + '.vcf.gz'
    inFile = gzip.open(f,'rt')
    for line in inFile:
        if line[0] == '#' and i == 0:
            outFile.write(line)
            continue
        elif line[0] == '#':
            continue        
        # get start
        tmp = line[0:100]
        tmp = tmp.split()
        p = int(tmp[1])
        if p >= s and p <= e:
            outFile.write(line)
    inFile.close()
outFile.close()

cmd = 'touch %s ' % myData['outFileNameComplete']
print(cmd)
doggenotype.runCMD(cmd)


# run-chunk.py

# program to make genomicsDB from GVCF and call genotypes
# for a given chunk of the genome

import doggenotype
import os
import sys
import argparse
import time

# SETUP

parser = argparse.ArgumentParser(description='process genome chunk')

parser.add_argument('--region', type=str,help='region string chr:start-end',required=True)
parser.add_argument('--samples', type=str,help='sample-name map file',required=True)

parser.add_argument('--ref', type=str,help='genome fasta with dictionary and .fai',required=True)
parser.add_argument('--tmpdir', type=str,help='tmp dir for running',required=True)
parser.add_argument('--finaldir', type=str,help='final dir for output',required=True)
args = parser.parse_args()

#####################################################################

myData = {} # dictionary for keeping and passing information

myData['tmpDir'] = args.tmpdir
myData['finalDir'] = args.finaldir
myData['ref'] = args.ref
myData['region'] = args.region
myData['samples'] = args.samples


if myData['tmpDir'][-1] != '/':
   myData['tmpDir'] += '/'
if myData['finalDir'][-1] != '/':
   myData['finalDir'] += '/'

myData['finalVCF'] = myData['finalDir'] + myData['region'] + '.vcf.gz'
myData['completeToken'] = myData['finalDir'] + myData['region'] + '.complete'
myData['logFileName'] = myData['finalDir'] + myData['region'] + '.genotype.log'

# if log file exists, then there is partial processing so not sure we want to redo and overwrite
# safe to just quite and letter user deal with it

if os.path.isfile(myData['logFileName']) is True:
    print('ERROR!!!')
    print('%s exists.  Do you really want to rerun this pipeline?' % myData['logFileName'] )
    print('ERROR!!!')
    sys.exit()

myData['logFile'] = open(myData['logFileName'],'w')

# add initial infoto log
doggenotype.init_log(myData)

# make sure programs are availble
doggenotype.check_prog_paths(myData)

# check space
doggenotype.check_dir_space(myData)


# run import
doggenotype.run_GenomicsDBImport(myData)

# run genotype
doggenotype.run_GenotypeGVCFs(myData)


# clean up and get elapsed time!
doggenotype.remove_tmp_dir(myData)

cmd = 'touch %s ' % myData['completeToken']
print(cmd,flush=True)
myData['logFile'].write(cmd + '\n')
doggenotype.runCMD(cmd)

myData['endTime'] = time.localtime()
myData['tEnd'] = time.time()
t = time.strftime("%a, %d %b %Y %H:%M:%S", myData['endTime'])
myData['logFile'].write('\nEnded!\n%s\n' % t)

elapsedTime = myData['tEnd'] - myData['tStart'] # this is in nanoseconds??

# convert to minutes
elapsedTime= elapsedTime / 60
# convert to hours
elapsedTime = elapsedTime / 60

myData['logFile'].write('Elapsed time:\n%s hours\n' % elapsedTime)
myData['logFile'].close()


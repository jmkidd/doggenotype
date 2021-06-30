# functions for running genotype of gVCF

import sys
import subprocess
import os
import argparse
import time
import socket
import shutil

# Helper function to run commands, handle return values and print to log file
def runCMD(cmd):
    val = subprocess.Popen(cmd, shell=True).wait()
    if val == 0:
        pass
    else:
        print('command failed')
        print(cmd)
        sys.exit(1)
###############################################################################
# Helper function to run commands, handle return values and print to log file
def runCMD_output(cmd):
    val = subprocess.Popen(cmd, text=True, shell=True, stdout = subprocess.PIPE)
    resLines = []
    for i in val.stdout:
       i = i.rstrip()
       resLines.append(i)
    return resLines
#############################################################################        
# setup paths to default programs to use and checks for required programs
def check_prog_paths(myData):        
    myData['logFile'].write('\nChecking for required programs...\n')
    
    for p in ['gatk']:
        if shutil.which(p) is None:
            s = p + ' not found in path! please fix (module load?)'
            print(s, flush=True)
            myData['logFile'].write(s + '\n')
            myData['logFile'].close()        
            sys.exit()
        else:
            myData['logFile'].write('%s\t%s\n' % (p,shutil.which(p)))
            
    myData['logFile'].flush()              
############################################################################# 
def init_log(myData):
    k = list(myData.keys())
    k.sort()
    myData['startTime'] = time.localtime()
    myData['tStart'] = time.time()
    t = time.strftime("%a, %d %b %Y %H:%M:%S", myData['startTime'])        
    myData['logFile'].write(t + '\n')
    
    hn = socket.gethostname()
    myData['logFile'].write('Host name: %s\n' % hn)
    print('Host name: %s\n' % hn,flush=True)
    
    myData['logFile'].write('\nInput options:\n')
    for i in k:
        if i in ['logFile']:
            continue        
        myData['logFile'].write('%s\t%s\n' % (i,myData[i]))                
    myData['logFile'].flush()  
############################################################################# 
############################################################################# 
def check_dir_space(myData,checkSize = True):
    myData['logFile'].write('\nchecking file systems\n')
    
    # check tmp dir
    if os.path.isdir(myData['tmpDir']) is False:
        s = myData['tmpDir'] + ' is not found! making it'        
        print(s,flush=True)
        myData['logFile'].write(s + '\n')
        myData['logFile'].flush()        
        
        cmd = 'mkdir -p %s ' % myData['tmpDir']
        print(cmd,flush=True)
        myData['logFile'].write(cmd + '\n')
        myData['logFile'].flush()  
        runCMD(cmd)              

    if os.path.isdir(myData['finalDir']) is False:
        s = myData['finalDir'] + ' is not found! please check'
        print(s,flush=True)
        myData['logFile'].write(s + '\n')
        myData['logFile'].flush()        
        sys.exit()
        
    cmd = 'df -h %s' % myData['tmpDir']
    o = runCMD_output(cmd)
    myData['logFile'].write(cmd + '\n')
    myData['logFile'].write(o[0] + '\n')
    myData['logFile'].write(o[1] + '\n')
    myData['logFile'].write('\n')

    cmd = 'df -h %s' % myData['finalDir']
    o = runCMD_output(cmd)
    myData['logFile'].write(cmd + '\n')
    myData['logFile'].write(o[0] + '\n')
    myData['logFile'].write(o[1] + '\n')
    
    stats =  os.statvfs(myData['tmpDir'])
    freeSpace = stats.f_frsize * stats.f_bavail 
    freeSpaceGb = freeSpace / (1024**3)
    if freeSpaceGb < 20.0:
        s = 'less than 20 Gb free in tmpDir! %f\n' % freeSpaceGb
        print(s,flush=True)
        myData['logFile'].write(s + '\n')
        myData['logFile'].flush()
        if checkSize is True:  # kill job
            s = 'ERROR!! less than 20 Gb free in tmpDir! %f\n Exiting Script!' % freeSpaceGb
            print(s,flush=True)
            myData['logFile'].write(s + '\n')
            myData['logFile'].flush()
            myData['logFile'].close()
            sys.exit()
    else:
        s = 'more than 20 Gb free in tmpDir! %f\n Ok!' % freeSpaceGb
        print(s,flush=True)
        myData['logFile'].write(s + '\n')
        myData['logFile'].flush()
        
    stats =  os.statvfs(myData['finalDir'])
    freeSpace = stats.f_frsize * stats.f_bavail 
    freeSpaceGb = freeSpace / (1024**3)
    if freeSpaceGb < 50.0:
        s = 'less than 50 Gb free in final dir! %f\n!' % freeSpaceGb
        print(s,flush=True)
        myData['logFile'].write(s + '\n')
        myData['logFile'].flush()
        if checkSize is True:  # kill job
            s = 'ERROR less than 50 Gb free in final dir! %f\n! Exiting!' % freeSpaceGb
            print(s,flush=True)
            myData['logFile'].write(s + '\n')
            myData['logFile'].flush()
            myData['logFile'].close()
            sys.exit()
    else:
        s = 'more than 50 Gb free in final dir! %f\n Ok!' % freeSpaceGb
        print(s,flush=True)
        myData['logFile'].write(s + '\n')
        myData['logFile'].flush()        
    myData['logFile'].flush()  
############################################################################# 
def remove_tmp_dir(myData,run=True):
    #setup, run, and apply BQSR
    s = 'starting remove tmp dir: %s ' % (myData['tmpDir'])
    print(s,flush=True)
    myData['logFile'].write('\n' + s + '\n')
    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())        
    myData['logFile'].write(t + '\n')
    myData['logFile'].flush()
    
    check_dir_space(myData,checkSize = False)
    
    if run is True:
        shutil.rmtree(myData['tmpDir']) 
        s = 'removed!'
        print(s,flush=True)
        myData['logFile'].write('\n' + s + '\n')
        t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())        
        myData['logFile'].write(t + '\n')
        myData['logFile'].flush()
    else:
        s = 'skipping rmtree!'
        print(s,flush=True)
        myData['logFile'].write('\n' + s + '\n')
        t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())        
        myData['logFile'].write(t + '\n')
        myData['logFile'].flush()
############################################################################# 
def run_GenomicsDBImport(myData):
    s = 'Starting GenomicsDBImport'
    print(s,flush=True)
    myData['logFile'].write('\n' + s + '\n')
    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())        
    myData['logFile'].write(t + '\n')
    myData['logFile'].flush()              

    myData['genomicsdb'] = myData['tmpDir'] + 'chunkDB'

    cmd = 'gatk --java-options "-Xmx5g -Xms5g" GenomicsDBImport '
    cmd += ' --tmp-dir %s ' % myData['tmpDir']
    cmd += ' --L %s ' % myData['region']
    cmd += ' --sample-name-map %s ' % myData['samples']
    cmd += ' --batch-size 50 '
    cmd += ' --genomicsdb-workspace-path %s ' %  myData['genomicsdb']


    print(cmd,flush=True)
    myData['logFile'].write(cmd + '\n')
    myData['logFile'].flush()              
    runCMD(cmd)        

    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())        
    myData['logFile'].write(t + '\n')        
    myData['logFile'].flush()              
############################################################################# 
def run_GenotypeGVCFs(myData):
    s = 'Starting GenotypeGVCFs'
    print(s,flush=True)
    myData['logFile'].write('\n' + s + '\n')
    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())        
    myData['logFile'].write(t + '\n')
    myData['logFile'].flush()              

    cmd = 'gatk --java-options "-Xmx5g -Xms5g" GenotypeGVCFs '
    cmd += ' --tmp-dir %s ' % myData['tmpDir']
    cmd += ' -R %s ' % myData['ref']
    cmd += ' -O %s ' % myData['finalVCF']
    cmd += ' -V gendb://%s' % myData['genomicsdb']

    print(cmd,flush=True)
    myData['logFile'].write(cmd + '\n')
    myData['logFile'].flush()              
    runCMD(cmd)        

    t = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())        
    myData['logFile'].write(t + '\n')        
    myData['logFile'].flush()              
############################################################################# 

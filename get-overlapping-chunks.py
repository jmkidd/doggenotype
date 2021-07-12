import sys



ref='/home/jmkidd/links/kidd-lab/genomes/UU_Cfam_GSD_1.0/ref-Y/UU_Cfam_GSD_1.0_ROSY.fa'
refFAI = ref + '.fai'

chromLens = {}
inFile = open(refFAI,'r')
for line in inFile:
    line = line.rstrip()
    line = line.split()
    c = line[0]
    l = int(line[1])
    chromLens[c] = l
inFile.close()

chromNames = []
for i in range(1,39):
    c = 'chr' + str(i)
    chromNames.append(c)


windowSize = 1000000
overLapSize = 2000

outFile = open('auto.overlap.chunks.txt','w')
for c in chromNames:
    cLen = chromLens[c]
    print(c,cLen)
    ws = 1
    we = ws + windowSize -1
    while True:
        if we >= cLen:
            we = cLen
            outFile.write('%s\t%i\t%i\n' % (c,ws,we))
            break
        else:
            outFile.write('%s\t%i\t%i\n' % (c,ws,we))
            ws = we - overLapSize
            we = ws + overLapSize +  windowSize


for c in ['chrX']:
    cLen = 6605250
    print(c,cLen)
    ws = 1
    we = ws + windowSize -1
    while True:
        if we >= cLen:
            we = cLen
            outFile.write('%s\t%i\t%i\n' % (c,ws,we))
            break
        else:
            outFile.write('%s\t%i\t%i\n' % (c,ws,we))
            ws = we - overLapSize
            we = ws + overLapSize +  windowSize
outFile.close()


outFile = open('chrX.overlap.chunks.txt','w')
for c in ['chrX']:
    cLen = chromLens[c]
    print(c,cLen)
    ws = 6605251
    we = ws + windowSize -1
    while True:
        if we >= cLen:
            we = cLen
            outFile.write('%s\t%i\t%i\n' % (c,ws,we))
            break
        else:
            outFile.write('%s\t%i\t%i\n' % (c,ws,we))
            ws = we - overLapSize
            we = ws + overLapSize +  windowSize

outFile.close()



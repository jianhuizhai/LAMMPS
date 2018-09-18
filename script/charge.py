import numpy as np
import sys

OldNewFileName = sys.argv[1]
skipline = int(sys.argv[2])
NewFileName = sys.argv[3]      # NewFileName is the name of new file

print('old file name is', OldNewFileName)
print('new file name is', NewFileName)

data = np.loadtxt(OldNewFileName, skiprows=(skipline))
newfile = open(NewFileName, 'w')

f = open(OldNewFileName,'r')
for i in range(skipline):
    line = f.readline()
    newfile.write(line)
f.close()

for i in range(len(data)):
    if(int(data[i][1])==1):
        charge = 2
    else:
        charge = -2
    line = '%10i %5i %5i %20.8f %20.8f %20.8f\n'%(i+1, data[i][1], charge, data[i][2], data[i][3], data[i][4])
    newfile.write(line)
newfile.close()
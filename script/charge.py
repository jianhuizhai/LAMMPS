import numpy as np
import sys


OldFileName = sys.argv[1]
# skipline = int(sys.argv[2])
NewFileName = sys.argv[2]      # NewFileName is the name of new file

print('old file name is', OldFileName)
print('new file name is', NewFileName)

# for skipline you can use if command for different crystal lattices.
# here 16 is used for a lattice type contains two atom types.
skipline = 16

data = np.loadtxt(OldFileName, skiprows=(skipline))
newfile = open(NewFileName, 'w')

oldfile = open(OldFileName,'r')
for i in range(skipline):
    if (i == skipline-2):
        line = "Atoms # charge\n"
    elif(i == skipline-1):
        line = "\n"
    else:
        line = oldfile.readline()
    newfile.write(line)
oldfile.close()

totalcharge = 0.0
for i in range(len(data)):
    if(int(data[i][1])==1):
        charge = 1.7
    else:
        charge = -1.7
    totalcharge = totalcharge + charge
    line = '%10i %5i %8.1f %16.8f %16.8f %16.8f\n'%(i+1, data[i][1], charge, data[i][2], data[i][3], data[i][4])
    newfile.write(line)
newfile.close()

print('total charge is', totalcharge)
print('The file is successfully changed!!')
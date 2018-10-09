import numpy as np
import sys


OldFileName = sys.argv[1]
# skipline = int(sys.argv[2])
NewFileName = sys.argv[2]      # NewFileName is the name of new file

print('old file name is', OldFileName)
print('new file name is', NewFileName)

# for skipline you can use if command for different crystal lattices.
# here 16 is used for a lattice type contains two atom types.

skipmass = int(input("the skipline for mass (the line do not contains Masses keyword): "))
skipline = 16

data = np.loadtxt(OldFileName, skiprows=(skipline))
newfile = open(NewFileName, 'w')

oldfile = open(OldFileName,'r')

for i in range(skipmass):
    line = oldfile.readline()
    newfile.write(line)

line = 'Masses'+'\n'
newfile.write(line)
line = '\n'
newfile.write(line)
line = '           1   24.30500000    # Mg'+'\n'
newfile.write(line)
line = '           2   15.99900000    # O'+'\n'
newfile.write(line)
line = '\n'
newfile.write(line)
line = "Atoms # charge\n"
newfile.write(line)
line = '\n'
newfile.write(line)
oldfile.close()

totalcharge = 0.0
for i in range(len(data)):
    if(int(data[i][1])==1):
        charge = 1.7
    else:
        charge = -1.7
    totalcharge = totalcharge + charge
    line = '%10i %5i %8.1f %16.8f %16.8f %16.8f\n'%(data[i][0], data[i][1], charge, data[i][2], data[i][3], data[i][4])
    newfile.write(line)
newfile.close()

print('total charge is', totalcharge)
print('The file is successfully changed!!')
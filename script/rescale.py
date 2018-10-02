import sys
import numpy as np

OldFileName = sys.argv[1]
# skipline = int(sys.argv[2])
NewFileName = sys.argv[2]      # NewFileName is the name of new file

skipline = 16   # this number is for atoms system with two type atoms.

# print('type which axis is compressed or tension')
axis     = raw_input('type which axis is compressed or tension: ')
print('axis=',axis)
print('old file name is', OldFileName)
print('new file name is', NewFileName)

print('type compression or tension ratio')
ratio = float(input())

if(axis == 'x'):
    specifiedLine = 6
elif(axis == 'y'):
    specifiedLine = 7
else:
    specifiedLine = 8

data = np.loadtxt(OldFileName, skiprows=(skipline))
newfile = open(NewFileName, 'w')

oldfile = open(OldFileName,'r')
for i in range(skipline):
    if(i== (specifiedLine-1)):
        line = oldfile.readline()
        listLine = list(line)
        listLine[22:33] = str('%11.8f' %(float(line[22:33])*ratio))
        line = ''.join(listLine)
        print(line)
    else:
        line = oldfile.readline()
    
    newfile.write(line)
oldfile.close()


for i in range(len(data)):
    
    if( axis == 'x' ):
        data[i][2] = data[i][2]*ratio
    elif( axis == 'y' ):
        data[i][3] = data[i][3]*ratio
    else:
        data[i][4] = data[i][4]*ratio

    
    line = '%10i %5i %16.8f %16.8f %16.8f\n'%(i+1, data[i][1], data[i][2], data[i][3], data[i][4])
    newfile.write(line)
newfile.close()

print('The file is succefully changed!')
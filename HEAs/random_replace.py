'''This code is used to generate HEAs with 5 atom types for molecular simulation.'''
'''It is used with HEAs.sh together. It can be extended to other atom types.'''
import numpy as np
import sys
import random

linecommon = '========================================================================================'
#========================================================================================
OldFileName = sys.argv[1]
#NewFileName = sys.argv[2]      # NewFileName is the name of new file

#-----------------------------------------------------------------------------
# Initialize the random number generator. Random number sequence will same if seed does not change.
seed = input("The number of seed : ")
random.seed( int(seed) )
print(linecommon)

#-----------------------------------------------------------------------------
NewFileName = OldFileName+'.'+seed
print('old file name is', OldFileName)
print('new file name is', NewFileName)
print(linecommon)

skipline = 19
data = np.loadtxt(OldFileName, skiprows=(skipline))

#========================================================================================
newfile = open(NewFileName, 'w')
oldfile = open(OldFileName,'r')

for i in range(skipline):
    line = oldfile.readline()
    #if(i == 3):
    #    line = line.replace("1","5") # There are 5 atom types.
    newfile.write(line)

oldfile.close()

#========================================================================================
totalAtoms = len(data)
print('totalAtoms   = ', totalAtoms)
replaceAtoms = int(0.2*totalAtoms)
print('replaceAtoms = ', replaceAtoms)

atoms_id=list(data[:,0].astype(int))     # astype(int) changes float to int.

# from atoms_id random selct 4*replaceAtoms and put it in slice
slice = np.array(random.sample(atoms_id, replaceAtoms*4))  
print('len(slice)   = ',len(slice))
# print('slice = ', slice)
print(linecommon)

data[:,1] = 1    # make all the atom types are 1.
for i in range(4):
    begin = i * replaceAtoms
    end   = (i+1)*replaceAtoms
    #print('i = %2i, begin = %8i, end = %8i, lens = %8i' %(i, begin, end, end-begin) )
    print('%-8i atoms change to type %2i' %(end-begin, i+2))
    #for j in range(begin,end):
    #    if(slice[j]>=4000):
    #        print(slice[j])
# number in slice is begining from 1, -1 to make it consistent with python agreement
# slice[0:2] contains slice[0] and slice[1]. number is end-1+1-begin = end - begin
    data[:,1][slice[begin:end]-1] = i+2

#data[:,1][slice[0*replaceAtoms:1*replaceAtoms]] = 2
#data[:,1][slice[1*replaceAtoms:2*replaceAtoms]] = 3
#data[:,1][slice[2*replaceAtoms:3*replaceAtoms]] = 4
#data[:,1][slice[3*replaceAtoms:4*replaceAtoms]] = 5

#print (slice)  
#=============================================================================================
for i in range(len(data)):
    line = '%10i %5i %16.8f %16.8f %16.8f\n'%(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4])
    newfile.write(line)
newfile.close()

print(linecommon)

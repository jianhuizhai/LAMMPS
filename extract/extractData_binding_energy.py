import numpy as np
import os
import linecache
import subprocess  # for python3
# import commands   ## for python2

#=============================================================================================================
linecommon = "==============================================================================================="

#=============================================================================================================
print(linecommon)
print("    1 --------- noclimb.lmp")
print("    2 --------- climb.lmp")
print("    3 --------- distribution.dat")
flag = input("The reference system : ")

skiplines = 16
if(flag == '1'):
        filename = 'noclimb.lmp'
elif(flag == '2' ):
        filename = 'climb.lmp'
elif( flag == '3' ):
        filename = 'distribution.dat'
        skiplines = 0
else:
        exit("Unkown reference system!!!")

#=============================================================================================================
#                               load data file
#=============================================================================================================
print(linecommon)
print("load %s ..." %filename)

atomid, atom_type, x, y, z = np.loadtxt(filename, skiprows=skiplines, usecols=(0,1,2,3, 4), unpack=True)

energy_info = open('energy_info.dat', 'w')

for folder in os.listdir():
    
    if(os.path.isdir(folder)):
        
        if(folder != 'reference' and folder != '__pycache__'):

                print(linecommon)
                print(folder)

                os.chdir(folder)
                bash_return, dumpfile = subprocess.getstatusoutput('grep -B1 "Loop time" log.lammps') ## for python3
                # bash_return, dumpfile = commands.getstatusoutput('grep -B1 "Loop time" log.lammps') ## for python2
                #print(dumpfile)
                energy = dumpfile.split()[1]

                print(energy)
                
                for j in range(len(atomid)):
                    if( int(atomid[j]) == int(folder)):
                        line = '%-8i %8i %20.8f %20.8f %20.8f %20.8f\n' %(atomid[j], atom_type[j], x[j], y[j], z[j], float(energy))
                os.chdir("../")
                
                energy_info.write(line)
                linecache.clearcache()
energy_info.close()

#=============================================================================================================
#                       sorted energy_info.dat according to energy
#=============================================================================================================
data = np.loadtxt('energy_info.dat')

energy_info = open('energy_info.dat', 'w')
a = np.array( sorted(data,key=lambda x:x[-1]) )
for i in range(len(data)):
    line = '%-8i %4i %16.8f %16.8f %16.8f %22.8f %12.6f\n' %(a[i][0], a[i][1], a[i][2], a[i][3], a[i][4], a[i][5], a[i][5]-a[len(data)-1][5] )
    energy_info.write(line)
energy_info.close()

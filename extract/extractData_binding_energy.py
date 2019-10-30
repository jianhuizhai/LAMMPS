import numpy as np
import os
import linecache
import subprocess

#=============================================================================================================
linecommon = "==============================================================================================="

# copy earlier energy_info.dat to energy_info_earlier.dat
os.system('cp energy_info.dat energy_info_earlier.dat')
#=============================================================================================================
print(linecommon)
print("    1 --------- noclimb.lmp")
print("    2 --------- climb.lmp")
print("    3 --------- distribution.dat")
print("    4 --------- distribution_halfLength.dat")
print("    5 --------- distribution_inRegion.dat")
print("    6 --------- all folders ")
print('='*80)

flag = input("The reference system : ")

skiplines = 16
if(flag == '1'):
        filename = 'noclimb.lmp'
elif(flag == '2' ):
        filename = 'climb.lmp'
elif( flag == '3' ):
        filename  = 'distribution.dat'
        skiplines = 0
elif( flag == '4' ):
        filename  = 'distribution_halfLength.dat'
        skiplines = 0
elif flag == '5' :
        filename  = 'distribution_inRegion.dat'
        skiplines = 0
elif flag == '6' :
        filename = 'relax.lmp'
        print( linecommon )
        print( 'The ref sys : relax.lmp.' )
else:
        exit("Unkown reference system!!!")

flag_eng = input("The reference energy : relaxed (1) or unrelaxed (2)    ")
print('='*80)
flag_pot = input("Do you want to just extract potEng ( y or n) ").lower()
#=============================================================================================================
#                               load data file
#=============================================================================================================
print(linecommon)
print("load %s ..." %filename)

atomid, atom_type, x, y, z = np.loadtxt(filename, skiprows=skiplines, usecols=(0,1,2,3, 4), unpack=True)

energy_info = open('energy_info.dat', 'w')

for folder in os.listdir():
    cwd = os.getcwd()
    if(os.path.isdir( os.path.join(cwd, folder) )):
        if not os.path.exists('reference') and flag_pot == 'n' :
            exit('reference folder do not exist.')
        if folder == 'reference':
            os.chdir( folder )
            if flag_eng == 1:
                bash_return, loglammpsfile = subprocess.getstatusoutput('grep -B1 "Loop time" log.lammps')
                reference_eng         = loglammpsfile.split()[1]
            else:
                bash_return, loglammpsfile = subprocess.getstatusoutput('grep -A1 "Step PotEng Lx" log.lammps')            
                reference_eng         = loglammpsfile.split()[14]
            print( 'The reference energy is {}'.format(reference_eng) )

            os.chdir('../')

        elif folder != '__pycache__' :

            print(linecommon)
            print(folder)

            os.chdir(folder)
            if flag_eng == '1':
                bash_return, loglammpsfile = subprocess.getstatusoutput('grep -B1 "Loop time" log.lammps')
                print(loglammpsfile)
                energy = loglammpsfile.split()[1]
            elif flag_eng == '2':
                bash_return, loglammpsfile = subprocess.getstatusoutput('grep -A1 "Step PotEng Lx" log.lammps')
                energy = loglammpsfile.split()[14]
            else:
                exit('unknown flag_eng')
            #finally:
            #    exit("There is no avaliable data in lammps.out or log.lammps.")
            #print( loglammpsfile)
            print(energy)
            '''    
            for j in range(len(atomid)):
                #  if( int(atomid[j]) == int(folder)):
                if( int(folder) == int(atomid[j])):
                    line = '%-8i %8i %20.8f %20.8f %20.8f %20.8f\n' %(atomid[j], atom_type[j], x[j], y[j], z[j], float(energy))
                    energy_info.write(line)
            '''
            index = int(folder) - 1
            line = '%-8i %8i %20.8f %20.8f %20.8f %20.8f\n' %(atomid[index], atom_type[index], x[index], y[index], z[index], float(energy))
            energy_info.write(line)
            os.chdir("../")
            
energy_info.close()

#=============================================================================================================
#                       sorted energy_info.dat according to energy
#=============================================================================================================

data = np.loadtxt('energy_info.dat')

energy_info = open('energy_info.dat', 'w')
a = np.array( sorted(data,key=lambda x:x[-1]) )
for i in range(len(data)):
    if flag_pot == 'n':
        line = '%-8i %4i %16.8f %16.8f %16.8f %22.8f %12.6f\n' %(a[i][0], a[i][1], a[i][2], a[i][3], a[i][4], a[i][5], a[i][5] - float(reference_eng) )
    elif flag_pot == 'y':
        line = '%-8i %4i %16.8f %16.8f %16.8f %22.8f\n' %(a[i][0], a[i][1], a[i][2], a[i][3], a[i][4], a[i][5] )
    energy_info.write(line)
energy_info.close()
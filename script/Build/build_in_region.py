"""
This code find the folder in the specified region and build the lammps file.
Copy the files in the corrsponded folder to HPC (zeus).
"""
import os
import numpy as np

linecomment = '='*80

build_flag = input("Do you want to build lammps input file in the folders (y or n) : ").lower()
#desiniteWorkDirection = input('desiniteWorkDirection in zeus: ')


if not os.path.exists('region_runned.dat') :
    os.system('touch region_runned.dat')
    #exit("region_runned.dat does not exixt.")

runned = np.loadtxt('region_runned.dat',usecols=([0]))

print("This will submit job in specified region.")

z_deleted = np.loadtxt('deleted.dat', usecols=([3]))

folders, z, binding_energy = np.loadtxt('energy_info.dat', usecols=([0, 4, 6]), unpack=True )


workDirectionZeus = os.getcwd()[50:]
zeuspre = 'jianhui.zhai@zeus:/home/jianhui.zhai/edge_110/100x100/'
workDirectionZeus = zeuspre + workDirectionZeus
print(workDirectionZeus)

#================================================================================================
#                   cp deleted.dat to zeus
#================================================================================================
os.system('scp deleted.dat {}'.format(workDirectionZeus) )



print('The selected region : {}---{}'.format( np.min(z_deleted), np.max(z_deleted) ) )
for i in range( len(z) ) :
    if z[i] <= np.max(z_deleted) and z[i] >= np.min(z_deleted) and binding_energy[i] <= 0:
        folder = str( int( folders[i] ) )
        if not any( [folder == str( int(k) ) for k in runned ] ):
            print('folder name : {}'.format( int( folders[i])) )
            if build_flag == 'y' :
                print( linecomment )
                os.chdir( folder )
                os.system('bash build_noclimb.sh')
                os.chdir('../')
                print( linecomment )

            os.system('scp -r {} {}'.format(folder, workDirectionZeus) )

'''
for folder in folders:
    folder = str( int(folder) )
    if build_flag == 'y':
        print( linecomment )
        os.chdir( folder )
        os.system('bash build_noclimb.sh')
        os.chdir('../')
        print( linecomment )
    
    os.system('scp -r {} jianhui.zhai@zeus:/home/jianhui.zhai/edge_110/100x100/{}'.format(folder, workDirectionZeus) )
'''

print( linecomment )
print( workDirectionZeus )
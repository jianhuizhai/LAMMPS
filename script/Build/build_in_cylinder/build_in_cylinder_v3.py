import numpy as np
import os
import subprocess
from sys import argv
from math import ceil
import matplotlib.pylab as plt
from mpl_toolkits import mplot3d

#==================================================================================
#                 define a function to create build.sh in specified folder
#==================================================================================
def mk_build( filename, length, flag_interstitial, atom_delete, atom_id ):
    
    os.system('touch '+filename)
    f = open(filename,'w')
    line = '#! /bin/bash \n'
    f.write(line)
    line = 'rm -f noclimb.lmp initial.lmp dump.relax* \n'
    f.write(line)
    
    '''
    line = 'n=5 \n'
    f.write(line)
    line = 'n4=$(echo "4*$n" | bc -l) \n'
    f.write(line)
    line = 'atomsk /home/jianhui/LASCO/MgO/edge_110/calculations/jog/0GPa/unit_collection/climb0.lmp -duplicate 1 1 $n4 noclimb.lmp \n'
    f.write(line)
    '''

    str_line = 'atomsk ../relax.lmp '
    if( length%2 == 0):
        if flag_interstitial != 2:
            line = str_line + '-select %i -rmatom select -add-atom %s at 224.855 150.6465 82.2513 initial.lmp \n' %( int(atom_id), atom_delete )
        elif flag_interstitial ==2:
            line = str_line + '-select %i -rmatom select -add-atom %s at 224.855 150.6465 82.2513 -add-atom %s at 74.9506 150.65 82.2513 initial.lmp \n' %( int(atom_id), atom_delete, atom_delete )
        print(line)
    elif( length%2 == 1 ):
        if flag_interstitial != 2:
            line = str_line+'-select %i -rmatom select initial.lmp \n' %( int(atom_id) )
        elif flag_interstitial ==2:
            line = str_line + '-select %i -rmatom select -add-atom %s at 224.855 150.6465 82.2513 -add-atom %s at 74.9506 150.65 82.2513 initial.lmp \n' %( int(atom_id), atom_delete, atom_delete )
        print(line)
    else:
        exit("Unkown flag interstitial.")
    f.write(line)
    line = 'lmp_atom2charge.sh initial.lmp \n'
    f.write(line)
    line = '#ovito initial.lmp \n'
    f.write(line)

    # copy files
    line = 'cp ~/bin/in.relax_atom . \n'
    f.write(line)
    line = 'cp ~/bin/job_relax.slurm . \n'
    f.write(line)
    

    f.close()

#==================================================================================
linecommon = "==============================================================================================="

print(linecommon)
print("load deleted.dat")
x_d, y_d, z_d = np.loadtxt('deleted.dat', usecols=(1,2,3), unpack=True)

'''
#==================================================================================
#                   cd the folder which has the lowest energy
#==================================================================================
parent_folder = np.loadtxt('energy_info.dat',dtype=int, usecols=(0))[0]
#print(str(parent_folder))
os.chdir( str(parent_folder) )
print(os.getcwd())
'''
#==================================================================================
print(linecommon)
atom_delete = input("The deleted ion type : " ).lower()
if(atom_delete == 'mg'):
    delete_type =1
elif(atom_delete == 'o'):
    delete_type = 2
else:
    exit("Unkown deleted ion type!")

#==================================================================================

print(linecommon)
bash_return, dumpfile = subprocess.getstatusoutput('(ls -t dump.relax* | head -n 1)')

print("lmp_file : ", dumpfile )
print("loading files ...")

#=================================================================================
#                   create corresponed vacancy folder
#=================================================================================
v_folder = 'v_' + atom_delete
if not os.path.exists( v_folder ):
    os.mkdir( v_folder )
os.chdir( v_folder )

print(linecommon)
print( os.getcwd() )

#=================================================================================
print(linecommon)

os.system('touch build_relax.sh')
f = open('build_relax.sh','w')
line = '#! /bin/bash \n'
f.write(line)
line = 'rm -f relax.lmp\n'
f.write(line)
line = 'atomsk ../'+dumpfile+' -select in cylinder z 224.855 150.6465 1.0 -rmatom select relax.lmp \n'
f.write(line)
f.close()
os.system('bash build_relax.sh')

#=================================================================================
print(linecommon)
print("load relax.lmp")

atomid, atom_type, x, y, z  = np.loadtxt('relax.lmp', skiprows=16, usecols=(0,1,2,3,4), unpack=True)
atomid = np.array(atomid, dtype = int)  # change to int type to create folder

xc = np.mean(x_d)
yc = np.mean(y_d)
zc = np.mean(z_d)

z_max = np.max(z_d)
z_min = np.min(z_d)
line = '#ovito initial.lmp \n'

print(linecommon)
print("xc = ", xc)
print("yc = ", yc)
print("zc = ", zc)

#==================================================================================================
#                   open a file and write the atom id (meet the critia) to it
#==================================================================================================
radius     = 2.5
z_distance = 0.5*len(x_d) * 4.218 - 4.218
while True:
    ions=[]
    test_info = open('distribution.dat', 'w')
    line = '%10i %8i %20.8f %20.8f %20.8f \n' %(0, 0, xc, yc, zc )
    test_info.write(line)

    for i in range(len(atomid)):
        if(atom_type[i] == delete_type):
            r2 = (x[i] - xc)**2 + (y[i] - yc)**2
            if(r2 <= radius**2 and z[i] <= z_max + z_distance and z[i] >= z_min - z_distance ):
                ions.append( atomid[i] )
                line = '%10i %8i %20.8f %20.8f %20.8f\n' %(atomid[i], atom_type[i], x[i], y[i], z[i] )
                test_info.write(line)
    line = '# %12i \n' %len(ions)
    test_info.write(line)
    test_info.close()

    print(linecommon)
    print("Write distribution.dat")
    print("The selected number of ions are : ", len(ions))

#====================================================================================================
#               plot the chosen ions type
#====================================================================================================
    print(linecommon)
    print("Plot point distribution")

    data = np.loadtxt('distribution.dat')
    ax = plt.axes(projection='3d')
    #ax.scatter(x, y, z, c='r')  # 绘制数据点,颜色是红色
    #plt.scatter(data[:,2],data[:,3], data[:,4], cmap='coolwarm')
    ax.scatter3D(data[:,2],data[:,3], data[:,4], c=data[:,1], cmap='coolwarm')
    #cb = plt.colorbar(scatters, pad=0.01)
    plt.xlim(xc - 4*radius, xc+4*radius)
    plt.ylim(yc - 4*radius, yc+4*radius)

    plt.savefig('point_distribution.pdf')
    plt.show()
    flag = input("Do you satisfy the point distribution (y or n) : ")
    if(flag == 'y'):
        break
    else:
        print("Earlier   radius   is ", radius)
        print("Earlier z_distance is ", z_distance)
        radius     = float(input("The   radius   : "))
        z_distance = float(input("The z_distance : "))

#====================================================================================================
filename = 'build_noclimb.sh'
print(linecommon)

os.system('ls')
print(linecommon)

#flag_floder     = input("Do you want to clean earlier results          (y or n) \n \
#This will delete all the folders in current folder.   : ")
flag_interstitial= int( input("How many interstitial do you want to add (0--1--2 ) : ") )

#if(flag_floder == 'y'):
for folder in os.listdir():
    if(os.path.isdir(folder)):
        if(folder != 'reference' and folder != '__pycache__' and folder != 'v_mg' and folder != 'v_o'):
            #os.system('rm -r '+folder)
            if( all( [folder != str(k) for k in ions ] ) ):
                os.system('rm -r '+folder)
            else:
                os.chdir( folder )
                print(os.getcwd())
                os.system('bash ~/bin/clean.sh')
                os.chdir("../")
                print(os.getcwd())

for atom in ions:
    print(linecommon)
    print('atom id is : ', atom)
    folder = str(atom)
    if(not os.path.exists( folder )):
        os.mkdir( folder )
    os.chdir( folder )
    print(os.getcwd())

    # generate build_noclimb.sh file to generate initial.lmp
    mk_build( filename, len(atomid), flag_interstitial, atom_delete, folder )

    os.system('bash '+filename)
    '''
    os.system('cp ~/bin/in.relax_atom .')
    os.system('cp ~/bin/job_relax.slurm .')
    '''
    os.chdir("../")
print(os.getcwd())
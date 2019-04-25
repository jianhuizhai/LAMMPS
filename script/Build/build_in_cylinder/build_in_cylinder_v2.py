import numpy as np
import os
from math import ceil
import matplotlib.pylab as plt
from mpl_toolkits import mplot3d


#==================================================================================
#                 define a function to create build.sh in specified folder
#==================================================================================
def mk_build( filename, deleted_atom, atom_delete, atom_id ):
    
    os.system('touch '+filename)
    f = open(filename,'w')
    line = '#! /bin/bash \n'
    f.write(line)
    line = 'rm -f noclimb.lmp initial.lmp \n'
    f.write(line)
    
    '''
    line = 'n=5 \n'
    f.write(line)
    line = 'n4=$(echo "4*$n" | bc -l) \n'
    f.write(line)
    line = 'atomsk /home/jianhui/LASCO/MgO/edge_110/calculations/jog/0GPa/unit_collection/climb0.lmp -duplicate 1 1 $n4 noclimb.lmp \n'
    f.write(line)
    '''

    len_deleted = len(deleted_atom)
    str_line = 'atomsk ../noclimb.lmp '
    if( len_deleted <= 17):
        #line1    = '-select ' + ','.join(str(int(i)) for i in deleted_atom ) + ' -rmatom select '
        line1    = '-select ' + ','.join(str(int(i)) for i in deleted_atom )
        str_line = str_line + line1
    else:
        # a mention to change the input file (noclimb.lmp file)
        exit("The number of deleted atoms are already 18.") 
        '''
        repeat = int( ceil(len_deleted/18) )
        
        for i in range(repeat):
            #line1 = '-select ' + ','.join(str(int(k)) for k in deleted_atom[10*i:10*i+10] ) + ' -rmatom select '
            line1 = '-select ' + ','.join(str(int(k)) for k in deleted_atom[10*i:10*i+10] )
            str_line = str_line + line1
        '''   
    if( len(deleted_atom)%2 == 0 ):
        line = str_line + ',%i -rmatom select -add-atom %s at 224.855 150.6465 82.2513 initial.lmp \n' %( int(atom_id), atom_delete )
        print(line)
    elif( len(deleted_atom)%2 == 1):
        line = str_line+',%i -rmatom select initial.lmp \n' %( int(atom_id) )
        print(line)
    f.write(line)
    line = 'lmp_atom2charge.sh initial.lmp \n'
    f.write(line)
    line = '#ovito initial.lmp \n'
    f.write(line)

    f.close()

    #s = open(filename).read()
    #s = s.replace('*****',atom_id)
    #f = open(filename, 'w')
    #f.close()
#==================================================================================
linecommon = "=========================================================================="

atom_delete = input("The deleted ion type : " ).title()
if(atom_delete == 'Mg'):
    delete_type =1
elif(atom_delete == 'O'):
    delete_type = 2
else:
    exit("Unkown deleted ion type!")

radius = float(input("The radius of cylinder (3 or 2.5) : "))

#==================================================================================
ions=[]

print(linecommon)
print("lmp_file : noclimb.lmp")
print("dat_file : deleted.dat")
print("loading files ...")

atomid, atom_type, x, y, z  = np.loadtxt('noclimb.lmp', skiprows=16, usecols=(0,1,2,3,4), unpack=True)
deleted_atom, x_d, y_d, z_d = np.loadtxt('deleted.dat', usecols=(0,2,3,4), unpack=True)
atomid = np.array(atomid, dtype = int)

xc = np.mean(x_d)
yc = np.mean(y_d)
zc = np.mean(z_d)

z_max = np.max(z_d)
z_min = np.min(z_d)

print(linecommon)
print("xc = ", xc)
print("yc = ", yc)
print("zc = ", zc)

#==================================================================================================
#                   open a file and write the atom id (meet the critia) to it
#==================================================================================================
test_info = open('distribution.dat', 'w')
line = '%10i %8i %20.8f %20.8f %20.8f \n' %(0, 0, xc, yc, zc )
test_info.write(line)



for i in range(len(atomid)):
    if(atom_type[i] == delete_type):
        if ( all( [atomid[i] != deleted_atom[k] for k in range(len(deleted_atom))] ) ):
        #if(abs(z[i] - zc) <= 5.0):
            r2 = (x[i] - xc)**2 + (y[i] - yc)**2
            if(r2 <= radius**2 and z[i] <= z_max + 4.4 and z[i] >= z_min - 4.4 ):
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
'''
print('type(ions) is ', type(ions))
ions = np.array( ions, dtype = int )  # change list to int array. 
print('type(ions) is ', type(ions))

for atom in ions:
    folder = str(atom)
    print(folder)
'''

#====================================================================================================
#               plot the chosen ions type
#====================================================================================================
print(linecommon)
print("Plot point distribution")

data = np.loadtxt('distribution.dat')
#print(data)
ax = plt.axes(projection='3d')
#ax.scatter(x, y, z, c='r')  # 绘制数据点,颜色是红色
#plt.scatter(data[:,2],data[:,3], data[:,4], cmap='coolwarm')
ax.scatter3D(data[:,2],data[:,3], data[:,4], c=data[:,1], cmap='coolwarm')
#cb = plt.colorbar(scatters, pad=0.01)
plt.savefig('point_distribution.pdf')
plt.show()



#====================================================================================================
filename = 'build_noclimb.sh'
print("=============================================================")

flag     = input("Do you want to clean earlier results          (y or n) \n \
This will delete all the folders in current folder.   : ")

os.system('rm -f energy_info.dat')
if(flag == 'y'):
    for folder in os.listdir():
        if(os.path.isdir(folder)):
            if(folder != 'reference' and folder != '__pycache__'):
                os.system('rm -r '+folder)
            #os.rmdir(folder)
            #os.chdir(folder)
            #os.system('clean.sh')
            #os.chdir("../")
for atom in ions:
    print('atom id is : ', atom)
    folder = str(atom)
    if(not os.path.exists( folder )):
        os.mkdir( folder )
        os.chdir( folder )
        print(os.getcwd())
        mk_build( filename, deleted_atom, atom_delete, folder )   # generate build_noclimb.sh file to generate initial.lmp

        os.system('bash '+filename)
        os.system('cp ~/bin/in.relax_atom .')
        os.system('cp ~/bin/job_relax.slurm .')
        os.chdir("../")
        print(os.getcwd())
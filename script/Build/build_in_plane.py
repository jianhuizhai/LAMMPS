import numpy as np
import os
import matplotlib.pylab as plt


#==================================================================================
#                 define a function to create build.sh in specified folder
#==================================================================================
def mk_build( filename, atom_type, atom_id ):
    
    os.system('touch '+filename)
    f = open(filename,'w')
    line = '#! /bin/bash \n'
    f.write(line)
    line = 'rm -f noclimb.lmp initial.lmp \n'
    f.write(line)
    line = 'n=5 \n'
    f.write(line)
    line = 'n4=$(echo "4*$n" | bc -l) \n'
    f.write(line)
    line = 'atomsk /home/jianhui/LASCO/MgO/edge_110/calculations/jog/0GPa/unit_collection/climb0.lmp -duplicate 1 1 $n4 noclimb.lmp \n'
    f.write(line)
    line = 'atomsk noclimb.lmp -add-atom %4s at 224.855 150.6465 82.2513 -select %5i -rmatom select initial.lmp \n' %( atom_type, int(atom_id) )
    f.write(line)
    line = 'lmp_atom2charge.sh initial.lmp \n'
    f.write(line)
    line = 'ovito initial.lmp \n'
    f.write(line)

    f.close()

    #s = open(filename).read()
    #s = s.replace('*****',atom_id)
    #f = open(filename, 'w')
    #f.close()
#==================================================================================

#oxygen = [803634, 803638, 811960, 803642, 803646, 803650, \
#          803234, 803238, 811956, 803242, 803246, 803250, \
#          802834, 802838, 811952, 802842,  802846, 802850, \
#          802434, 802438, 811948, 802442, 802446, 802450, \
#          802034, 802038, 811944, 802042, 802046, 802050, \
#          801634, 801638, 801642, 801646, 801650, \
#          801234, 801238, 801242, 801246, 801250, \
#          800834, 800838, 800842, 800846, 800850, \
#          800434, 800438, 800442, 800446, 800450]
xc = 149.892
yc = 226.214

atom_add = input("The added ion type : " )
if(atom_add == 'Mg'):
    add_type =1
elif(atom_add == 'O'):
    add_type = 2
else:
    exit("Unkown deleted ion type!")

ions=[]
#print('ions = ', ions)
atomid, atom_type, x, y, z = np.loadtxt('noclimb.lmp', skiprows=16, usecols=(0,1,2,3,4), unpack=True)

#==================================================================================================
#                   open a file and write the atom id (meet the critia) to it
#==================================================================================================
test_info = open('test.dat', 'w')
line = '%10i %8i %20.8f %20.8f \n' %(0, 0, xc, yc )
test_info.write(line)

for i in range(len(atomid)):
    if(atom_type[i] == add_type and z[i]>82):
        r2 = (x[i] - xc)**2 + (y[i] - yc)**2
        if(r2 <= 100):
            ions.append( atomid[i] )
            line = '%10i %8i %20.8f %20.8f \n' %(atomid[i], atom_type[i], x[i], y[i] )
            test_info.write(line)
line = '# %12i \n' %len(ions)
test_info.write(line)
test_info.close()

#====================================================================================================
print('type(ions) is ', type(ions))
ions = np.array( ions, dtype = int )  # change list to int array. 
print('type(ions) is ', type(ions))
'''
for atom in ions:
    folder = str(atom)
    print(folder)
'''

#====================================================================================================
#               plot the chosen ions type
#====================================================================================================
data = np.loadtxt('test.dat')
#print(data)
scatters = plt.scatter(data[:,2],data[:,3],c=data[:,1], cmap='coolwarm')
cb = plt.colorbar(scatters, pad=0.01)
plt.savefig('point_distribution.pdf')
plt.show()



#====================================================================================================
filename = 'build_noclimb.sh'
print("=============================================================")

flag     = input("Do you want to clean earlier results          (y or n) \n \
This will delete all the folders in current folder.   : ")


if(flag == 'y'):
    for folder in os.listdir():
        if(os.path.isdir(folder)):
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
        mk_build( filename, atom_add, folder )   # generate build_noclimb.sh file to generate initial.lmp

        os.system('bash '+filename)
        os.system('cp ~/bin/in.relax_atom .')
        os.system('cp ~/bin/job_relax.slurm .')
        os.chdir("../")
        print(os.getcwd())
'''
    else:
        print("folder exists. Go to the folder")
        
        os.chdir( folder )
        print(os.getcwd())
        mk_build( filename, folder )   # generate build_noclimb.sh file to generate initial.lmp

        os.system('bash '+filename)
        os.system('cp ~/bin/in.relax_atom .')
        os.system('cp ~/bin/job_relax.slurm .')
        os.chdir("../")
        print(os.getcwd())
'''
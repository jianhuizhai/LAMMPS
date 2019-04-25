"""
This code is used to visulization of energy by using dumpfile.
The energy value of deleted atoms are assigned to 5.
The energy value of not considered atoms are assigned to 20.
"""
import numpy as np
import sys
import linecache
from output_fake import DumpOutput

linecommon = '========================================================='

print(linecommon)
'''
n = int(input("How many atoms are deleted : "))
ions=[]
while (n>0):
    ions.append(input("atom id : "))
    n = n-1

ions = np.array( ions, dtype = int )  # change list to int array. 
'''
id_d, x_d, y_d, z_d = np.loadtxt("deleted.dat", usecols=(0,1,2,3))
print("The already deleted %i ions are : "  %x_d.size)
#print( ions )

deleted_file= sys.argv[1]
lmp_file    = sys.argv[2]
energy_file = sys.argv[3]

id_d, x_d, y_d, z_d = np.loadtxt("deleted.dat", usecols=(0,1,2,3))
print("The already deleted %i ions are : "  %x_d.size)

print(linecommon)
print("deleted_file: ", deleted_file)
print("lmp_file    : ", lmp_file)
print("energy_file : ", energy_file)
print(linecommon)

xlim = linecache.getline(lmp_file, 6)
ylim = linecache.getline(lmp_file, 7)
zlim = linecache.getline(lmp_file, 8)

print(xlim, end='')
print(ylim, end='')
print(zlim, end='')
print(linecommon)

skipline  = 16
atom_id, atom_type, x,y,z = np.loadtxt(lmp_file, skiprows=skipline, usecols=(0,1,2,3,4), unpack=True)
eng_id, eng_eng = np.loadtxt(energy_file, usecols=(0,6), unpack=True)

atom_id = list(atom_id)
atom_type = list(atom_type)
x         = list(x)
y         = list(y)
z         = list(z)
Eng       = [20]*len(atom_id)
#list(np.ones(len(atom_id))*20)
'''
print("type(atom_id) : ", type(atom_id))
print("type(ions) : ", type(ions))
'''
len_new = len(atom_id) + x_d.size
if( x_d.size == 1):
    atom_type.append(id_d)
    x.append( x_d )
    y.append( y_d )
    z.append( z_d )
    Eng.append( 5 )
else:
    for i in range(x_d.size):
        atom_type.append(id_d[i])
        x.append( x_d[i] )
        y.append( y_d[i] )
        z.append( z_d[i] )
        Eng.append( 5 )

#Eng = np.ones(len(atom_id))*20
#print("Eng", Eng)


for k in range(eng_id.size):
    id = atom_id.index( eng_id[k] )
    Eng[id] = eng_eng[k]

'''
# this is the older version assign energy value
for i in range(len(atom_id)):
    if(ions.size != 0):
        if(ions.size == 1):
            if(atom_id[i] == ions):
                Eng[i] = 5
        else:
            for k in range(ions.size):
                if(atom_id[i] == ions[k]):
                    Eng[i] = 5
    for j in range(len(eng_id)):
        if( atom_id[i] == eng_id[j] ):
            Eng[i] = eng_eng[j]
'''

DumpOutput('dump.eng',xlim, ylim, zlim, atom_id, atom_type, x, y, z, Eng)
print("Output file: dump.eng")
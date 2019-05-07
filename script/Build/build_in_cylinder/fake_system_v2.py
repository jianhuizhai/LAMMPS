"""
This code is used to visulization of energy by using dumpfile.
The energy value of deleted atoms are assigned to 5.
The energy value of not considered atoms are assigned to 20.
"""
import numpy as np
import sys
import linecache
from output_fake import DumpOutput

#=================================================================================
#                   specify lmp_file
#=================================================================================
linecommon = '========================================================='

lmp_file = sys.argv[1]

#=================================================================================
#                   print dat files info
#=================================================================================

print(linecommon)
print("deleted_file: deleted.dat")
print("lmp_file    : ", lmp_file)
print("energy_file : energy_info.dat")
print("loading files...")

xlim = linecache.getline(lmp_file, 6)
ylim = linecache.getline(lmp_file, 7)
zlim = linecache.getline(lmp_file, 8)
print(linecommon)
print(xlim, end='')
print(ylim, end='')
print(zlim, end='')

#=================================================================================
#                       loading files
#=================================================================================
skipline  = 16
atom_id, atom_type, x,y,z = np.loadtxt(lmp_file, skiprows=skipline, usecols=(0,1,2,3,4), unpack=True)
eng_id, eng_eng = np.loadtxt('energy_info.dat', usecols=(0,6), unpack=True)

#=================================================================================
#               change array to list (eassy to append data)
#=================================================================================
#          add already deleted data to atom_type, x, y and z; and assign Eng
#=================================================================================
atom_id   = list(atom_id)
atom_type = list(atom_type)
x         = list(x)
y         = list(y)
z         = list(z)
Eng       = [20]*len(atom_id)

#length = len( open('deleted.dat').read() )
length = len( open(r"deleted.dat",'rU').readlines())
if length != 0:
    id_d, x_d, y_d, z_d = np.loadtxt("deleted.dat", usecols=(0,1,2,3), unpack=True)

    len_new = len(atom_id) + x_d.size
    if( x_d.size == 1 ):
    
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
#--------------------------------------------------------------------------------
#                assign the energy values of distributed ions to Eng
#--------------------------------------------------------------------------------
for k in range(eng_id.size):
    id = atom_id.index( eng_id[k] )
    Eng[id] = eng_eng[k]

print(linecommon)
print("The number of already deleted ions are %i: "  %length )


#=================================================================================
DumpOutput('dump.vacancies'+str(length),xlim, ylim, zlim, atom_id, atom_type, x, y, z, Eng)
print("Output file: dump.vacancies"+str(length) )
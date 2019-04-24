"""
This code is used to generate deleted.dat.
The ions which is tested to have the lowest energy is not included in it.
"""
import numpy as np


linecommon = '========================================================='

print(linecommon)
print("load deleted.dat")
print("load noclimb.lmp")

deleted_atom               = np.loadtxt('deleted.dat', usecols=(0) )
atomid, atom_type, x, y, z = np.loadtxt('noclimb.lmp', skiprows=16, usecols=(0,1,2,3,4), unpack=True)

info = open('deleted.dat', 'w')
atomid = list(atomid)

for i in range(len(deleted_atom)):
    #ions.append(input("atom id : "))
    index = atomid.index(deleted_atom[i])
    line = '%-10i %4i %20.8f %20.8f %20.8f \n' %(atomid[index], atom_type[index], x[index], y[index], z[index] )
    info.write(line)
info.close()

print(linecommon)
print("write deleted.dat")
print(linecommon)
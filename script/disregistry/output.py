import numpy as np

def DumpOutput(filename, xlim, ylim, zlim, atomtype, x, y, z):
    newfile = open(filename, 'w')
    line = 'ITEM: TIMESTEP'+'\n'
    newfile.write(line)
    line = '0'+'\n'
    newfile.write(line)
    line = 'ITEM: NUMBER OF ATOMS'+'\n'
    newfile.write(line)
    line = str(len(x))+'\n'
    newfile.write(line)            
    line = 'ITEM: BOX BOUNDS pp pp pp'+'\n'
    newfile.write(line)
    line = xlim
    newfile.write(line)
    line = ylim
    newfile.write(line)
    line = zlim
    newfile.write(line)
    line = 'ITEM: ATOMS id type element xu yu zu'+'\n'
    newfile.write(line)
    for i in range(len(x)):
        if( atomtype[i]== 1):
            element = 'Mg'
        else:
            element = 'O'
        line = '%8i %4i %4s %16.8f %16.8f %16.8f\n'%(i+1, atomtype[i], element, x[i], y[i], z[i])
        newfile.write(line)
    newfile.close()
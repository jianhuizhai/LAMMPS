'''This code is used to extract plane along dislocation direction'''
'''This code now is worked for slice process.'''

import numpy as np
import sys
import linecache
from output import DumpOutput
from scipy.optimize import curve_fit
import matplotlib.pylab as plt

#======================================================================================
#       define objective function to fit disregistry and density of disregistry
#======================================================================================
def func(x,b,mean,width):
    return b/np.pi*np.arctan((x-mean)/width)+b/2
def rho(x,b, mean, width):
    return b/np.pi*width/(np.power(x-mean,2)+ np.power(width,2))

#=======================================================================================
#                        material parameter under different pressures
#=======================================================================================
pressure = int(input("type the pressure of system: (100, 60, 30 or 0 -- units in GPa)"+"\n"))

if(pressure == 100):
    alat = 3.83
elif(pressure == 60):
    alat = 3.94
elif(pressure == 30):
    alat = 4.05
elif(pressure == 0):
    alat = 4.22
else:
    print("The pressure is not included in the code.")
    exit()

#=======================================================================================
#        specify the distance between atoms in different directions
#=======================================================================================
bmag = alat/np.sqrt(2)
XDistance = 0.5*bmag
YDistance = 0.5*bmag
ZDistance = 0.5*alat

#=======================================================================================
#                               extract disloc
#=======================================================================================
filename = sys.argv[1]       # you need to specify the filename in the terminal

xlim = linecache.getline(filename, 6)
ylim = linecache.getline(filename, 7)
zlim = linecache.getline(filename, 8)

xlo = float( xlim.split()[0] );  xhi = float( xlim.split()[1] )
ylo = float( ylim.split()[0] );  yhi = float( ylim.split()[1] )
zlo = float( zlim.split()[0] );  zhi = float( zlim.split()[1] )

print("xlim ", xlim, end='')
print("ylim ", ylim, end='')
print("zlim ", zlim)

skipline = 9
atomtype = np.loadtxt(filename, skiprows=skipline, usecols=(1))
data     = np.loadtxt(filename, skiprows=skipline, usecols=(3,4,5))

x0 = data[:,0]; y0 = data[:,1]; z0 = data[:,2]

PlaneNum = 0

pz   = np.min(z0) - ZDistance

ratio = 1.6

ylayers = int( (yhi-ylo)/YDistance )
zlayers = int( (zhi-zlo)/ZDistance )+1 # actual layers is zlayers+1

#===========================================================================
linecommon = '=========================================================\n'

print("ylayers = ", ylayers)
print("zlayers = ", zlayers)


#============================================================================
#      write disloc info to DislocInfo.dat file
#============================================================================
Info = open('DislocInfo_'+filename+'.dat','w')
line = 'Information about simulation cell.'+'\n'
Info.write(line)

Info.write(xlim)
Info.write(ylim)
Info.write(zlim)


Info.write(linecommon)
line = 'Info about disloc'+'\n'
Info.write(line)
Info.write(linecommon)
line1 = 'PlaneNum   DislocNum       calculated properties(b_c, x_c, y_c, z_c)      '
line2 = 'fitting properties(b, x0, width)\n'
line  = line1 + line2 + '\n'
Info.write(line)
#======================================================================
#                  extract  layer 
#======================================================================
for i in range(zlayers):
    planex = []; planey = []; planez = []
    dataplane = []
    AtomPosiZlayer = []

    for j in range( len(z0) ): # number of atoms in the simulation box
        if( z0[j]< pz+ratio*ZDistance and z0[j]> pz):
            planex.append( x0[j] ); planey.append( y0[j] ); planez.append( z0[j] )
            dataplane.append(data[j])
            AtomPosiZlayer.append( j )

    PlaneNum = PlaneNum + 1
    print(linecommon, "PlaneNum = ", PlaneNum)
    
    dumpfile = "dump.plane."+str(PlaneNum)
    DumpOutput(dumpfile, xlim, ylim, zlim, atomtype[AtomPosiZlayer], planex, planey,planez)
    pz = np.max(planez)

#========================================================================
#            search for dislocation
#========================================================================
    DislocNum = 0
    py        = np.min(y0)
    for k in range(ylayers):
        position = []
# =======================================================================
#       below plane; above plane
#========================================================================
        half1 = []; half2 = []
        # x = []; y = []; z = []
        above = []
        # AtomsDisloc = []

        for l in range(len(dataplane)):
            if( dataplane[l][1] < py+ratio*YDistance and dataplane[l][1]>= py):
                if(dataplane[l][1]<py+0.5*ratio*YDistance):
                    half1.append( dataplane[l] )
                else:
                    half2.append(dataplane[l])
                    above.append(dataplane[l][1])
                # x.append( dataplane[l][0] )
                # y.append( dataplane[l][1] )
                # z.append( dataplane[l][2] )
                AtomsDisloc = half1+half2
                AtomsDisloc = np.array(AtomsDisloc)
                position.append(l)

        py = np.min(above)
        len_above = len(half2)
        len_below = len(half1)

        if( len_below == len_above ):
            continue
        elif( len_below ==0 or len_above ==0):
            print(linecommon)
            print("one atom layer is empty!")
            print("py = ", py)
            print("ylim = ", ylim)
            print(linecommon)
            exit()
        else:
            DislocNum = DislocNum +1
            print("DislocNum = ", DislocNum)
        #====================================================================================
        #                      dump dislocation configuration
        #====================================================================================
            dumpfile = 'dump.plane'+str(PlaneNum) +".Disloc"+str(DislocNum)
            DumpOutput(dumpfile, xlim, ylim, zlim, atomtype[position], AtomsDisloc[:,0], AtomsDisloc[:,1], AtomsDisloc[:,2] )

        #  sort half2 and half1 according to x coorinate
            half1.sort(key=lambda x: x[0])
            half2.sort(key=lambda x: x[0])
        #====================================================================================
        #                  fitting disloc position
        #====================================================================================
        atoms = int( (len_above + len_below - 1 )*0.5 )
        # print("atoms = ",atoms)
        disregistry = np.zeros(atoms)
        if(len(half2)> len(half1)):
            atoms_above = np.array( [x[0] for x in half2] )[0:len(half2)-1]  # x[0] command is used to get first column value of list half2
            atoms_below = np.array( [x[0] for x in half1] )
        else:
            atoms_above = np.array( [x[0] for x in half2] )
            atoms_below = np.array( [x[0] for x in half1] )[0:len(half1)-1]

        if(atoms_above[0]-atoms_below[0] > 0):
            disregistry = 0.5*bmag -(atoms_above-atoms_below)
        else:
            disregistry = -0.5*bmag - (atoms_above - atoms_below)
        
        b_calculated = (disregistry[-1]-disregistry[0])
        # find the value in disregistry close to 0.5*b_calculated 
        density_max  = min(list(disregistry), key=lambda x:abs(x-0.5*b_calculated))

        # get index of the density_max and then get corresponded atoms_above value
        x_calculated = atoms_above[list(disregistry).index(density_max)]
        y_calculated = np.mean( AtomsDisloc[:,1] )
        z_calculated = np.mean( AtomsDisloc[:,2] )

        f = open('disregistry.plane' + str(PlaneNum) +'Dis' +str(DislocNum)+'.dat', 'w')
        for k in range(len(disregistry)):
            line = '%16.8f %16.8f \n'%(atoms_above[k], disregistry[k])
            f.write(line)
        f.close()
#=========================================================================================
#                              curve fitting 
#=========================================================================================
        popt, pcov = curve_fit(func, atoms_above, disregistry, p0=[b_calculated, x_calculated, 2.0])
        b    = popt[0]
        mean = popt[1]
        width = popt[2]
        x=[i for i in np.arange(0.,np.max(atoms_above),0.1)]
        x = np.array(x)
        yvals=func(x, b, mean,width)

        fig, ax1 = plt.subplots(figsize=(18.5,10.5))
        ax1.plot( atoms_above, disregistry, 'o', label='data')
        ax1.plot(x, yvals, 'r',linewidth=5.0,label='fit')
        ax1.set_xlabel("x"+'(' + r'$\AA$' +')')
        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_ylabel(r'$\phi$'+'(' + r'$\AA$' +')', color='red')
        ax1.tick_params('y', colors='red')

        ax2 = ax1.twinx()
        rho2 = np.vectorize(rho)
        ax2.plot(x, rho2(x, b, mean, width), 'blue', linewidth=3.0, label ='density')
        ax2.set_ylabel(r'$\rho$', color='blue')
        ax2.tick_params('y', colors='blue')
        fig.tight_layout()
        
        plt.savefig('disregistry.plane'+ str(PlaneNum) + 'Disloc'+str(DislocNum)+'.pdf',bbox_inches="tight")
        # plt.show()
#============================================================================================
        line1 = '%4i %11i' %(PlaneNum, DislocNum)
        line2 = '%16.8f %16.8f %16.8f %16.8f' %(b_calculated, x_calculated, y_calculated, z_calculated)
        line3 = '%16.8f %16.8f %16.8f' %(b, mean, width)
        line  = line1 + line2 +line3 +'\n'
        Info.write(line)
Info.close
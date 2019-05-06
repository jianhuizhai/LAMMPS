'''This code is used to extract plane along dislocation direction'''
'''This code is for edge dislocation.'''
'''Dislocation glide in xy plane, line direction is y. Burgurs vector along x direction.'''
#========================================================================================
'Attenton: x_fit should be used to determine the position of dislocation not x_calcu.'
'x_calcu is not exactly corrected.'
# when add determine jog position, add code to determine the dislocation line direction,
# direction of burgers vector and direction normal to line direction and burgers vector
#========================================================================================
import os
import numpy as np
import sys
import linecache
from output import DumpOutput
from scipy.optimize import curve_fit
import matplotlib.pylab as plt

#======================================================================================
#       define objective function to fit disregistry and density of disregistry
#======================================================================================
#def func(x, b, alpha, mean1,width1,mean2, width2):
#    return 0.5*b + b/np.pi*( alpha *np.arctan( (x-mean1)/width1 ) + 0.5*(1-alpha)*np.arctan( (x-mean1-mean2)/width2) + \
#    0.5*(1-alpha)*np.arctan( (x-mean1+mean2)/width2))
#def rho(x,b, alpha, mean1, width1, mean2, width2):
#    return b/np.pi*( alpha * width1/(np.power(x-mean1,2)+ np.power(width1,2)) + \
#    0.5*(1-alpha)* width2/( np.power(x-mean1-mean2,2) + np.power(width2,2)) + \
#    0.5*(1-alpha)* width2/( np.power(x-mean1+mean2,2) + np.power(width2,2)))
def func(x ,mean, width):
    return b_calculated/np.pi*np.arctan((x-mean)/width)+b_calculated/2
def rho(x , mean, width):
    return b_calculated/np.pi*width/(np.power(x-mean,2)+ np.power(width,2))

#======================================================================================
#                       specify the filename in the terminal
#======================================================================================
linecommon = '=========================================================\n'

if len(sys.argv) < 2:
    exit('Please provide a dump file to exact jog.')
    
filename = sys.argv[1]
if not os.path.isfile(filename):
    exit("The file is not existed!")
#=======================================================================================
#                        material parameter under different pressures
#=======================================================================================
while True:
    pressure = input("type the pressure of system: (100, 60, 30 or 0 -- units in GPa)"+"\n")
    if pressure.isdecimal():
        pressure = int(float(pressure))
        break
    else:
        print("The pressure should be a number!!")

if(pressure == 100):
    alat = 3.82776
elif(pressure == 60):
    alat = 3.9355
elif(pressure == 30):
    alat = 4.047
elif(pressure == 0):
    alat = 4.218
else:
    print("The pressure is not included in the code.")
    while True:
        alat = input("Type lattice parameter : \n")
        if alat.isdecimal():
            alat = float(alat)
            break
        else:
            print("The lattice parameter should be a number!!!")

print(linecommon)

#=======================================================================================
flag_plane = input("Do you want to dump plane: (y or n) \n").lower()
flag_disloc= input("Do you want to dump disloc: (y or n) \n").lower()
print(linecommon)
#=======================================================================================
#        specify the distance between atoms in different directions
#=======================================================================================
bmag = alat/np.sqrt(2)
BurgDistance = 0.5*bmag
LineDistance = 0.5*alat
NormDistance = 0.5*bmag

#=======================================================================================
#                               extract disloc
#=======================================================================================

xlim = linecache.getline(filename, 6)
ylim = linecache.getline(filename, 7)
zlim = linecache.getline(filename, 8)

xlo = float( xlim.split()[0] );  xhi = float( xlim.split()[1] )
ylo = float( ylim.split()[0] );  yhi = float( ylim.split()[1] )
zlo = float( zlim.split()[0] );  zhi = float( zlim.split()[1] )

print("xlim ", xlim, end='')
print("ylim ", ylim, end='')
print("zlim ", zlim)

print(linecommon)

#============================================================================
skipline = 9

data1     = np.loadtxt(filename, skiprows=skipline, usecols=(1,3,4,5))
atomtype  = data1[:,0]
data      = data1[:,1:4]

x0 = data[:,0]; y0 = data[:,1]; z0 = data[:,2]

PlaneNum = 0

PosiLine   = np.min(y0) - LineDistance

ratio = 1.4

NormLayers = round( (np.max(z0) - np.min(z0)) / NormDistance )       # 四舍五入
LineLayers = round( (np.max(y0) - np.min(y0)) / LineDistance ) + 1

NormLayers = int(NormLayers)
LineLayers = int(LineLayers)
#===========================================================================

print("NormLayers = ", NormLayers)
print("LineLayers = ", LineLayers)


#============================================================================
#      write disloc info to DislocInfo.dat file
#============================================================================
Info = open('DislocInfo_jog_'+filename+'.dat','w')
line = 'Information about simulation cell.'+'\n'
Info.write(line)

Info.write(xlim)
Info.write(ylim)
Info.write(zlim)


Info.write(linecommon)
line = 'Info about disloc'+'\n'
Info.write(line)
Info.write(linecommon)
line1 = 'PlaneNum   DislocNum       calculated properties(b_c, x_c, y_c, z_c)            '
line2 = 'fitting properties(mean, width)     Percent(%) \n'
line  = line1 + line2 + '\n'
Info.write(line)
#======================================================================
#                  extract  layer 
#======================================================================
for i in range(LineLayers):
    planex = []; planey = []; planez = []
    dataplane = []
    AtomPosiZlayer = []

    for j in range( len(y0) ): # number of atoms in the simulation box
        if( y0[j]< PosiLine + ratio*LineDistance and y0[j]> PosiLine):
            planex.append( x0[j] ); planey.append( y0[j] ); planez.append( z0[j] )
            dataplane.append(data[j])
            AtomPosiZlayer.append( atomtype[j] )

    PlaneNum = PlaneNum + 1
    print(linecommon, "PlaneNum = ", PlaneNum)
    if(flag_plane == 'y'):
        dumpfile = "dump.plane."+str(PlaneNum)
        DumpOutput(dumpfile, xlim, ylim, zlim, AtomPosiZlayer, planex, planey,planez)
    
    # the beginning position is the higest y of current plane
    PosiLine = np.max(planey)

#========================================================================
#            search for dislocation
#========================================================================
    DislocNum = 0
    PosiNorm = np.min(z0)
    for k in range(NormLayers):
        position = []
# =======================================================================
#       below plane; above plane
#========================================================================
        half1 = []; half2 = []
        atomx = []; atomy = []; atomz = []
        above = []

        for l in range(len(dataplane)):
            if( dataplane[l][2] < PosiNorm+ratio*NormDistance and dataplane[l][2]>= PosiNorm):
                if(dataplane[l][2]<PosiNorm+0.5*ratio*NormDistance):
                    half1.append( dataplane[l] )
                else:
                    half2.append(dataplane[l])
                    above.append(dataplane[l][2]) # [2] means z coordinate
                atomx.append( dataplane[l][0] )
                atomy.append( dataplane[l][1] )
                atomz.append( dataplane[l][2] )
                position.append(AtomPosiZlayer[l])

        PosiNorm = np.min(above)
        len_above = len(half2)
        len_below = len(half1)
        
        if( len_below == len_above ):
            continue
        elif( len_below ==0 or len_above ==0):
            print("one atom layer is empty!")
            print(linecommon)
            exit()
        else:
            #  sort half2 and half1 according to x coorinate
            half1.sort(key=lambda x: x[0])
            half2.sort(key=lambda x: x[0])

            DislocNum = DislocNum +1
            print("DislocNum = ", DislocNum)
            #====================================================================================
            #                      dump dislocation configuration
            #====================================================================================
            if(flag_disloc == 'y'):
                dumpfile = 'dump.plane'+str(PlaneNum) +".Disloc"+str(DislocNum)
                DumpOutput(dumpfile, xlim, ylim, zlim, position, atomx, atomy, atomz )

        #====================================================================================
        #                  fitting disloc position
        #====================================================================================
        atoms = int( (len_above + len_below - 1 )*0.5 )
        # print("atoms = ",atoms)
        disregistry = np.zeros(atoms)
        if(len(half2)> len(half1)):
            atoms_above  = np.array( [x[0] for x in half2] )[0:len(half2)-1]  # x[0] command is used to get first column value of list half2
            atoms_below  = np.array( [x[0] for x in half1] )
            atoms_disreg = atoms_below
        else:
            atoms_above  = np.array( [x[0] for x in half2] )
            atoms_below  = np.array( [x[0] for x in half1] )[0:len(half1)-1]
            atoms_disreg = atoms_above

        if(atoms_above[0]-atoms_below[0] > 0):
            disregistry = 0.5*bmag -(atoms_above-atoms_below)
        else:
            disregistry = -0.5*bmag - (atoms_above - atoms_below)
        
        b_calculated = (disregistry[-1]-disregistry[0])
        # find the value in disregistry close to 0.5*b_calculated 
        density_max  = min(list(disregistry), key=lambda x:abs(x-0.5*b_calculated))

        # get index of the density_max and then get corresponded atoms_above value
        x_calculated = atoms_disreg[list(disregistry).index(density_max)]
        y_calculated = np.mean( atomy )
        z_calculated = np.mean( atomz )

        f = open('disregistry.plane' + str(PlaneNum) +'Dis' +str(DislocNum)+'.dat', 'w')
        for k in range(len(disregistry)):
            line = '%16.8f %16.8f \n'%(atoms_disreg[k], disregistry[k])
            f.write(line)
        f.close()
#=========================================================================================
#                              curve fitting 
#=========================================================================================
        popt, pcov = curve_fit(func, atoms_disreg, disregistry)
        mean = popt[0]
        width= popt[1]

        x=[i for i in np.arange(0.,np.max(atoms_disreg),0.1)]
        x = np.array(x)
        yvals=func(x, mean, width)

        fig, ax1 = plt.subplots(figsize=(18.5,10.5))
        ax1.plot( atoms_disreg, disregistry, 'o', label='data')
        ax1.plot(x, yvals, 'r',linewidth=5.0,label='fit')
        ax1.set_xlabel("x"+'(' + r'$\AA$' +')')
        # Make the y-axis label, ticks and tick labels match the line color.
        ax1.set_ylabel(r'$\phi$'+'(' + r'$\AA$' +')', color='red')
        ax1.tick_params('y', colors='red')

        ax2 = ax1.twinx()
        rho2 = np.vectorize(rho)
        ax2.plot(x, rho2(x, mean, width), 'blue', linewidth=3.0, label ='density')
        ax2.set_ylabel(r'$\rho$', color='blue')
        ax2.tick_params('y', colors='blue')
        fig.tight_layout()
        
        plt.savefig('disregistry.plane'+ str(PlaneNum) + 'Disloc'+str(DislocNum)+'.pdf',bbox_inches="tight")
        # plt.show()
#============================================================================================
        line1 = '%4i %8i' %(PlaneNum, DislocNum)
        line2 = '%14.8f %14.8f %14.8f %14.8f ' %(b_calculated, x_calculated, y_calculated, z_calculated)
        line3 = '%20.8f %14.8f %12.2f' %(mean, width, 100*(y_calculated-ylo)/(yhi-ylo))
        line  = line1 + line2 +line3 +'\n'
        Info.write(line)
Info.close
import os
from search import SearchFile
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pylab as plt

#======================================================================================
#               define objective function to fit energy difference
#======================================================================================
def func(x,a):
    return a*np.power(x, 2)

#======================================================================================
#                            specify pressure
#======================================================================================
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
bmag = 0.5*np.sqrt(2)*alat

#=====================================================================================
#               getting data from corresponed folder
#=====================================================================================
linecommon = '\n'+'========================================================================'
print(linecommon)
print("cwd: ", os.getcwd())
print(linecommon)

middle = int(input("NUmber of middle image: "))
img = [1, middle, 16]
px = np.zeros((3,4))

skipline = 9
#-------------------------------------------------------------------------------------
for i in range(3):
    os.chdir("img"+str(img[i]))
    print("cwd:   ", os.getcwd() )
    filename = SearchFile.findfile('.', 'DislocInfo_', '.')[2:]
    print("filename is ", filename)

    px[i] = np.loadtxt(filename, skiprows=skipline, usecols=7)
    os.chdir("../")
    print("cwd: ", os.getcwd())
    print(linecommon)

#-------------------------------------------------------------------------------------
dx = np.zeros(2); de = np.zeros(2)
dx_max  = px[2][1] - px[2][0] -(px[0][1] - px[0][0])
dx_half = px[1][1] - px[1][0] -(px[0][1] - px[0][0])
# dx_half = 0.5*bmag

dx[1] = dx_max     # assign the coordinate difference for RD =1
#-------------------------------------------------------------------------------------

energy = np.loadtxt('nebpath.dat', usecols=(1))
de[1] = energy[-1]      # assign the energy difference for RD =1

#=====================================================================================
#                                fitting curve
#=====================================================================================
popt, pcov = curve_fit(func, dx, de)
a    = popt[0]

points =[i for i in np.arange(0.,1.5*dx_max,0.1)]
points = np.array(points)
yvals=func(points, a)
# yvals=func(x, *popt)
plt.figure(figsize=(18.5,10.5))
plt.plot( dx, de, 'o', label='data')
plt.plot(points, yvals, 'r',linewidth=4.0,label='fit')

plt.savefig('energy_correction.pdf',bbox_inches="tight")
# plt.show()

energy_half = a*dx_half**2
Ea = np.max(energy) - energy_half

#======================================================================================
#                    write results to energy_correction.dat
#======================================================================================
f = open('energy_correction.dat', 'w')
line = 'dx = %12.10f \n' %dx[1]
f.write(line) 
line = 'dx_half = %12.10f energy_half = %16.8f \n' %(dx_half, energy_half) 
f.write(line)
line = "Ea= %16.8f \n" %Ea
f.write(line)
f.close()

#========================================================================================
#                           print information on terminal
#========================================================================================
print("dx = ", dx)
print("dx_half = ", dx_half, "energy_half = ", energy_half)
print("Ea = ", Ea )
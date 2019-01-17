import os
from search import SearchFile
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pylab as plt


#======================================================================================
#               define objective function to fit energy difference
#======================================================================================
def func1(x,a):
    return a*np.power(x, 1)
def func2(x,a):
    return a*np.power(x, 2)

#===================================================================================
print("The character of dislocation: positive or negtive .")
character = input("Please type p or n. \n")

if(character == 'p'):
    filename = 'CorePosition_p.dat'
elif(character == 'n'):
    filename = 'CorePosition_n.dat'
else:
    print("Unknown dislocation character.")
    exit()
#===================================================================================
position= np.loadtxt(filename, usecols=2)
rd, energy1 = np.loadtxt('nebpath.dat', unpack=True)

#------------------------------------------------------------------------------
print("Do you want to consider energy correction by babel. ")
correct_flag = input("Please type y or n. \n")

if(correct_flag == 'y'):
    energy2 = np.loadtxt('nebpath_correction.dat', usecols=1)
    energy = energy1 - energy2
elif(correct_flag == 'n'):
    energy = energy1
else:
    print("Unkown babel correction flag!")
    exit()

#print('energy is ', energy)

#=====================================================================================
#                                fitting curve
#=====================================================================================

data_x = np.array([position[0],position[-1]])
data_y = np.array([energy1[0],energy1[-1]])
#-------------------------------------------------------------------------------------
#              fit the data with linear correction
#-------------------------------------------------------------------------------------
popt, pcov = curve_fit(func1, data_x, data_y)
a_linear   = popt[0]


points = [i for i in np.arange(np.min(position),np.max(position),0.1)]
points = np.array(points)

yvals=func1(points, a_linear)
# yvals=func(x, *popt)
plt.figure(figsize=(18.5,10.5))
plt.plot( data_x, data_y, 'o', label='data')
plt.plot(points, yvals, 'r',linewidth=4.0,label='fit')
plt.savefig('curvefit1.pdf',bbox_inches="tight")


#-------------------------------------------------------------------------------------
#              fit the data with Quadratic fitting
#-------------------------------------------------------------------------------------
popt, pcov = curve_fit(func2, data_x, data_y)
a_qudratic = popt[0]

yvals=func2(points, a_qudratic)
# yvals=func(x, *popt)
plt.figure(figsize=(18.5,10.5))
plt.plot( data_x, data_y, 'o', label='data')
plt.plot(points, yvals, 'r',linewidth=4.0,label='fit')
plt.savefig('curvefit2.pdf',bbox_inches="tight")

#----------------------------------------------------------------------------------
#                       apply linear or qudratic fitting
#----------------------------------------------------------------------------------
energy_correction=open('energy_correction.dat','w')

de_correct1 = np.zeros(len(position))
de_correct2 = np.zeros(len(position))
for i in range(len(position)):
    de_correct1[i] = energy1[i] - func1(position[i],a_linear)  # apply energy correction to energy difference
    de_correct2[i] = energy1[i] - func2(position[i],a_qudratic)

    line = '%16.8f %16.8f %16.8f\n' %(position[i], de_correct1[i], de_correct2[i])
    energy_correction.write(line)
energy_correction.close

#===================================================================================
plt.figure(figsize=(18.5,10.5))
ax = plt.subplot(1,1,1)
#--------------------------------------------------------------------
#                     plot figure
#--------------------------------------------------------------------
plt.scatter(rd, energy1, s=200, label= 'uncorrected')
plt.plot(rd, energy1, '--', linewidth=5)

if(correct_flag == 'y'):
    plt.scatter(position/ position[-1], energy,s=200, label= 'babel')
    plt.plot( position / position[-1], energy, '--', linewidth=5)

plt.scatter(position/ position[-1], de_correct2,s=200, label= 'qudratic')
plt.plot( position / position[-1], de_correct2, '--', linewidth=5)

plt.scatter(position/ position[-1], de_correct1,s=200, label= 'linear')
plt.plot( position / position[-1], de_correct1, '--', linewidth=5)

#--------------------------------------------------------------------
ax.tick_params(axis='x', pad=15)  # distance between axis and text
ax.tick_params(axis='y', pad=15)
#--------------------------------------------------------------------
ax.spines['left'].set_linewidth(3.0)
ax.spines['right'].set_linewidth(3.0)
ax.spines['top'].set_linewidth(3.0)
ax.spines['bottom'].set_linewidth(3.0)

#===================================================================================
plt.minorticks_on()
plt.tick_params(which='major',direction='in',width=3.0,length=12)  # 
plt.tick_params(which='minor',direction='in',width=3.0,length=5)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)

plt.axhline(y=0.0, linestyle='--',xmin=0.0, xmax=1.0, linewidth=3.5, color = 'k' )
plt.xlim(0, 1)
plt.ylim(-0.002,0.005)

plt.xlabel('x/b', fontsize='35')
plt.ylabel(r'$\Delta E(eV)$', fontsize='35')

lg=plt.legend(loc=2,bbox_to_anchor=(0.02,1.0),fontsize=28,frameon=True,edgecolor='black')
lg.get_frame().set_linewidth(4)
# lg.get_frame().set_edgecolor("red")  # set the color of frame to red
#ax.xaxis.set_major_locator(xmajorLocator)
#=================================================================================

plt.savefig("neb_correction.pdf",bbox_inches="tight")
plt.show()


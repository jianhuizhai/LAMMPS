'''This code is used to fit diregistry data by using two arctan function which is suitable to wide spread core'''

import numpy as np
from scipy.optimize import curve_fit
import sympy as sp
import sys
import matplotlib.pylab as plt

#===============================================================================================================
#                                       objective function
#===============================================================================================================
def func(x ,mean1, width1, alpha1, mean2, width2):
    return b_calculated/2 + b_calculated/np.pi* ( alpha1*np.arctan( (x-mean1)/width1 ) + (1-alpha1)*np.arctan(x-mean2)/width2 )
def rho(x , mean1, width1, alpha1, mean2, width2):
    return b_calculated/np.pi*( alpha1*width1/( np.power(x-mean1,2)+np.power(width1,2) ) + (1-alpha1)*width2/( np.power(x-mean2,2)+np.power(width2,2) ))

#=================================================================================================================
#                           write disloc info to TwoArctanInfo.dat file
#=================================================================================================================
linecommon = '=========================================================\n'

print('The output file is:  TwoArctanInfo.dat')
Info = open('TwoArctanInfo.dat','w')
Info.write(linecommon)
line = 'Info about disloc'+'\n'
Info.write(line)
Info.write(linecommon)
line = 'DislocNum             b_c,          alpha1,        mean1,         width1,       mean2,          width2,    core_position'+'\n'
Info.write(line)
#===============================================================================================================
files = ['plane1Dis1', 'plane1Dis2', 'plane2Dis1', 'plane2Dis2']

for filename in files: 
    print('filename is :', filename)
    position, disregistry = np.loadtxt('disregistry.'+filename+ '.dat', unpack=True)
    b_calculated = disregistry[-1] - disregistry[0]

    popt, pcov = curve_fit(func, position, disregistry, p0=[90, 2.0, 0.7, 130, 1.0])
    mean1 = popt[0]
    width1= popt[1]
    alpha1= popt[2]
    mean2 = popt[3]
    width2= popt[4]

    #print('alpha1 = ', alpha1)
    #print('mean1  = ', mean1)
    #print('width1 = ', width1)
    #print('mean2  = ', mean2)
    #print('width2 = ', width2)

    #---------------------------------------------------------------------------------------------------------
    #                             obtain dislocation core position
    #---------------------------------------------------------------------------------------------------------
    x = sp.Symbol("x")
    core_position = sp.nsolve(alpha1*sp.atan( (x-mean1)/width1 ) + (1-alpha1)*sp.atan( (x-mean2)/width2) , 120)
    #print('Position of dislocation core is : ', core_position)

    #---------------------------------------------------------------------------------------------------------
    #                  write the fitting parameter to TwoArctanInfo.dat file
    #---------------------------------------------------------------------------------------------------------
    line1 = '%-14s' %filename
    line2 = '%14.6f %14.6f %14.6f %14.6f %14.6f %14.6f %14.6f' %(b_calculated, alpha1, mean1, width1, mean2, width2, core_position)
    line  = line1 + line2 +'\n'
    Info.write(line)

    #=================================================================================================================
    x=[i for i in np.arange(0.,np.max(position),0.1)]
    x = np.array(x)
    yvals=func(x, mean1, width1, alpha1, mean2, width2)

    #=================================================================================================================
    fig, ax1 = plt.subplots(figsize=(18.5,10.5))
    ax1.plot( position, disregistry, 'o', label='data')
    ax1.plot(x, yvals, 'r',linewidth=5.0,label='fit')
    ax1.set_xlabel("x"+'(' + r'$\AA$' +')')

    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel(r'$\phi$'+'(' + r'$\AA$' +')', color='red')
    ax1.tick_params('y', colors='red')

    ax2 = ax1.twinx()
    ax2.plot(x, rho(x, mean1, width1, alpha1, mean2, width2), 'blue', linewidth=3.0, label ='density')
    ax2.set_ylabel(r'$\rho$', color='blue')
    ax2.tick_params('y', colors='blue')
    fig.tight_layout()

    plt.savefig('disregistry'+filename+'_twoArctan.pdf')
    #plt.show()

#====================================================================================================================
Info.close

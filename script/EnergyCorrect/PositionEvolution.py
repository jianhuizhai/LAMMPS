import numpy as np
import os
import linecache
from search import SearchFile
from scipy.optimize import curve_fit
import matplotlib.pylab as plt

#======================================================================================
#       define objective function to fit disregistry and density of disregistry
#======================================================================================
def func(x,mean,width):
    return b_calculated/np.pi*np.arctan((x-mean)/width)+b_calculated/2
def rho(x, mean, width):
    return b_calculated/np.pi*width/(np.power(x-mean,2)+ np.power(width,2))
#======================================================================================

linecommon = '===============================================================\n'
#======================================================================================
print("The character of dislocation: positive or negtive .")
character = input("Please type p or n. \n")

if(character == 'p'):
    dataLine = 11
elif(character == 'n'):
    dataLine = 10
else:
    print("Unknown dislocation character.")
    exit()
#====================================================================================
#                           specify picture size
#====================================================================================
plt.figure(figsize=(18.5,10.5))

img = int(input("Number of replicas: \n"))
#=====================================================================================
#             open file to store image core position
#=====================================================================================
CorePosition = open('CorePosition_'+character+'.dat','w')

mean = np.zeros(img)
#-------------------------------------------------------------------------------------
for i in range(img):
    #=================================================================================
    #                    get specified file in each folder
    #=================================================================================
    os.chdir("img"+str(i+1))
    print("cwd:   ", os.getcwd() )
    filename = SearchFile.findfile('.', 'DislocInfo_', '.')[2:]
    print("filename is ", filename)
    line = linecache.getline(os.path.abspath(filename), dataLine)
    mean[i] = float( line.split()[6] )
    width= float( line.split()[7] )
    #print('mean = ', mean)
    #print('width= ', width)
    os.chdir("../")
    print("cwd: ", os.getcwd())
    print(linecommon)
#======================================================================================
#                            curve fitting
#======================================================================================
    line = '%-2i %16.8f %16.8f %16.8f\n' %(i+1, round(mean[i],3), round(mean[i]-mean[0],2),round(width, 3) )
    CorePosition.write(line)
CorePosition.close     # close data file

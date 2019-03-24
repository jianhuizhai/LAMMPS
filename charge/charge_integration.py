import sys
import numpy as np

filename = sys.argv[1]
x, y, density = np.loadtxt(filename, skiprows=4, unpack=True)

dx = x[0]
dy = y[0]

print('dx = ' ,dx)
print('dy = ' ,dy)

# specify the integral area
xlo = float(input("The minimum value of x is : "))
xhi = float(input("The maxmium value of x is : "))
ylo = float(input("The minimum value of y is : "))
yhi = float(input("The maxmium value of y is : "))

charge = 0.0 

for i in range(len(x)):
    if(x[i]<=xhi and x[i]>=xlo):
        if(y[i]<= yhi and y[i]>= ylo):
            charge = charge + dx*dy*density[i]

print("The charge of the integral area is : ", charge)

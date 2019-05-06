import os

xlo = int(input("minimun running id : "))
xhi = int(input("maximum running id : "))

for i in range(xlo, xhi+1, 1):
    os.system('scancel '+str(i))

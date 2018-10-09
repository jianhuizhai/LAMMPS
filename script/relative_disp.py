import numpy as np
import sys
import matplotlib.pylab as plt


begin = sys.argv[1]
end  = sys.argv[2]
filename = sys.argv[3]

skipline = 9
begin_data = np.loadtxt(begin, skiprows=skipline, usecols=[4])
end_data   = np.loadtxt(end,   skiprows=skipline, usecols=[4])

print("begin_data =", begin_data)
# print("len(begin_data)=", len(begin_data))

plt.plot(begin_data, end_data-begin_data, 'o')

plt.savefig(filename+'.pdf')
plt.show()
import numpy as np
import matplotlib.pyplot as plt

#plt.rc('text', usetex = True)
#plt.rc('font', family = 'Times New Roman')

f = open('tune.dat')
f.readline()
d = f.readlines()
f.close()

dat = np.genfromtxt(d, dtype = str)
E = np.asarray(map(lambda x: float(x), dat[:, 0]))
H = np.asarray(map(lambda x: float(x), dat[:, 1]))
V = np.asarray(map(lambda x: float(x), dat[:, 2]))


ch = '#731cef'
cv = '#20ea45'

plt.plot(H, V, 'x-',
         color = '#fa3dd0',
         label = 'Tune')
plt.xlabel('Qh')
plt.ylabel('Qv')
plt.savefig('tune_diagram.pdf')
plt.show()

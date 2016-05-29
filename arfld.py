import numpy as np
import matplotlib.pyplot as plt

class bdata:
    def __init__(self):
        self.get_data()
        
    def get_data(self):
        f = open('zgoubi.table', 'r')
        header = []
        data = []
        for i in range(8):
                header.append(f.readline())
        line = f.readlines()
        for l in line:
                data.append(l.split())
        npd = np.asarray(data)
        x = np.asarray(map(lambda x: float(x), npd[:, 0]))
        y = np.asarray(map(lambda x: float(x), npd[:, 1]))
        z = np.asarray(map(lambda x: float(x), npd[:, 2]))
        bx = np.asarray(map(lambda x: float(x), npd[:, 3]))
        by = np.asarray(map(lambda x: float(x), npd[:, 4]))
        bz = np.asarray(map(lambda x: float(x), npd[:, 5]))

        r = np.round(np.sqrt(x**2 + y**2))
        th = np.round(np.arctan2(y, x) * 180 / np.pi, 2)

        self.r = r
        self.z = y
        self.th = th
        
        self.by = bx
        self.bz = by
        self.bx = bz
        
if __name__ == '__main__':
    f = open('zgoubi.table', 'r')
    newf = open('new_zgoubi.table', 'w')
    header = []
    data = []
    for i in range(8):
        header.append(f.readline())
    line = f.readlines()
    for l in line:
        data.append(l.split())
    npd = np.asarray(data)

    x = np.asarray(map(lambda x: float(x), npd[:, 0]))
    y = np.asarray(map(lambda x: float(x), npd[:, 1]))
    z = np.asarray(map(lambda x: float(x), npd[:, 2]))
    bx = np.asarray(map(lambda x: float(x), npd[:, 3]))
    by = np.asarray(map(lambda x: float(x), npd[:, 4]))
    bz = np.asarray(map(lambda x: float(x), npd[:, 5]))

    r = np.round(np.sqrt(x**2 + y**2))
    th = np.arctan2(y, x)
    br = bx * np.cos(th) + by * np.sin(th) # -> br
    bth = -bx * np.sin(th) + by * np.cos(th) # -> bx

    for index, l in enumerate(header):
        if index == 0:
            s = '430. 1.0 0.01 0.1 0 0 0\n'
            newf.write(s)
        else:
            newf.write(l)
    for i in range(len(data)):
        dline = '%.5e %.10e %.3e %.8e %.8e %.8e\n' % (r[i], th[i], z[i], bx[i], bz[i], by[i])
        newf.write(dline)
        
    f.close()
    

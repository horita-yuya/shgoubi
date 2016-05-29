import numpy as np
import sys

indKEX = 0
indY0 = 2
indT0 = 3
indZ0 = 4
indP0 = 5
indS0 = 6
indt0 = 7
indY = 9
indT = 10
indZ = 11
indP = 12
indS = 13
indt = 14
indENEKI = 23
indENERG = 24
indM = 28
indIPASS = 37
indLET = -1

indFai = [indKEX, indY0, indT0, indZ0, indP0, indS0, indt0,
          indY, indT, indZ, indP, indS, indt,indENEKI, indENERG, indM, indIPASS, indLET]

def tunes(Y, Z, IPASS, LET):
    Y = np.asarray(map(lambda x: float(x) * 10, Y))
    Z = np.asarray(map(lambda x: float(x) * 10, Z))
    rcl = np.sum(Y) / len(Y)
    Y = np.asarray(map(lambda x: x - rcl, Y))
    
    Fs = 1
    Ts = 1
    x = np.arange(0, float(IPASS[-1]), Ts)
    n = len(Y)
    y_ft = np.fft.fft(Y)[range(n / 2)]
    z_ft = np.fft.fft(Z)[range(n / 2)]
    freq = np.fft.fftfreq(n, Ts)[range(n / 2)]
    rfreq = freq[abs(y_ft) == np.max(abs(y_ft))]
    zfreq = freq[abs(z_ft) == np.max(abs(z_ft))]
    
    print '%.5f %.5f' % (rfreq[0] * 12, zfreq[0] * 12)
    


def racceptance(Y, T, Y0, T0, IPASS, LET):
    y = np.asarray(map(lambda x: float(x) * 10, Y))
    y_ = np.asarray(map(lambda x: float(x), T))
    y0 = np.asarray(map(lambda x: float(x) * 10, Y0))
    y0_ = np.asarray(map(lambda x: float(x), T0))
    turn = np.asarray(map(lambda x: int(x), IPASS))
    rcl = np.sum(y) / len(y)
    y = np.asarray(map(lambda x: x - rcl, y))
    y0 = np.asarray(map(lambda x: x - rcl, y0))

    y0_one = y0[turn == 1]
    y0__one = y0_[turn == 1]

def zacceptance(Z, P, Z0, P0, IPASS, LET):
    z = np.asarray(map(lambda x: float(x) * 10, Z))
    z_ = np.asarray(map(lambda x: float(x), P))
    z0 = np.asarray(map(lambda x: float(x) * 10, Z0))
    z0_ = np.asarray(map(lambda x: float(x), P0))
    turn = np.asarray(map(lambda x: int(x), IPASS))

    z0_one = z0[turn == 1]
    z0__one = z0_[turn == 1]

if __name__ == '__main__':
# data reading and set variables from here
    f = open('zgoubi.fai', 'r')
    row_datas = f.readlines()
    header = []
    row_data = []
    row_data_split = []
    
    for index, d in enumerate(row_datas):
        if index <= 3:
            header.append(d)
        else:
            row_data.append(d)
    numbers = map(lambda s: s.strip(), header[1].split(','))
    values = map(lambda s: s.strip(), header[2].split(','))
    units = map(lambda s: s.strip(), header[3].split(','))
    
    for d in row_data:
        row_data_split.append(d.split())
    ary_data = np.asarray(row_data_split)
    KEX = ary_data[:, indKEX]
    Y0 = ary_data[:, indY0]
    T0 = ary_data[:, indT0]
    Z0 = ary_data[:, indZ0]
    P0 = ary_data[:, indP0]
    S0 = ary_data[:, indS0]
    t0 = ary_data[:, indt0]
    Y = ary_data[:, indY]
    T = ary_data[:, indT]
    Z = ary_data[:, indZ]
    P = ary_data[:, indP]
    S = ary_data[:, indS]
    t = ary_data[:, indt]
    ENEKI = ary_data[:, indENEKI]
    ENERG = ary_data[:, indENERG]
    M = ary_data[:, indM]
    IPASS = ary_data[:, indIPASS]
    LET = ary_data[:, indLET]
    
    dFai = [KEX, Y0, T0, Z0, P0, S0, t0,
          Y, T, Z, P, S, t, ENEKI, ENERG, M, IPASS, LET]
    
    args = sys.argv
    if args[1] != IPASS[-1]:
        print "Divergence"
        exit(99)
# data reading and set variables to here
    tunes(Y, Z, IPASS, LET)

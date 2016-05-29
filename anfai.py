import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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

def twip(xdata, ydata):
    def Courant_Snyder(x, a1, a2, a3):
        return a1 * x[0]**2 + a2 * x[0]*x[1] + a3 * x[1]**2 - 1
    zeroData = np.zeros_like(xdata)
    effID, pconv = curve_fit(Courant_Snyder, [xdata, ydata], zeroData)
    x0max = np.max(xdata)
    beta = np.sqrt(x0max**2 * effID[2])
    epsilon = beta / effID[2]
    gamma = effID[0] * epsilon
    alpha = effID[1] * epsilon / 2
    
    return {'alpha': alpha, 'beta': beta, 'gamma': gamma, 'epsilon': epsilon}

def tunes(Y, Z, IPASS, LET):
    Y = np.asarray(map(lambda x: float(x) * 10, Y))
    Z = np.asarray(map(lambda x: float(x) * 10, Z))
    rcl = np.sum(Y) / len(Y)
    Y = np.asarray(map(lambda x: x - rcl, Y))
    
    Fs = 1
    Ts = 1
    x = np.arange(0, float(IPASS[-1]), 1)
    n = len(Y)
    y_ft = np.fft.fft(Y)[range(n / 2)]
    z_ft = np.fft.fft(Z)[range(n / 2)]
    freq = np.fft.fftfreq(n, Ts)[range(n / 2)]
    rfreq = freq[abs(y_ft) == np.max(abs(y_ft))]
    zfreq = freq[abs(z_ft) == np.max(abs(z_ft))]
    rcolor = '#aadaff'
    rpcolor = '#5555ff'
    zcolor = '#aaffda'
    zpcolor = '#55ff55'
    
    plt.subplot(311)
    plt.plot(x, Y, '-',
             color = rcolor)
    plt.xlabel('Revolutions')
    plt.ylabel('$r$ [mm]')
    plt.subplot(312)
    plt.plot(x, Z, '-',
             color = zcolor)
    plt.xlabel('Revolutions')
    plt.ylabel('$z$ [mm]')
    
    plt.subplot(313)
    plt.plot(freq, abs(y_ft) / np.max(abs(y_ft)), '-',
             color = rcolor)
    plt.plot([rfreq, rfreq], [0, 1], '-.',
             color = rpcolor,
             alpha = 0.8,
             label = '%.3f' % (rfreq))
    plt.plot(freq, abs(z_ft) / np.max(abs(z_ft)), '-',
             color = zcolor)
    plt.plot([zfreq, zfreq], [0, 1], '-.',
             color = zpcolor,
             alpha = 0.8,
             label = '%.3f' % (zfreq))
    plt.xlabel('$\\nu_x$')
    plt.ylabel('Strength')
    plt.legend(loc = 'best')
    plt.tight_layout()
    plt.savefig('tunes.pdf')
    plt.show()

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
    
    plt.gca()
    plt.xlabel('$r$ [mm]')
    plt.ylabel("$r'$ [mrad]")
#    plt.xlim(3.6, 6.3)
#    plt.ylim(-0.43, 0.43)
    plt.plot(y, y_,
             'o',
             color = '#99ff99',
             alpha = 0.8,
             markeredgewidth = 1.0,
             markeredgecolor = '#88ff88',
             ms = 2.0)
    plt.plot(y0_one, y0__one,
             'x',
             color = '#ff0000',
             alpha = 0.9,
             ms = 5.0,
             label = 'initial')
    plt.legend(loc = 'best', numpoints = 1)
    plt.savefig('r_acpt')
    plt.show()

def zacceptance(Z, P, Z0, P0, IPASS, LET):
    z = np.asarray(map(lambda x: float(x) * 10, Z))
    z_ = np.asarray(map(lambda x: float(x), P))
    z0 = np.asarray(map(lambda x: float(x) * 10, Z0))
    z0_ = np.asarray(map(lambda x: float(x), P0))
    turn = np.asarray(map(lambda x: int(x), IPASS))

    z0_one = z0[turn == 1]
    z0__one = z0_[turn == 1]
    

    plt.gca()
    plt.xlabel('$z$ [mm]')
    plt.ylabel("$z'$ [mrad]")
#    plt.xlim(3.6, 6.3)
#    plt.ylim(-0.43, 0.43)
    plt.plot(z, z_,
             'o',
             color = '#99ff99',
             alpha = 0.8,
             markeredgewidth = 1.0,
             markeredgecolor = '#88ff88',
             ms = 2.0)
    plt.plot(z0_one, z0__one,
             'x',
             color = '#ff0000',
             alpha = 0.9,
             ms = 5.0,
             label = 'initial')
    plt.legend(loc = 'best', numpoints = 1)
    plt.savefig('z_acpt')
    plt.show()

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
    for i in indFai:
        print str(values[i]) + ' '*5 + str(units[i])
# data reading and set variables to here
    print values
    plt.rc('text', usetex = True)
    plt.rc('font', family = 'Times New Roman')
    racceptance(Y, T, Y0, T0, IPASS, LET)
    zacceptance(Z, P, Z0, P0, IPASS, LET)
    tunes(Y, Z, IPASS, LET)

    
    plt.show()

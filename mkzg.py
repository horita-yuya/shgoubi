from math import *
import sys

def TITLE(s):
    return s + '\n'

def OBJET(energy, init_r = 460, delta_r = 1, num_p = 1):
    fi = ''
    title = "'OBJET'\n"
    fi += title
    mp = 938.2720813
    brho = sqrt(energy*(energy + 2 * mp)) / 0.2997925
    s_brho = str(brho) + '\n'
    fi += s_brho
    fi += '2\n'
    s_num_p = str(num_p)
    fi += s_num_p + ' 1' + '\n'
    for i in range(num_p):
        fi += str(init_r + delta_r * i) + ' 0.0 0.1 0.01 0.0 1 "' + str(i + 1) + '"\n'
    fi += '1 ' * num_p + '\n'
    fi += '\n'

    return fi

def PARTICUL():
    fi = ''
    fi += "'PARTICUL'\n"
    fi += ' 938.2720813 1.60217733D-19 0. 0. 0.\n'
    fi += '\n'
    return fi

def TOSCA():
    fi = ''
    fi += "'TOSCA'\n"
    fi += ' 0 0\n'
    fi += ' -1.e-3 1. 1. 1.\n'
    fi += ' HEADER_8\n'
    fi += ' 3001 121 41 20\n'
    fi += ' new_zgoubi.table\n'
    fi += ' 0 0 0 0\n'
    fi += ' 2\n'
    fi += ' 0.1\n'
    fi += ' 2\n'
    fi += ' 0. 0. 0. 0.\n'
    fi += '\n'
    return fi
def FAISTORE():
    fi = ''
    fi += "'FAISTORE'\n"
    fi += 'zgoubi.fai\n'
    fi += ' 1\n'
    fi += '\n'
    return fi
def REBELOTE(revTime = 100):
    fi = ''
    fi += "'REBELOTE'\n"
    fi += str(revTime) + ' 0.2 99\n'
    fi += '\n'
    return fi
def END():
    return "'END'"
    
if __name__ == '__main__':
    argvs = sys.argv
    print argvs[1]
    print argvs[2]
    
    fi = ''
    fi += TITLE('tracking')
    fi += OBJET(energy = float(argvs[1]), init_r = float(argvs[2]), delta_r = 0.1, num_p = 1)
    fi += PARTICUL()
    fi += TOSCA()
    fi += FAISTORE()
    fi += REBELOTE(revTime = int(argvs[3]) - 1)
    fi += END()

    fil = open('zgoubi.dat', 'w')
    fil.write(fi)
    fil.close()



    
    

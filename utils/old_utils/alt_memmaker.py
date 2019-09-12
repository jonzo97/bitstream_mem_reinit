import sys
FNAME = 'designs/init/init.txt'
WIDTH = 16
DEPTH = 1024
DATA = 'ffff'
PERLINE = 16
DATAFILE = False


def main():
    fname = sys.argv[1]
    width = sys.argv[2]
    depth = sys.argv[3]
    data1 = sys.argv[4]
    data2 = sys.argv[5]
    perline = sys.argv[6]

    data = [data1, data2]

    if type(width) is str:
        width = int(width)
    if type(depth) is str:
        depth = int(depth)
    if type(perline) is str:
        perline = int(perline)

    make_mem(fname=fname,
             width=width,
             depth=depth,
             data=data,
             perline=perline)
    '''
    make_mem(fname='designs/init/1_by_16k.txt',
             width=1,
             depth=16384,
             data='1',
             perline=128)
    make_mem(fname='designs/init/1_by_32k.txt',
             width=1,
             depth=16384*2,
             data='1',
             perline=128)

    make_mem(fname='designs/init/2_by_8k.txt',
             width=2,
             depth=8192,
             data='2',
             perline=128)
    make_mem(fname='designs/init/2_by_16k.txt',
             width=2,
             depth=16384,
             data='2',
             perline=128)

    make_mem(fname='designs/init/3_by_5k.txt',
             width=3,
             depth=5000,
             data='4',
             perline=128)

    make_mem(fname='designs/init/16_by_1024.txt',
             width=16,
             depth=1024,
             data='7000',
             perline=16)
    '''


def make_mem(fname=FNAME, width=WIDTH, depth=DEPTH, data=DATA, perline=PERLINE, datafile=DATAFILE):
    vals = []
    if datafile:
        with open(datafile, 'r') as f:
            for line in f:
                vals.append(line.split(' '))
    else:
        #vals = [hex(int(data))[2:] for x in range(depth)]
        vals = [data[x % 2] for x in range(depth)]
    with open(fname, 'w+') as f:
        vals = [vals[x:x+perline] for x in range(0, depth, perline)]
        for val in vals:
            f.write(' '.join(val))
            f.write('\n')
    print(f'we done, printed to {fname}')


if __name__ == "__main__":
    main()

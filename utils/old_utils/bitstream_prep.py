import sys
import os
LISTFILE = 'utils/testlist.txt'


class Test:
    width, depth, depthname, data, perline, frmt = [None for x in range(6)]

    def __init__(self, width=1, depth=16384,
                 depthname='16k', data='0',
                 perline=256, frmt='hex'):
        self.width = width
        self.depth = depth
        self.depthname = depthname
        self.data = data
        self.perline = perline
        self.frmt = frmt


def main():
    listfile = LISTFILE
    opt = None
    if len(sys.argv) >= 2:
        opt = sys.argv[1]
        if len(sys.argv) >= 3:
            listfile = sys.arg[2]
    tests = []
    with open(LISTFILE, 'r') as f:
        for line in f:
            if line is not None:
                line = line.split(' ')
                print(f'{".".join(line)}')
                assert len(line) is 6
                width, depth, depthname, data, perline, frmt = line
                currtest = Test(width=width, depth=depth, depthname=depthname,
                                data=data, perline=perline, frmt=frmt)
                tests.append(currtest)
    if opt == '-build':
        print(f'Building tests')
        for test in tests:
            make_mem_and_top(test)
    elif opt == '-extract':
        print(f'Generating bitstreams and extracting memories for tests')
        for test in tests:
            generate_and_extract(test)
    else:
        print('Please specify -build or -extract')
        # print(f'Building and extracting for tests')
        # for test in tests:
        #     make_mem_and_top(test)
        # for test in tests:
        #     generate_and_extract(test)


def make_mem_and_top(d):
    command = f'bash make_mem_and_top.sh {d.width} {d.depth} {d.depthname} {d.data} {d.perline} {d.frmt}'
    os.system(command)


def generate_and_extract(d):
    command = f'bash gen_and_extract.sh {d.width} {d.depth} {d.depthname} {d.perline}'
    os.system(command)


if __name__ == '__main__':
    main()

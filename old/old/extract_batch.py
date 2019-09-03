import sys
import os

LISTFILE='utils/bitstream_list.txt'


def main():
    listfile=None
    if len(sys.argv)>=2:
        listfile = sys.argv[1]
    else:
        listfile=LISTFILE
    with open(listfile, 'r') as f:
        for line in f:
            line = line.split(' ')
            print(f'{line[0]}.{line[1]}')
            assert len(line) is 2
            bit, mem = line[0], line[1]
            command = f'bash utils/extract.sh {bit} {mem}'
            print(command)
            os.system(command)


if __name__ == "__main__":
    main()

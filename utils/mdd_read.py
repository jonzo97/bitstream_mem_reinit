
import sys


def main():
    mdd_name = sys.argv[1]
    print(f'Reading {mdd_name}')
    read_mdd(fname=mdd_name)


def read_mdd(fname):
    cells = {}
    with open(fname, 'r') as f:
        addr = ''
        for ln in f:
            ln = ln.strip()
            ln = ln.split(' ')
            print(ln[0])
            if ln[0] == 'CELL':
                addr = ln[1]
                cells[addr] = {}
                # print(f'Addr set to {addr}')
            elif ln[0] == 'ENDCELL':
                addr = ''
                # print(f'End of cell')
                continue
            elif addr != '':
                cells[addr][ln[0]] = ln[1]
                # print(f'Assigned {ln[1]} to parameter {ln[0]} for {addr}')
    for key, cell in cells.items():
        print(f'CELL {key}')
        for param, val in cell.items():
            print(f'  {param:<27} {val}')


if __name__ == "__main__":
    main()

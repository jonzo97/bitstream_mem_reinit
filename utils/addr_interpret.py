import fasm
import fasm.output
import re
from utils.parseutil import fasmread


def main():
    myargs = parse_args()
    assert myargs.fasm is not None
    assert myargs.outfile is not None
    infasm = myargs.fasm
    outfile = myargs.outfile

    fasmtups = fasmread.get_fasm_tups(infasm)
    tiledata = get_sorted_tiledata(fasmtups)
    addr_data = interpret_addrs(tiledata)
    print_addr_data(addr_data, outfile=outfile)


def interpret_addrs(tiledata):
    addrline = re.compile(
        r'BRAM_(?:L|R)_X\d+Y\d+.BRAM_ADDR(?P<aorb>ARD|BWR)ADDR(?P<loru>L|U)(?P<num>\d+).BRAM_(?P<type>IMUX|CASCINTOP|CASCINBOT)')
    # r'BRAM_ADDR(ARD|BWR)ADDR(L|U)(\d+).BRAM_(IMUX|CASCINTOP|CASCINBOT)')
    addr_data = {}
    for tile, tiletupes in tiledata.items():
        addr_data[tile] = {}
        for tup in tiletupes:
            # print(tup.set_feature.feature)
            addrmatch = re.match(
                pattern=addrline, string=tup.set_feature.feature)
            if addrmatch:
                # print('matched')
                aorb = addrmatch.group("aorb")
                loru = addrmatch.group("loru")
                num = addrmatch.group("num")
                addrtype = addrmatch.group("type")
                groupaddr = f'{aorb} {loru}'
                if groupaddr not in addr_data[tile].keys():
                    addr_data[tile][groupaddr] = {}
                addr_data[tile][groupaddr][num] = addrtype

            # feature = ' '.join('.'.split(tup.set_feature.feature))
            # feature = tup.set_feature.feature.split('.')[1:]
            # if 'BRAM_ADDR' in feature[0]:
            #     print(feature)

    return addr_data


def print_addr_data(addrdata, outfile=None):
    if outfile == None:
        interpret_addrs
        for tile, tilegroups in addrdata.items():
            print(tile)
            for groupaddr, addrgroup in tilegroups.items():
                print(f'\t{groupaddr}')
                inorder_addrs = sorted([int(key) for key in addrgroup.keys()])
                for addr in inorder_addrs:
                    print(f'\t\t{addr}: {addrgroup[str(addr)]}')
    else:
        with open(outfile, 'w+') as of:

            inorder_tiles = sorted([tile for tile in addrdata.keys()])
            # for tile, tilegroups in addrdata.items():
            for tile in inorder_tiles:
                tilegroup = addrdata[tile]
                lines = []
                lines.append(f'{tile}')
                sorted_groups = sorted([group for group in tilegroup.keys()])
                for group in sorted_groups:
                    groupaddr = group
                    addrgroup = tilegroup[groupaddr]
                    # for groupaddr, addrgroup in tilegroup.items():
                    # of.write(f'\tADDR{groupaddr}')
                    # of.write('\n')
                    if len(lines) <= 1:
                        lines.append(f'    ')
                    lines[1] = lines[1]+f'{groupaddr:<14}'
                    inorder_addrs = sorted([int(key)
                                            for key in addrgroup.keys()])
                    for linenum, addr in enumerate(inorder_addrs, start=2):
                        if linenum >= len(lines):
                            lines.append(f'{str(addr)+":":<4}')
                        lines[linenum] = lines[linenum] + \
                            f'{addrgroup[str(addr)]:<14}'
                        # of.write(f'\t\t{addr:<2}: {addrgroup[str(addr)]}')
                        # of.write('\n')
                for line in lines:
                    of.write(f'{line}\n')
                of.write(f'\n\n')


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='Alter BRAM initialization values')
    parser.add_argument(
        '-fasm',
        help="Fasm to be read")
    parser.add_argument(
        '-outfile',
        help="Output file")
    args = parser.parse_args()
    return args


def get_sorted_tiles(tups):
    in_use = re.compile(r'BRAM_[LR]_X\d+Y\d+\.RAMB18_Y(\d)\.IN_USE')
    tiles = set()
    for tup in tups:
        feature = tup.set_feature.feature
        if re.match(pattern=in_use, string=feature):
            tilename = get_tup_tileaddr(tup)
            tiles.add(tilename)
    tiles = [tile for tile in tiles]
    # print('Unsorted')
    # for tile in tiles:
    #     print(tile)
    # print('Sorted')
    # tiles = sorted(tiles, reverse=True)
    # for tile in tiles:
    #     print(tile)
    return tiles


def get_sorted_tiledata(tups):
    tiles = get_sorted_tiles(tups)
    tiledict = {}
    for tile in tiles:
        tiledict[tile] = set()
    for tup in tups:
        tileaddr = get_tup_tileaddr(tup)
        if tileaddr in tiledict.keys():
            tiledict[tileaddr].add(tup)
    return tiledict


def get_tup_tileaddr(tup):
    # tilename = '.'.join(tup.set_feature.feature.split('.')[0:2])
    tilename = f'{tup.set_feature.feature.split(".")[0]}'
    return tilename


if __name__ == "__main__":
    main()

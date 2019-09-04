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
    datatups = simplify_tiledata(tiledata)
    print_tiledata(datatups, outfile=outfile)


def simplify_tiledata(tiledata):
    in_use = re.compile(r'BRAM_[LR]_X\d+Y\d+\.RAMB18_Y(\d)\.IN_USE')
    init = re.compile(
        r'((BRAM_[LR]_X\d+Y\d+)\.(RAMB\d\d_Y\d+))\.((INITP?_)?[0-9a-fA-F]{2})')
    # data = []
    for tile, tiletups in tiledata.items():
        for tup in tiletups:
            feature = tup.set_feature.feature
            if in_use.match(feature) or init.match(feature):
                yield tup
    #             data.append(tup)
    # return data


def print_tiledata(datatups, outfile):
    with open(outfile, 'w') as f:
        datatups = fasm.output.merge_and_sort(datatups)
        f.write(fasm.fasm_tuple_to_string(datatups))
        # for tup in tuplist:
        # print(type(tup))
        # f.write(f'{fasm.fasm_line_to_string(tup)}\n')


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
    tilename = f'{tup.set_feature.feature.split(".")[0:1]}'
    return tilename


if __name__ == "__main__":
    main()

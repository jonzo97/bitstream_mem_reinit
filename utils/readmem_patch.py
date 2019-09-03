
# Width
# Depth
# new_init
# fasm_to_patch


import sys
import os
import fasm
import fasm.output
from utils.parseutil import fasmread

DIRECTORY = 'reconstruction_tests'
FASM = f'{DIRECTORY}/extracted.fasm'
INIT = f'{DIRECTORY}/init.txt'
MEMFASM = f'{DIRECTORY}/memfasm.fasm'
OUTFILE = f'{DIRECTORY}/patched.fasm'
WIDTH = 1
DEPTH = 16384


def main():
    myargs = parse_args()
    assert myargs.fasm is not None
    assert myargs.init is not None
    assert myargs.width is not None
    assert myargs.depth is not None
    fasm_to_patch = myargs.fasm
    new_init = myargs.init
    width = int(myargs.width)
    depth = int(myargs.depth)
    outfile = myargs.outfile

    # init_data = read_meminit(fname=new_init)
    fasm_tups = read_fasm(fasm_to_patch)
    # cleared_tups = fasmread.clear_init(fasm_tups)
    # in_use_tiles = fasmread.get_in_use_tiles(fasm_tups)

    # memfasm_tups = initdata_to_memfasm(init_data=init_data, tileorder=in_use_tiles,
    #                                    width=width, depth=depth, write_per_block=1, memfasm_name=f'{DIRECTORY}/mem.fasm')
    # merged = merge_tuples(cleared_tups=cleared_tups, mem_tups=memfasm_tups)

    # with open(outfile, 'w+') as out:
    #     out.write(fasm.fasm_tuple_to_string(merged))

    # print(f'Patched {outfile} successfully (probably)')
    # mem_from_reinit = f'{"/".join(new_init.split("/")[0:-1])}/init_frm_reinit.txt'
    # os.system(
    #     f'python3 ../meminit/fasmchange.py -extract_mem -infile {outfile} -outfile {mem_from_reinit}')
    # print(f'Memory extracted from {outfile} to {mem_from_reinit}')
    # print()

    # sorted_tiles = fasmread.get_sorted_tiledata(fasm_tups)
    # print()
    # rw_widths = fasmread.get_rw_widths(sorted_tiles)
    # for tile, width in rw_widths.items():
    #     print(f'{tile}: {width}')
    # print()
    # print()

    memfasm = initfile_to_memfasm(
        infile=new_init, fasm_tups=fasm_tups, memfasm_name=f'{DIRECTORY}/mem.fasm', width=width, depth=depth)
    cleared_tups = fasmread.clear_init(fasm_tups)
    merged = merge_tuples(cleared_tups=cleared_tups, mem_tups=memfasm)
    with open(outfile, 'w+') as out:
        out.write(fasm.fasm_tuple_to_string(merged))


def patch_fasm_with_mem(initfile, fasmfile, outfile, width, depth):
    # initdata_to_memfasm()
    fasm_tuples = fasm.parse_fasm_filename(fasmfile)
    mem_tuples = fasm.parse_fasm_filename('memfasm.fasm')
    merged_tuples = merge_tuples(fasm_tuples, mem_tuples)
    with open(outfile, 'w') as out:
        out.write(fasm.fasm_tuple_to_string(merged_tuples))
    import os
    os.remove('memfasm.fasm')


def merge_tuples(cleared_tups, mem_tups):
    if type(cleared_tups) is not list:
        cleared_tups = list(cleared_tups)
    if type(mem_tups) is not list:
        mem_tups = list(mem_tups)
    all_tups = fasmread.chain_tuples(cleared_tups, mem_tups)
    merged = fasm.output.merge_and_sort(all_tups)
    return merged


def initfile_to_memfasm(infile, fasm_tups, memfasm_name, width, depth):
    def initfile_to_initlist(infile, width, depth):
        init_data = read_meminit(fname=infile, width=width)
        assert len(init_data) == depth
        return init_data

    def initlist_to_writesdict(init, fasm_tups, width):
        wid_dict = fasmread.get_rw_widths(tups=fasm_tups)
        writesdict = {}
        for ramb18 in wid_dict.keys():
            writesdict[ramb18] = {'INIT': [], 'INITP': []}
        for data in init:
            tilecount = len(wid_dict)
            for count, (key, wid) in enumerate(wid_dict.items()):
                tiledata = [data[x]
                            for x in range(count, len(data), tilecount)]
                if wid_dict[key] > 8:
                    initp_len = wid_dict[key] % 8
                    writesdict[key]['INITP'].append(
                        ''.join(tiledata[0:initp_len]))
                    writesdict[key]['INIT'].append(
                        ''.join(tiledata[initp_len:]))
                else:
                    writesdict[key]['INIT'].append(''.join(tiledata))
        return writesdict

    def writesdict_to_initstr(writesdict):
        for key, init_types in writesdict.items():
            for init_type, init_data in init_types.items():
                writesdict[key][init_type] = ''.join(init_data[::-1])
        return writesdict

    def initstr_to_initlines(initstr):
        for key, init_types in initstr.items():
            for init_type, datastr in init_types.items():
                initlines = [datastr[x-256:x]
                             for x in range(len(datastr), 0, -256)]
                initstr[key][init_type] = initlines
        return initstr

    def initlines_to_memfasm(initlines):
        fasmlines = []
        for key, init_types in initlines.items():
            for init_type, init_lines in init_types.items():
                tile_init = f'{key}.{init_type}_'
                for count, line in enumerate(init_lines):
                    fasmline = f'{tile_init}{count:02X}[255:0] = 256\'b{line}'
                    fasmlines.append(fasmline)
                    print(fasmline)
        return fasmlines

    width = get_eff_width(width)
    initlist = initfile_to_initlist(infile, width, depth)
    writesdict = initlist_to_writesdict(
        init=initlist, fasm_tups=fasm_tups, width=width)
    initstr = writesdict_to_initstr(writesdict)
    initlines = initstr_to_initlines(initstr)
    memfasm = initlines_to_memfasm(initlines)
    with open(memfasm_name, 'w') as f:
        for line in memfasm:
            f.write(line)
            f.write('\n')
    return fasmread.get_fasm_tups(memfasm_name)


def initdata_to_memfasm(init_data, tileorder, width, depth, write_per_block, memfasm_name):
    def chunkify_block_data(datastring):
        datastring = [datastring[x-256:x]
                      for x in range(len(datastring), 0, -256)]
        return datastring

    def blockdata_to_fasmlines(blocks, pblocks=None):
        fasmlines = []
        for block, datadict in blocks.items():
            tile_init = f'{".".join(block.feature.split(".")[0:2])}.INIT_'
            for addr, initdata in datadict.items():
                initdata = f'{tile_init}{addr}[255:0] = 256\'b{initdata}\n'
                fasmlines.append(initdata)
        for block, datadict in pblocks.items():
            tile_init = f'{".".join(block.feature.split(".")[0:2])}.INITP_'
            for addr, initdata in datadict.items():
                initdata = f'{tile_init}{addr}[255:0] = 256\'b{initdata}\n'
                fasmlines.append(initdata)
                # print(initdata)
        return fasmlines

    blocks = dict()
    for tile in tileorder:
        blocks[tile] = ''
    parity_blocks = dict()
    eff_width = get_eff_width(width)
    parity_used = False
    if eff_width >= 9:
        parity_used = True

    for data in init_data:
        data = data.zfill(eff_width)
        data = [data[x:x+write_per_block]
                for x in range(0, eff_width, 1)]
        data_per_tile = ['' for x in range(len(tileorder))]
        for count, blockchunk in enumerate(data):
            curr_tilenum = count % len(tileorder)
            data_per_tile[curr_tilenum] = f'{data_per_tile[curr_tilenum]}{blockchunk}'
        for tile, data in zip(tileorder, data_per_tile):
            blocks[tile] = f'{data}{blocks[tile]}'
    if parity_used:
        for key, datastring in blocks.items():
            wid = eff_width
            pdata = ''.join(datastring[x-wid:x-wid+(wid % 8)]
                            for x in range(len(datastring), 0, -eff_width))
            # print(len(pdata)/256)
            # print(f'{int(pdata,2):X}')
            data = ''.join(datastring[x-wid+(wid % 8):x]
                           for x in range(len(datastring), 0, -eff_width))
            # print(len(data)/256)
            # print(f'{int(data,2):X}')
            blocks[key] = data
            parity_blocks[key] = pdata
        for key, datastring in parity_blocks.items():
            data = chunkify_block_data(datastring)
            lines = len(datastring)
            parity_blocks[key] = dict(zip([f'{x:02X}'
                                           for x in range(lines)], [substr for substr in data]))
    for key, datastring in blocks.items():
        data = chunkify_block_data(datastring)
        lines = len(datastring)
        blocks[key] = dict(zip([f'{x:02X}'
                                for x in range(lines)], [substr for substr in data]))
    fasmlines = blockdata_to_fasmlines(blocks=blocks, pblocks=parity_blocks)
    with open(memfasm_name, 'w') as f:
        for line in fasmlines:
            f.write(line)
    return fasmread.get_fasm_tups(memfasm_name)


def order_tiles():
    pass


def read_meminit(fname, width=None):
    with open(fname, 'r') as f:
        init_data = []
        for line in f:
            linedata = line.split(' ')
            for data in linedata:
                data = bin(int(data, 16))[2:]
                if width is not None:
                    data = data.zfill(width)
                init_data.append(data)
        return init_data


def read_fasm(fname):
    fasm_tuples = fasmread.get_fasm_tups(fname)
    tiles = fasmread.get_in_use_tiles(fasm_tuples)
    tiles = fasmread.get_tile_data(tups=fasm_tuples, in_use=tiles)
    for tileaddr, tups in tiles.items():
        # print(tileaddr)

        for tup in tups:
            pass
            # rint(f'\t{tup.feature}')
    return fasm_tuples


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='Alter BRAM initialization values')
    parser.add_argument(
        '-fasm',
        help="Fasm to be patched",
        default=FASM)
    parser.add_argument(
        '-outfile',
        help="Output file",
        default='reconstruction_tests/patched.fasm')
    parser.add_argument(
        '-init',
        help="New Init memory file used for patching",
        default=INIT)
    parser.add_argument(
        '-path',
        help="Path to directory in which patching is to take place",
        default=DIRECTORY)
    parser.add_argument(
        '-width',
        help="Data width of init file",
        default=WIDTH)
    parser.add_argument(
        '-depth',
        help="Data depth (number of items in the array)",
        default=DEPTH)
    args = parser.parse_args()
    return args


def get_eff_width(wid):
    if wid <= 1:
        return 1
    elif wid <= 2:
        return 2
    elif wid <= 4:
        return 4
    elif wid <= 8:
        return 8
    elif wid <= 9:
        return 9
    # elif wid <= 16:
    #     return 16
    elif wid <= 18:
        return 18
    # elif wid <= 32:
    #     return 32
    elif wid <= 36:
        return 36
    else:
        return wid


def calculate_tiles_used(eff_wid, depth):
    return int((eff_wid*depth)/(16384*2))


if __name__ == "__main__":
    main()

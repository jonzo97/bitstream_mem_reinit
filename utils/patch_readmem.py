import sys
import os
import fasm
import fasm.output
import utils.parseutil.parse_mdd as mddutil
import utils.parseutil.fasmread as fasmutil
import utils.parseutil.parse_init as initutil

DIRECTORY = 'reconstruction_tests'


def main():
    myargs = parse_args()
    assert myargs.fasm is not None
    assert myargs.init is not None
    assert myargs.mdd is not None
    fasm_to_patch = myargs.fasm
    new_init = myargs.init
    outfile = myargs.outfile
    mdd_fname = myargs.mdd

    fasm_tups = read_fasm(fasm_to_patch)
    cleared_tups = fasmutil.clear_init(fasm_tups)

    mdd_data = mddutil.read_mdd(mdd_fname)
    memfasm = initutil.initfile_to_memfasm(
        infile=new_init,
        fasm_tups=fasm_tups,
        memfasm_name='temp_mem.fasm',
        mdd=mdd_data)
    # memfasm = initutil.initfile_to_memfasm(
    #     infile=new_init,
    #     fasm_tups=fasm_tups,
    #     memfasm_name=f'{DIRECTORY}/mem.fasm',
    #     mdd=mdd_data)

    # merged = merge_tuples(cleared_tups, memfasm)
    # write_fasm(outfile, merged)


def write_fasm(outfile, merged_tups):
    with open(outfile, 'w+') as out:
        out.write(fasm.fasm_tuple_to_string(merged_tups))


def patch_fasm_with_mem(initfile, fasmfile, outfile, width, depth):
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
    all_tups = fasmutil.chain_tuples(cleared_tups, mem_tups)
    merged = fasm.output.merge_and_sort(all_tups)
    return merged


def read_fasm(fname):
    fasm_tuples = fasmutil.get_fasm_tups(fname)
    tiles = fasmutil.get_in_use_tiles(fasm_tuples)
    tiles = fasmutil.get_tile_data(tups=fasm_tuples, in_use=tiles)
    return fasm_tuples


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(
        description='Alter BRAM initialization values')
    parser.add_argument(
        '-fasm',
        help="Fasm to be patched")
    parser.add_argument(
        '-outfile',
        help="Output file")
    parser.add_argument(
        '-init',
        help="New Init memory file used for patching")
    parser.add_argument(
        '-path',
        help="Path to directory in which patching is to take place",
        default=DIRECTORY)
    parser.add_argument(
        '-mdd',
        help="Filename for memory design description file")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()


# def get_eff_width(wid):
#     if wid <= 1:
#         return 1
#     elif wid <= 2:
#         return 2
#     elif wid <= 4:
#         return 4
#     elif wid <= 8:
#         return 8
#     elif wid <= 9:
#         return 9
#     # elif wid <= 16:
#     #     return 16
#     elif wid <= 18:
#         return 18
#     # elif wid <= 32:
#     #     return 32
#     elif wid <= 36:
#         return 36
#     else:
#         return wid


# def calculate_tiles_used(eff_wid, depth):
#     return int((eff_wid*depth)/(16384*2))


# def initdata_to_memfasm(init_data, tileorder, width, depth, write_per_block, memfasm_name):
#     def chunkify_block_data(datastring):
#         datastring = [datastring[x-256:x]
#                       for x in range(len(datastring), 0, -256)]
#         return datastring

#     def blockdata_to_fasmlines(blocks, pblocks=None):
#         fasmlines = []
#         for block, datadict in blocks.items():
#             tile_init = f'{".".join(block.feature.split(".")[0:2])}.INIT_'
#             for addr, initdata in datadict.items():
#                 initdata = f'{tile_init}{addr}[255:0] = 256\'b{initdata}\n'
#                 fasmlines.append(initdata)
#         for block, datadict in pblocks.items():
#             tile_init = f'{".".join(block.feature.split(".")[0:2])}.INITP_'
#             for addr, initdata in datadict.items():
#                 initdata = f'{tile_init}{addr}[255:0] = 256\'b{initdata}\n'
#                 fasmlines.append(initdata)
#                 # print(initdata)
#         return fasmlines

#     blocks = dict()
#     for tile in tileorder:
#         blocks[tile] = ''
#     parity_blocks = dict()
#     eff_width = get_eff_width(width)
#     parity_used = False
#     if eff_width >= 9:
#         parity_used = True

#     for data in init_data:
#         data = data.zfill(eff_width)
#         data = [data[x:x+write_per_block]
#                 for x in range(0, eff_width, 1)]
#         data_per_tile = ['' for x in range(len(tileorder))]
#         for count, blockchunk in enumerate(data):
#             curr_tilenum = count % len(tileorder)
#             data_per_tile[curr_tilenum] = f'{data_per_tile[curr_tilenum]}{blockchunk}'
#         for tile, data in zip(tileorder, data_per_tile):
#             blocks[tile] = f'{data}{blocks[tile]}'
#     if parity_used:
#         for key, datastring in blocks.items():
#             wid = eff_width
#             pdata = ''.join(datastring[x-wid:x-wid+(wid % 8)]
#                             for x in range(len(datastring), 0, -eff_width))
#             # print(len(pdata)/256)
#             # print(f'{int(pdata,2):X}')
#             data = ''.join(datastring[x-wid+(wid % 8):x]
#                            for x in range(len(datastring), 0, -eff_width))
#             # print(len(data)/256)
#             # print(f'{int(data,2):X}')
#             blocks[key] = data
#             parity_blocks[key] = pdata
#         for key, datastring in parity_blocks.items():
#             data = chunkify_block_data(datastring)
#             lines = len(datastring)
#             parity_blocks[key] = dict(zip([f'{x:02X}'
#                                            for x in range(lines)], [substr for substr in data]))
#     for key, datastring in blocks.items():
#         data = chunkify_block_data(datastring)
#         lines = len(datastring)
#         blocks[key] = dict(zip([f'{x:02X}'
#                                 for x in range(lines)], [substr for substr in data]))
#     fasmlines = blockdata_to_fasmlines(blocks=blocks, pblocks=parity_blocks)
#     with open(memfasm_name, 'w') as f:
#         for line in fasmlines:
#             f.write(line)
#     return fasmread.get_fasm_tups(memfasm_name)

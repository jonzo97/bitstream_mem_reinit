import re
import sys

FILE = 'designs/4_by_16k/extracted.mem'
WIDTH = 4
DEPTH = 16384
PERLINE = 64
INIT_FNAME = 'designs/4_by_16k/rebuilt_init.txt'


def main():
    infile, initfile = None, None
    if len(sys.argv) > 1:
        infile = f'designs/{sys.argv[1]}/extracted.mem'
        initfile = f'designs/{sys.argv[1]}/rebuilt_init.txt'
    else:
        infile = FILE
        initfile = INIT_FNAME
    width = int(sys.argv[2]) if len(sys.argv) >= 3 else WIDTH
    depth = int(sys.argv[3]) if len(sys.argv) >= 4 else DEPTH
    perline = int(sys.argv[4]) if len(sys.argv) >= 5 else PERLINE

    print(
        f'infile {infile} initfile {initfile} {width}x{depth}, {perline} per line')

    mem = parse_mem(memfile=infile)
    memarray = memdata_to_array(mem, width=width, depth=depth)
    arrprint(arr=memarray, fname=initfile,
             width=width, depth=depth, perline=perline)
    print(f'Wrote data to {initfile}')


def compile_data(mem):
    all_data = []
    len_block = None
    for data in mem.values():
        len_block = len(data)
        break
    for x in range(len_block):
        for data in mem.values():
            all_data.append(data[x])
    return all_data


def functional_width(width):
    if width <= 2:
        return width
    elif width <= 4:
        return 4
    elif width <= 8:
        return 8
    else:
        return width


def memdata_to_array(mem, width=WIDTH, depth=DEPTH):
    data = compile_data(mem)
    #print(f'data: {data}')
    width = functional_width(width)
    arr = [hex(int(''.join(data[x:x+width])[::-1],2))[2:] for x in range(0, depth*width, width)]
    #for arrdata in arr:
        #print(arrdata)
    return arr


def arrprint(arr, fname=INIT_FNAME, width=WIDTH, depth=DEPTH, perline=PERLINE):
    width = functional_width(width)
    # perline=int(256/width)
    with open(fname, 'w+') as f:
        assert arr is not None
        vals = [arr[x:x+perline] for x in range(0, depth, perline)]
        for val in vals:
            f.write(' '.join(val))
            f.write('\n')


def parse_mem(memfile):
    memline_re = re.compile('^(?:(?P<tileaddr>BRAM_[LR]_X\d+Y\d+)\.(?P<blockaddr>RAMB\d\d_Y\d+)(?: )?)?'
                            '((?P<chunkaddr>(?: INIT_)?[0-9a-fA-F]{2})(?: ))?'
                            '(?:(?P<hex_value>(?:0[xX])?[0-9a-fA-F]*)|'
                            '(?:(?P<bin_value>0[bB])?[01]*))?')
    with open(memfile, 'r') as mem:
        memlines = []
        for line in (l for l in mem if l is not None):
            memlines.append(memline_re.search(line))
    tileaddr, blockaddr = '', ''
    mem = dict()
    for line in memlines:
        assert line is not None
        outline = f''
        if line.group('tileaddr') is not None:
            tileaddr = line.group('tileaddr')
        if line.group('blockaddr') is not None:
            blockaddr = line.group('blockaddr')
        if tileaddr not in mem.keys():
            mem[tileaddr] = dict()
            #print(tileaddr)
        if blockaddr not in mem[tileaddr].keys():
            mem[tileaddr][blockaddr] = dict()
            #print(blockaddr)
        if line.group('hex_value'):
            val = bin(int(line.group('hex_value'), 16))[2:].zfill(256)[::-1]
            mem[tileaddr][blockaddr][line.group('chunkaddr')] = val
        elif line.group('bin_value'):
            #val = line.group('bin_value')[2:].zfill(256)[::-1]
            val = line.group('bin_value').zfill(256)[::-1]
            mem[tileaddr][blockaddr][line.group('chunkaddr')] = val
    tileorder = tile_order(mem)
    sortedmem = dict()
    for tileaddr, blockaddr in tileorder:
        block = mem[tileaddr][blockaddr]
        blockdata = f''
        for data in block.values():
            blockdata += f'{data}'
        sortedmem[(tileaddr, blockaddr)] = blockdata
        #print(blockdata)
    return sortedmem


def tile_order(mem):
    tiles = sorted(mem.keys(), reverse=True)
    for tileaddr in tiles:
        blocks = sorted(mem[tileaddr].keys(), reverse=False)
        for block in blocks:
            yield (tileaddr, block)


if __name__ == '__main__':
    main()


'''
        if line.group('bin_value'):
            val = line.group('bin_value')
            if '0b' in val or '0B' in val:
                val = val[2:]
            val_len = len(val)
            val = f'{val_len}\'b{val}'
            outline = f"{curr_tileaddr}.{curr_blockaddr}.INIT_{line.group('chunkaddr')}[{val_len-1}:0] = {val}"
'''


import utils.parseutil.parse_mdd as mddutil
import utils.parseutil.fasmread as fasmutil
import fasm
# from collections import recordclass


def initfile_to_initlist(infile, mdd):
    width = mddutil.get_width(mdd)
    with open(infile, 'r') as f:
        init_data = []
        for line in f:
            linedata = line.split(' ')
            for data in linedata:
                data = bin(int(data, 16))[2:]
                if width is not None:
                    data = data.zfill(width)
                init_data.append(data)
        return init_data


def initlist_to_edif_celldata(init, fasm_tups, mdd):
    for data in init:
        for cell in mdd:
            # print(data)
            # print(f'{cell.slice_beg}:{cell.slice_end}')
            data_for_cell = data[cell.slice_beg:cell.slice_end+1]
            # print(f'DFC {data_for_cell} ({len(data_for_cell)})')
            # print(f'{cell.pbits}+{cell.dbits}')
            assert len(data_for_cell) == cell.pbits+cell.dbits
            pbits = data_for_cell[0:cell.pbits]
            cell.INITP_LIST.append(pbits)

            dbits = data_for_cell[cell.pbits:]
            cell.INIT_LIST.append(dbits)
            # print(f'{data} -> {data_for_cell}')
            # print(f'{pbits} {dbits}')

            # dbits = data_for_cell[0:cell.dbits+1]
            # pbits = data_for_cell[-cell.pbits:]
            # if cell.pbits > 0:
    for cell in mdd:
        cell.INIT = ''.join(cell.INIT_LIST[::-1])
        if cell.pbits > 0:
            cell.INITP = ''.join(cell.INITP_LIST[::-1])
    return mdd


def convert_placement(tileaddr):
    import re
    xyfind = re.compile(r'X(\d+)Y(\d+)')
    matched_addr = re.match(pattern=xyfind, string=tileaddr)
    assert matched_addr is not None
    x = matched_addr[1]
    y = matched_addr[2]
    # figure my life out here

    tileaddr = f'BRAM_L_X{x}Y{y}'
    return tileaddr


def edif_celldata_to_fasm_initlines(mdd):
    def split_into_lines(bigstr):
        initlines = [''.join(bigstr[x-256:x])
                     for x in range(len(bigstr), 0, -256)]
        return initlines

    tiles = {}
    for cell in mdd:
        y1_init = split_into_lines(cell.INIT[0::2])
        y0_init = split_into_lines(cell.INIT[1::2])
        y1_initp = split_into_lines(cell.INITP[0::2])
        y0_initp = split_into_lines(cell.INITP[1::2])
        tiledata = {'Y0': {'INIT': y0_init, 'INITP': y0_initp},
                    'Y1': {'INIT': y1_init, 'INITP': y1_initp}}
        tileaddr = cell.tile
        # tileaddr = convert_placement(cell.placement)
        # tileaddr = f'BRAM_L_{cell.placement}'
        tiles[tileaddr] = tiledata
    return tiles


def initlines_to_memfasm(initlines, infile_name):
    fasmlines = []
    for tileaddr, tile in initlines.items():
        for yaddr, inits in tile.items():
            for init_type, data in inits.items():
                line_header = f'{tileaddr}.RAMB18_{yaddr}.{init_type}_'
                for count, data in enumerate(data):
                    # if '1' in data:
                        # fasmlines.append(
                        #     f'{line_header}{count:02X}[255:0] = 256\'b{data}')
                    fasmlines.append(
                        f'{line_header}{count:02X}[255:0] = 256\'b{data}')
        #             print(f'{line_header}{count:02X}[255:0] = 256\'b{data}')
        #     print()
        # print()
    with open(f'{infile_name.split(".")[0]}_check.txt', 'w+') as w:
        for line in fasmlines:
            w.write(f'{line}\n')
            # print(line)
    memfasm = (next(fasm.parse_fasm_string(line)) for line in fasmlines)
    # for mf in memfasm:
    # print(type(mf))
    # print(next(fasm.fasm_line_to_string(mf)))
    return memfasm


def initfile_to_memfasm(infile, fasm_tups, memfasm_name, mdd):
    init = initfile_to_initlist(infile, mdd=mdd)
    modified_mdd = initlist_to_edif_celldata(
        init=init, fasm_tups=fasm_tups, mdd=mdd)
    initlines = edif_celldata_to_fasm_initlines(mdd=modified_mdd)
    initlines_to_memfasm(initlines, infile)
    return f''
    # width = mddutil.get_width(mdd)
    # initlist = initfile_to_initlist(infile, width)
    # writesdict = initlist_to_writesdict(
    #     init=initlist, fasm_tups=fasm_tups, mdd=mdd)
    # # init=initlist, fasm_tups=fasm_tups, width=width)
    # initstr = writesdict_to_initstr(writesdict)
    # initlines = initstr_to_initlines(initstr)
    # memfasm = initlines_to_memfasm(initlines)
    # with open(memfasm_name, 'w') as f:
    #     for line in memfasm:
    #         f.write(line)
    #         f.write('\n')
    # return fasmutil.get_fasm_tups(memfasm_name)


#   writesdict = {}
    #    for ramb18 in wid_dict.keys():
    #         writesdict[ramb18] = {'INIT': [], 'INITP': []}
    #     for data in init:
    #         tilecount = len(wid_dict)
    #         for count, (key, wid) in enumerate(wid_dict.items()):
    #             tiledata = [data[x]
    #                         for x in range(count, len(data), tilecount)]
    #             if wid_dict[key] > 8:
    #                 initp_len = wid_dict[key] % 8
    #                 writesdict[key]['INITP'].append(
    #                     ''.join(tiledata[0:initp_len]))
    #                 writesdict[key]['INIT'].append(
    #                     ''.join(tiledata[initp_len:]))
    #             else:
    #                 writesdict[key]['INIT'].append(''.join(tiledata))
    #     return writesdict

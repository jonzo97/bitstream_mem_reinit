

import os

biggest_width = 64
target_size = 1024*16
enable_parity_widths = True

fasm_name = 'patched.fasm'
extracted_init_name = 'init_frm_reinit.txt'
extracted_memfile_name = 'mem_frm_reinit.mem'
fasmchange = '../meminit/fasmchange.py -extract_mem'


designs = [
    (1, '16k'),
    (2, '8k'),
    (4, '4k'),
    (8, '2k'),
    (9, '2k'),
    (16, '1k'),
    (18, '1k'),
    (32, '512'),
    (36, '512'),
]


'python3 ../meminit/fasmchange.py -extract_mem -infile temp/top.fasm -outfile $OUTFILE'

for design in designs:
    width, depth = design[0], design[1]
    #dir_name = f'~/bigmems/designs/{width}_by_{depth}'
    dir_name = f'designs/{width}_by_{depth}'
    fasm_path = f'{dir_name}/{fasm_name}'
    extr_memfile_path = f'{dir_name}/mem/{extracted_init_name}'

    command = f'python3 {fasmchange} -infile {fasm_path} -outfile {extr_memfile_path}'
    os.system(command)

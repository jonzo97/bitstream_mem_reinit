import os
init = 'init.txt'
designs = [
    (1, '32k'),
    (2, '16k'),
    (4, '8k'),
    (8, '4k'),
    (9, '4k'),
    (16, '2k'),
    (18, '2k'),
    (32, '1k'),
    (36, '1k'),
]

for design in designs:
    width, depth = design[0], design[1]

    command = f'bash gen_scripts/patchmem_control.sh {width} {depth} {init}'
    os.system(command)

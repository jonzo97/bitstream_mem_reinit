import os
designs = [
    (1, '32k', 1),
    (2, '16k', 1),
    (4, '8k', 'a'),
    (8, '4k', 'f0'),
    (9, '4k', '1f0'),
    (16, '2k', 'f000'),
    (18, '2k', '3f000'),
    (32, '1k', 'f0000000'),
    (36, '1k', 'af0000000'),
]

for design in designs:
    width, depth, data = design[0], design[1], design[2]

    command = f'bash gen_scripts/do_everything.sh {width} {depth} {data}'
    os.system(command)

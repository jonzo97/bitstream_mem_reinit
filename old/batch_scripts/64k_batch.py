import os
designs = [
    (1, '64k', '1'),
    (2, '32k', '1'),
    (4, '16k', 'a'),
    (8, '8k', 'f0'),
    (9, '8k', '1f0'),
    (16, '4k', 'f000'),
    (18, '4k', '3f000'),
    (32, '2k', 'f0000000'),
    (36, '2k', 'af0000000'),
]

# for design in designs:
#     width, depth, data = design[0], design[1], design[2]

#     command = f'bash gen_scripts/do_everything.sh {width} {depth} {data}'
#     os.system(command)


for design in designs:
    width, depth, data = design[0], design[1], design[2]

    command = f'bash gen_scripts/init_maker.sh {width} {depth} {data} altinit.txt'
    os.system(command)

# for design in designs:
#     width, depth, data = design[0], design[1], design[2]

#     command = f'bash gen_scripts/gen_and_extract.sh {width} {depth} altinit altextracted'
#     os.system(command)

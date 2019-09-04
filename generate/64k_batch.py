import os
import subprocess
designs = [
    (1,     '64k',  2048*32,    256,    '1'),
    (2,     '32k',  2048*16,    128,    '1'),
    (4,     '16k',  2048*8,     64,    'a'),
    (8,     '8k',   2048*4,     32,    'f0'),
    (9,     '8k',   2048*4,     32,    '1f0'),
    (16,    '4k',   2048*2,     16,    'f000'),
    (18,    '4k',   2048*2,     16,    '3f000'),
    (32,    '2k',   2048*1,     8,    'f0000000'),
    (36,    '2k',   2048*1,     4,    'af0000000'),
]

BATCHDIR = '64k'
SUBTITLE = ''

for design in designs:
    width, depthname, depth, perline, data = design[0], design[1], design[2], design[3], design[4]

    command = f'./generate/do_everything.sh {BATCHDIR} {width} {depthname} {depth} {perline} {SUBTITLE}'
    os.system(command)

    # source_command = f'generate/do_everything.sh {BATCHDIR} {width} {depthname} {depth} {perline} {SUBTITLE}'
    # subprocess.Popen(["/bin/sh", "~/bigmems/generate/do_everything.sh",
    #                   f'{BATCHDIR}', f'{width}', f'{depthname}', f'{depth}', f'{perline}', f'{SUBTITLE}'])


# for design in designs:
#     width, depth, data = design[0], design[1], design[2]

#     command = f'bash gen_scripts/init_maker.sh {width} {depth} {data} altinit.txt'
#     os.system(command)

# for design in designs:
#     width, depth, data = design[0], design[1], design[2]

#     command = f'bash gen_scripts/gen_and_extract.sh {width} {depth} altinit altextracted'
#     os.system(command)

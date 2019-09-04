import os
WIDTH = '18'
WID = 16
DEPTHNAME = '4k'
DPTH = 4096
PTRN_LEN = 4
DEPTH = str(int(DPTH/PTRN_LEN))
PERLINE = f'{int(256/(PTRN_LEN*WID))}'
print(PERLINE)

# data = [
#     '"3f000 0f000 0f000 0f000"',
#     '"0f000 3f000 0f000 0f000"',
#     '"0f000 0f000 3f000 0f000"',
#     '"0f000 0f000 0f000 3f000"',
# ]
# fnames = [
#     '3000',
#     '0300',
#     '0030',
#     '0003',
# ]

data = [
    '\"2f000 0f000 0f000 0f000\"',
    '\"1f000 3f000 0f000 0f000\"',
]
fnames = [
    '2f000',
    '1f000',
]


# pimm = [
#     [WIDTH, DEPTHNAME, DEPTH, '3f000 0f000 0f000 0f000', '3000.txt', PERLINE],
#     [WIDTH, DEPTHNAME, DEPTH, '0f000 3f000 0f000 0f000', '3000.txt', PERLINE],
#     [WIDTH, DEPTHNAME, DEPTH, '0f000 0f000 3f000 0f000', '3000.txt', PERLINE],
#     [WIDTH, DEPTHNAME, DEPTH, '0f000 0f000 0f000 3f000', '3000.txt', PERLINE],
# ]

pimm = [[WIDTH, DEPTHNAME, DEPTH, d,
         f, PERLINE] for d, f in zip(data, fnames)]
gae = [[WIDTH, DEPTHNAME, f] for f in fnames]


for args in pimm:
    command = f'bash gen_scripts/pattern_init_maker.sh {" ".join(args)}'
    os.system(command)

for args in gae:
    command = f'bash gen_scripts/gen_and_extract.sh {" ".join(args)}'
    os.system(command)

memfiles = [
    '1_by_16k',
    '1_by_32k',
    '1_by_64k',
    '2_by_8k',
    '2_by_16k',
    '2_by_32k',
    '2_by_64k',
    '4_by_8k',
    '4_by_16k',
    '4_by_32k',
    '8_by_8k',
    '8_by_16k',
    '16_by_8k',
    '16_by_16k'
]

for mf in memfiles:
    with open(f'designs/{mf}/extracted.mem', 'r') as inf, open(f'designs/{mf}/readable.mem', 'w+') as outf:
        for line in inf:
            print(line)
            line = line.split(' ')
            if len(line) >= 2:
                line[1] = line[1].replace('0', '_')
                outf.write(' '.join(line[0:2]))
            else:
                outf.write(' '.join(line))

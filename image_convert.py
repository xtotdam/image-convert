import sys
import imageio
from random import shuffle, choices
from textwrap import wrap
from math import sqrt
from itertools import product
from functools import partial
from pprint import pprint
from collections import Counter
import argparse


# https://gist.github.com/TerrorBite/e738e25881d4aecf9043
# https://gist.github.com/MicahElliott/719710
# Default color levels for the color cube
cubelevels = [0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff]
# Generate a list of midpoints of the above list
snaps = [(x+y)/2 for x, y in list(zip(cubelevels, [0]+cubelevels))[1:]]

def rgb2short(r, g, b):
    """ Converts RGB values to the nearest equivalent xterm-256 color."""
    # Using list of snap points, convert RGB value to cube indexes
    r, g, b = map(lambda x: len(tuple(s for s in snaps if s<x)), (r, g, b))
    # Simple colorcube transform
    return r*36 + g*6 + b + 16


parser = argparse.ArgumentParser(description='Convert image to pixelated C code')
parser.add_argument('image_file', metavar='image')
parser.add_argument('-r', '--rounds', type=int, default=13,
    help='Number of compression rounds')
parser.add_argument('-w', '--linewrap', type=int, default=80,
    help='Final text width')
parser.add_argument('-f', '--function', type=str, default='main',
    help='Name of function')
parser.add_argument('-o', '--outfile', type=str, default='test.c',
    help='Name of output file')
parser.add_argument('-s', '--shuffle', action='store_const', const=True, default=False,
    help='Shuffle letters or not')
args = parser.parse_args()
print(args)

# SETTINGS
linewrap_width = args.linewrap
comments = [
    (' // <--', 0.05),
    (' // magic', 0.03),
    (' // barrier cut-off', 0.01),
    ('', 1.)
]
shuffle_letters = args.shuffle
function_name = args.function
output_c_name = args.outfile
compress_rounds = args.rounds

im = imageio.imread(args.image_file)
# im = imageio.imread('pixel-link.png')

l2 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = list()
for x in range(1, 3+1):
    letters += list(''.join(s) for s in product(l2, repeat=x))
if shuffle_letters:
    shuffle(letters)


defines = dict()
markers = {
    'start': letters.pop(0),
    'end': letters.pop(0),
    'none': letters.pop(0),
    'eol': letters.pop(0)
}

defines[markers['start']] = '"[48;5;"'
defines[markers['end']] = '"m  [0m"'
defines[markers['none']] = '"  "'
defines[markers['eol']] = '"\\n"'

colors = set()
listoflines = list()
for line in im:
    lineinlist = list()
    for el in line:
        if len(el) == 4: # RGBA
            if el[-1] == 0: # transparent pixel
                lineinlist.append(None)
            else:
                color = rgb2short(*el[:-1])
                colors.add(color)
                lineinlist.append(color)
        else: #RGB
            color = rgb2short(*el)
            colors.add(color)
            lineinlist.append(color)
    lineforfinal = ' '.join(
        f'{markers["start"]}"{x}"{markers["end"]}' if x else markers['none'] for x in lineinlist)
    listoflines.append(lineforfinal)
final = f' {markers["eol"]} '.join(listoflines) + f' {markers["eol"]}'

print('*', len(colors), 'colors in the image')

for c in colors:
    l = letters.pop(0)
    final = final.replace(f'"{c}"', f' {l} ')
    defines[l] = f'"{c}"'

final = final.strip().split()
print('* Picture string', len(final))

for roundd in range(compress_rounds):
    pairs = list(zip(final[:-1], final[1:]))
    triples = list(zip(final[:-2], final[1:-1], final[2:]))
    quadres = list(zip(final[:-3], final[1:-2], final[2:-1], final[3:]))
    p = ' '.join(Counter(pairs).most_common(1)[0][0])
    t = ' '.join(Counter(triples).most_common(1)[0][0])
    q = ' '.join(Counter(quadres).most_common(1)[0][0])
    # print(p, t, q)

    final = ' '.join(final)

    l = letters.pop(0)
    fp = final.replace(f' {p} ', f' {l} ')
    ft = final.replace(f' {t} ', f' {l} ')
    fq = final.replace(f' {q} ', f' {l} ')
    lens = [len(fp), len(ft), len(fq)]
    i = lens.index(min(lens))

    # i = choices([0,1,2], k=1)[0]

    if i == 0:
        defines[l] = p
        final = fp
    elif i == 1:
        defines[l] = t
        final = ft
    else:
        defines[l] = q
        final = fq

    final = final.split()

    print('* Compress round', roundd+1, len(final))

print('* Last letter used:', l)

final = ' '.join(final)
defines = '\n'.join(
    f"#define {k} {v}" for (k,v) in defines.items()
)



# WRAPPING
lines = wrap(final, linewrap_width)
for i in range(len(lines)):
    c = choices([x[0] for x in comments], [x[1] for x in comments])
    lines[i] += c[0]
final = '\n'.join(lines)

final = final.strip()
print('Final string', len(final))

# OUTPUT
with open(output_c_name, 'w') as f:
    f.write(f'''#include <stdio.h>

{defines}

void {function_name}(void) {{ printf(
{final}
);}}''')

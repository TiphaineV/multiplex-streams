import sys

'''
def configure(paths=['../multiplex-streams/src', '../sgvis/src']):
    for p in paths:
        if p not in sys.path: sys.path.append(p)

configure()
'''

import os
import tempfile

def drawMS(ms, name='output', colors='byLayer', show=False, ordonne=False):
    dir = 'outputs'
    figfile = f'{dir}/{name}.fig'
    with open(os.devnull, 'w') as devnull:
        stdout = sys.stdout; sys.stdout = devnull
        ms.drawMS(figfile, colors=colors, neglect=-1, ordonne=ordonne, colL={})
        sys.stdout = stdout

    os.system(f'fig2dev -Lpng {figfile} {dir}/{name}.png')
    os.system(f'fig2dev -Lpdf {figfile} {dir}/{name}.pdf')
    
    from IPython.display import display, Image, FileLink
    if show:
        png = f'{dir}/{name}.png'
        display(Image(png))
        display(FileLink(png))

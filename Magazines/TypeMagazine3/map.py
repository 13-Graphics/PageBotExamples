#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     map.py
#
from pagebot.elements import Page
from pagebot.publications.magazine import Magazine
from pagebot.publications.magazine.parts import *
from metrics import *

elements =(
    Front(1),
    Ad(2),
    Ad(1),
)
coverFront = CoverFront(elements=elements)

elements = (
    TableOfContent(1),
    MastHead(1),
    Ad(1),
    Dummy(12),
)
frontOfTheBook = FrontOfTheBook(elements=elements)

elements = (
    Article(2, name='Roger'),
    Ad(1, name='Ad DDS?'),
    Article(2, name='One More JB'),
)
backOfTheBook = BackOfTheBook(elements=elements)

elements = (
    Ad(1),
    Ad(1, name='Backcover Ad')
)
coverBack = CoverBack(elements=elements)

elements = [
    coverFront,
    frontOfTheBook,
    Article(12, name='Gerrit Noordzij', thumbPath='_export/P20-P31-Type3-GerritNoordzij_%d.png'),
    Article(8, name='Parametric PageBot'),
    Article(10, name='Variables'),
    Article(12, name='Historical Futurism'),
    Article(12, name='Firsts', thumbPath='_export/P58-P73-Type3-Firsts_%d.png'),
    Article(22, name='People', thumbPath='_export/P74-P95-Type3-PeopleInType_%d.png'),
    backOfTheBook,
    coverBack,
]
class TypeMagazine(Magazine):
    u"""    

    >>> m = TypeMagazine(w=W, h=H, elements=elements, name='Type Magazine 3')
    >>> m.baselineGrid = BASELINE
    >>> m.baselineGridStart = BASELINE_START
    >>> m.gw = m.gh = GUTTER
    >>> m.cw = CW
    >>> m.padding = PADDING_LEFT
    >>> m.gridX = GRIDX
    >>> len(m)
    102
    >>> spreads = m.spreads
    >>> len(spreads)
    52
    >>> m.exportMap(cols=1, maxSpread=28, showGrid=True, showPadding=True)
    """

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
else:
    magazine = TypeMagazine(w=W, h=H, elements=elements, name='Type Magazine 3')
    magazine.baselineGrid = BASELINE
    magazine.baselineGridStart = BASELINE_START
    magazine.gw = magazine.gh = GUTTER
    magazine.cw = CW
    magazine.padding = PADDING_LEFT
    magazine.gridX = GRIDX


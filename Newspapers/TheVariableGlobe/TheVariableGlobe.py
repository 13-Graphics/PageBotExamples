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
# =============================================================================
#
#     TheVariableGlobe.py
#
from copy import copy

from pagebot.contexts.platform import getContext
# Blob random text for contenxt.
from pagebot.contributions.filibuster.blurb import Blurb
# Import the generic Document class. There is also specialized Publication classes 
# inheriting from Document, but for educational purpose, we'll use the generic class.
from pagebot.document import Document 
# Get constants needed for this Newspaper page.
from pagebot.constants import Broadsheet, GRID_SQR, BASE_LINE, BASE_INDEX_RIGHT, CENTER, LEFT
from pagebot.conditions import *
# Import the measure units that we need
from pagebot.toolbox.units import inch, pt, mm
# Import color stuff
from pagebot.toolbox.color import blackColor
from pagebot.elements import * # Import all types of page elemenents that we may need.
from pagebot.fonttoolbox.objects.font import findFont, getInstance

context = getContext()
# Random text generator
blurb = Blurb()

# =============================================================================
#    Measures
# .............................................................................
#W, H = Broadsheet # Split paper size in document width and height
W, H = mm(819, 1176) # Dutch Volskrant tabloid size.

U = pt(10)
G = 3*U
PL = 8*U # Page padding left
PR = 10.5*U
PT = 7*U # Page padding top
PB = 10*U # Page badding bottom
PADDING = PT, PR, PB, PL

# Grid definitions
CC = 5 # Column count
CW = (W-PL-PR+G)/CC-G # Column width (without gutter)
CW2 = 2*CW + G
CW3 = 3*CW + 2*G
CW4 = 4*CW + 3*G
CW5 = 5*CW + 4*G

RC = 8 # Row count
RH = (H-PT-PB+G)/RC-G # Row height (without gutter)

gridX = [] # Create the column grid
for colIndex in range(CC):
    gridX.append((CW, G))
gridY = [] # Create the row grid
for rowIndex in range(RC):
    gridY.append((RH, G))

# =============================================================================
#    Text content 
#    For this example defined as strings. Should from from MarkDown file instead.
# .............................................................................

TITLE = 'The Variable Globe'

# =============================================================================
#    Fonts and Variable instances.
# .............................................................................

bodyFont = findFont('RobotoDelta-VF')
#print(bodyFont.axes) # Uncomment to see axes and values for this VF
location = dict(wght=700)
boldFont = bodyFont.getInstance(location)
headFont = findFont('AmstelvarAlpha-VF')
#print(headFont.axes) # Uncomment to see axes and values for this VF
# Create bold/title font as Variable location
location = dict(wght=700, XTRA=260)
kerning = {('V','a'): -100}
headBoldFont = titleFont = headFont.getInstance(location, kerning=kerning)
# Install the fonts (there is a bug in either DrawBot or PageBot)
# Showing 
# *** DrawBot warning: font: 'AmstelvarAlpha-Default--XTRA260-wght700' 
# is not installed, back to the fallback font: 'Verdana' ***
# *** DrawBot warning: font: 'RobotoDelta-Regular' is not installed, 
# back to the fallback font: 'Verdana' ***
print(context.installFont(bodyFont))
print(context.installFont(headFont))
print(context.installFont(headBoldFont))

print('Variable axes for headFont: ', headFont.axes)
print('Variable axes for titleFont: ', titleFont.axes) # Single instance not longer has axes

# =============================================================================
#    Styles (comparable to InDesign paragraph and character styles)
# .............................................................................

# Define types of border below text boxes 
border = dict(strokeWidth=pt(1), stroke=blackColor)

# Create the styles
topHeadStyle = dict(font=bodyFont, fontSize=pt(48), xTextAlign=LEFT)
topHeadBoldStyle = copy(topHeadStyle)
topHeadBoldStyle['font'] = titleFont
titleStyle = dict(font=titleFont, fontSize=pt(100), xTextAlign=CENTER)
# Textline under the newspaper title
subTitleStyle = dict(font=bodyFont, fontSize=pt(12), xTextAlign=LEFT)
# Article headline
headline1Style = dict(font=headFont, fontSize=pt(60), textFill=0, xTextAlign=CENTER)
mainStyle = dict(font=bodyFont, fontSize=pt(16), textFill=0)

# =============================================================================
#    Create the document and define the viewing parameters
# .............................................................................
doc = Document(w=W, h=H, originTop=False, gridX=gridX, gridY=gridY, autoPages=1)
# Set the viewing parameters
view = doc.view
view.padding = inch(1)
view.showCropMarks = True
view.showRegistrationMarks = True
view.showNameInfo = True
view.showGrid = True # Defaults to showing GRID_
#view.showBaselines = [BASE_LINE, BASE_INDEX_RIGHT]
view.showFrame = True
view.showPadding = True

# =============================================================================
#    Get the first (and only) page from the doc
# .............................................................................

page = doc[1]
page.padding = PADDING # Set 4 padding values all at once.

# =============================================================================
#    Add background image from existing newspaper.
#    And overlay transparant gray layer to see template as shaded    
# .............................................................................

# Put them on z-position != 0, to avoid the condition floating hooking on them.
# E.g. Float2Top() layout conditions only look at elements with the same z-value.
newImage('2018-09-04_De_Volkskrant_-_04-09-2018.pdf', w=W, h=H, z=-10, parent=page)
newRect(fill=(1, 1, 1, 0.5), w=W, h=H, z=-10, parent=page)

# =============================================================================
#    Top-left headline above newspaper title. Bold name with designer quote
# .............................................................................

tx = blurb.getBlurb('name')
bs = context.newString(tx+': ', style=topHeadBoldStyle)
tx = blurb.getBlurb('design_theory').capitalize()
if not tx.endswith('.'):
    tx += '.'
bs += context.newString('“'+tx+'”', style=topHeadStyle)
tw, th = context.textSize(bs, w=CW3)
tx = ' P%d' % choice(range(80))
bs += context.newString(tx+': ', style=topHeadBoldStyle)
paddingTop = inch(1)
newTextBox(bs, parent=page, h=th+paddingTop, pt=paddingTop,
    conditions=(Left2Left(), Fit2ColSpan(colSpan=3), Float2Top()))


# Title of the newspaper
bs = context.newString(TITLE, style=titleStyle, w=page.pw)
tw, th = bs.size
print('Calculated fitting title size: ', bs.fittingFontSize)
newTextBox(bs, parent=page, h=th, borderBottom=border, 
    conditions=(Left2Left(), Fit2Width(), Float2Top()))
# Title subline of the newspaper
bs = context.newString('Aaaa ' * 30, style=subTitleStyle)
tw, th = bs.size
newTextBox(bs, parent=page, h=th*2, borderBottom=border, pt=th/2,
    conditions=(Left2Left(), Fit2Width(), Float2Top()))
'''
if 1:
    # Main article as group of 3 text boxes
    main1 = newRect(parent=page, w=CW4, mt=G, fill=0.8, conditions=(Left2Left(), Float2Top()))

    bs = context.newString('Headline main 1', style=headline1Style)
    tw, th = bs.size
    newTextBox(bs, name='head1', parent=main1, conditions=(Left2Left(), Fit2Width(), Float2Top()))

    bs = context.newString('Aaaa ' * 120, style=mainStyle)
    newTextBox(bs, name='main11', h=400, w=CW2, parent=main1, fill=0.8, mt=3*G,
        conditions=(Left2Left(), Float2Top()))
    bs = context.newString('Aaaa ' * 120, style=mainStyle)
    newTextBox(bs, name='main12', h=400, w=CW2, parent=main1, fill=0.8, mt=3*G, 
        conditions=(Right2Right(), Float2Top()))

if 1:
    # Main article as group of 3 text boxes
    main2 = newRect(parent=page, w=CW4, mt=G, fill=0.8, conditions=(Left2Left(), Float2Top()))

    bs = context.newString('Headline main 2', style=headline1Style)
    tw, th = bs.size
    newTextBox(bs, name='head2', parent=main2, conditions=(Left2Left(), Fit2Width(), Float2Top()))

    bs = context.newString('Aaaa ' * 120, style=mainStyle)
    newTextBox(bs, name='main21', h=400, w=CW2, parent=main2, fill=0.8, mt=3*G,
        conditions=(Left2Left(), Float2Top()))
    bs = context.newString('Aaaa ' * 120, style=mainStyle)
    newTextBox(bs, name='main22', h=400, w=CW2, parent=main2, fill=0.8, mt=3*G, 
        conditions=(Right2Right(), Float2Top()))

'''
doc.solve() # Drill down to solve all elements conditions.
doc.export('_export/TheVariableGlobe.pdf')

context.unInstallFont(bodyFont)
context.unInstallFont(headFont)
context.unInstallFont(boldFont)


# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     BertholdTypeSpecimen.py
#
#     This scripts generates a look-alike revival type specimen with an interpretation
#     of the classic Berthold specimen pages.
#     Special challenge is to use the capital-size system of Berthold in mm and 
#     the calculation of real values for the table and drawing the rulers.
#
#     For educational purpose in using PageBot, almost every line of code has been commented.
#

import os # Import standard libary for accessing the file system.
from random import choice, shuffle # Used for random selection of sample words

from pagebot.contexts import getContext # Decide if running in DrawBot or Linux-Flat
from pagebot.constants import CENTER, INLINE # Import some measure and alignments constants.
from pagebot.document import Document # Overall container class of any PageBot script
from pagebot.fonttoolbox.objects.font import findFont # Access to installed fonts
from pagebot.elements import newRect, newTextBox, newImage # Used elements in this specimen
from pagebot.conditions import * # Import layout conditions for automatic layout.
from pagebot.contributions.filibuster.blurb import Blurb

from pagebot.toolbox.transformer import path2FontName # Convenient CSS color to PageBot color conversion
from pagebot.toolbox.hyphenation import wordsByLength # Use English hyphenation dictionary as word selector
from pagebot.toolbox.units import inch, pt, em
from pagebot.toolbox.color import color

context = getContext()

SHOW_GRID = True
SHOW_TEMPLATE = True
SHOW_FRAMES = True

sampleFont = findFont('Upgrade-Regular')
 
blurb = Blurb()
    
# Basic page metrics.
U = pt(8) # Page layout units, to unite baseline grid and gutter.
W, H = pt(590, 842) # Copy size from original Berthold specimen scan.
# Hard coded padding sizes derived from the scan.
PT, PR, PB, PL = PADDING = pt(36, 34, 75, 70) # Page padding top, right, bottom, left
L = 2*U # Baseline leading
G = 3*U # Default gutter = space between the columns

# Hard coded column sizes derived from the scan.
C1, C2, C3 = (112, 300, 112)
# Construct the grid pattern. 
# Last value None means that there is no gutter running inside the right padding.
GRID_X = ((C1, G), (C2, G), (C3, G))
GRID_Y = ((H - PT - PB, G),)

# Classic Berthold type specimen
# Path to the scan, used to show at first page of this document.
BERTHOLD_PATH = 'resources/BertholdBodoniOldFace#152.pdf'

labelStyle = dict(font=sampleFont, fontSize=7, leading=em(1), paragraphTopSpacing=4, paragraphBottomSpacing=-10)

# Sample glyphs set in bottom right frame. Automatic add a spacing between all characters.
GLYPH_SET = ' '.join(u'ABCDEFGHIJKLMNOPQRSTUVWXYZ&$1234567890abcdefghijklmnopqrstuvwxyz.,-‘:;!?')

# Export in _export folder that does not commit in Git. Force to export PDF.
DO_OPEN = False
if SHOW_GRID:
    EXPORT_PATH_PDF = '_export/Berthold-Grid.pdf' 
    EXPORT_PATH_PNG = '_export/Berthold-Grid.png' 
else:
    EXPORT_PATH_PDF = '_export/Berthold-%s.pdf' % FAMILIES[0].name 
    EXPORT_PATH_PNG = '_export/Berthold-%s.png' % FAMILIES[0].name 

MAX_PAGES = 5

# Some parameters from the original book
PAPER_COLOR = color(rgb=0xFEFEF0) # Approximation of paper color of original specimen.
RED_COLOR = color(rgb=0xAC1E2B) # Red color used in the original specimen

# Get the dictionary of English ("en" is default language), other choice is Dutch ("nl").
# Danish could be made available for PageBot if requested.
# Other hyphenation tables are appreciated to be added to PageBot.
# WORDS key is the word length in character count and the values are lists words of
# equal amount of characters.
# In case there are no words available for a given length, longer words will be clipped.
LANGUAGE = 'nl' #'en'
WORDS = wordsByLength(LANGUAGE)
SHORT_WORDS = WORDS[3]+WORDS[4]+WORDS[3]+WORDS[4]+WORDS[3]+WORDS[4]+WORDS[5]+WORDS[6]
shuffle(SHORT_WORDS)

def getCapitalizedWord(l):
    u"""Select a random word from the hyphenation dictionary for this language."""
    if not l in WORDS and l < 100: # If the length does not exist, try larger
        return getCapitalizedWord(l+1)[:-1]
    return choice(WORDS[l]).capitalize()

def getCapWord(l):
    return getCapitalizedWord(l).upper()
    
def getShortWordText():
    u"""Answer all words of 3, 4, 5, 6 and shuffle them in a list."""
    shortWords = ' '.join(SHORT_WORDS[:40])
    shuffle(SHORT_WORDS)
    return shortWords.lower().capitalize()
    
def buildSpecimenPages(doc, family, pn):
    """Build the specimen for the family, one page per style."""
    for font in family.getFonts():
        pn = buildSpecimenPage(doc, family, font, pn)
        if pn >= MAX_PAGES:
            break
    return pn
   
       
def makeDocument(font):
    u"""Create the main document in the defined size with a couple of automatic empty pages."""

    # Build 4 pages, two for the original scan, the two for the generated version.
    doc = Document(w=W, h=H, title='Variable Font Sample Page', originTop=False, 
        autoPages=4, context=context, gridX=GRID_X, gridY=GRID_Y)
    
    # Get default view from the document and set the viewing parameters.
    view = doc.view
    view.padding = 0 # For showing cropmarks and such, make > mm(20) or inch(1).
    view.showPageCropMarks = True # Won't show if there is not padding in the view.
    view.showPageFrame = SHOW_FRAMES # No frame in case PAPER_COLOR exists to be shown.
    view.showPagePadding = SHOW_FRAMES # No frame in case PAPER_COLOR exists to be shown.
    view.showPageRegistrationMarks = True
    view.showGrid = SHOW_GRID # Show GRID_X lines
    view.showPageNameInfo = True # Show file name and date of the document
    view.showTextOverflowMarker = False # Don't show marker in case Filibuster blurb is too long.

    for pn in range(1, 3):
        page = doc[pn]
        page.ch = 0 # No vertical grid
        page.padding = PADDING
        page.gridX = GRID_X
        newRect(parent=page, fill=PAPER_COLOR, conditions=[Fit()])
        newImage(BERTHOLD_PATH, x=0, y=0, w=W, index=pn, parent=page)

    page = doc[3]
    page.ch = 0 # No vertical grid
    page.padding = PADDING
    page.gridX = GRID_X
    newRect(parent=page, fill=PAPER_COLOR, conditions=[Fit()])
    # During development, draw the template scan as background
    # Set z-azis != 0, to make floating elements not get stuck at the background
    if SHOW_TEMPLATE:
        newImage(BERTHOLD_PATH, x=0, y=0, z=-10, w=W, index=1, parent=page)

    page = doc[4]
    page.ch = 0 # No vertical grid
    page.padding = PADDING
    page.gridX = GRID_X
    newRect(parent=page, fill=PAPER_COLOR, conditions=[Fit()])
    # During development, draw the template scan as background
    # Set z-azis != 0, to make floating elements not get stuck at the background
    if SHOW_TEMPLATE:
        newImage(BERTHOLD_PATH, x=0, y=0, z=-10, w=W, index=1, parent=page)

    doc.solve()
    
    return doc

doc = makeDocument(sampleFont)
doc.export(EXPORT_PATH_PDF) 
#doc.export(EXPORT_PATH_PNG) 
if DO_OPEN:
    os.system(u'open "%s"' % EXPORT_PATH)
  
print('Done')

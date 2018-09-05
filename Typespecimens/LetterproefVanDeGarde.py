# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
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
#     NEEDS TO BE FIXED
#
#     LetterproefVanDeGarde.py
#
#     This scripts generates a look-alike revival type specimen with an interpretation
#     of the "Letterproef Van De Garde" Monotype letterpress type specimen, dated 1967.
#     The full name of the printer is "Koninklijke Drukkerij Van de Garde Zaltbommel"
#     Instead of the range of type faces the printer had, a selection of system fonts
#     is shown instead. If you want to use your own typefaces to show up, there is a little
#     coding exercise. 
#
#     As NL-based hot-metal, the measures in the origal book are augustin, but the layout
#     measures often seem to be whole measures of centimeters.
#     For convenience of calculation augustins are treated as points (font size, etc.)
#     and the other measures are calculated as multiplication factor of MM
#
#     This script is intentionally structures as a linear building of pages, without the
#     use of page functions or templates, in order to illustrate the sequentials building
#     of the content. 
#     As real application it would be more generic to add a second layer of abstractions,
#     that defines the types of pages as templates and uses parameter values and data
#     to make insert the content in the template elements.
#
import copy
from pagebot.contexts.platform import getContext
context = getContext()

import pagebot # Import to know the path of non-Python resources.
from pagebot.contributions.filibuster.blurb import Blurb
from pagebot.fonttoolbox.objects.font import findFont

from pagebot.style import CENTER, TOP, BOTTOM, MIDDLE, INLINE, ONLINE, OUTLINE, RIGHT, LEFT
# Document is the main instance holding all information about the document together (pages, views, etc.)
from pagebot.document import Document
# Import all element classes that can be placed on a page.
from pagebot.elements import *
# Import all layout condition classes
from pagebot.conditions import *
# Import colors and units
from pagebot.toolbox.color import color, noColor
from pagebot.toolbox.units import mm, pt, em
# Generic function to create new FormattedString, extended version of DrawBot FormattedString() call.

W, H, = PageWidth, PageHeight = mm(180), mm(247) # Original size of Letterproef (type specimen)
PADDING = PageWidth/18 # Padding based on size (= in book layout called margin) of the page.
PT = mm(22)
PB = mm(36)
PL = PR = mm(16) # Although the various types of specimen page have their own margin, this it the overall page padding.
pagePadding = (PT, PR, PB, PL)
G = pt(12) # Gutter
#SYSTEM_FAMILY_NAMES = ('Verdana',)
#SYSTEM_FAMILY_NAMES = ('Georgia',)
#FONT_NAME_PATTERNS = ('Bungee', 'Amstel', 'Deco') # TODO, make this work if fonts don't exist.
#SYSTEM_FAMILY_NAMES = ('Proforma', 'Productus')
#MY_FAMILY_NAMES = ('Proforma', 'Productus')
FONT_NAME_PATTERNS = ('Proforma')
#FONT_NAME_PATTERNS = ('Productus')
#FONT_NAME_PATTERNS = ('Bitcount',)
#FONT_NAME_PATTERNS = ('Upgrade',)

# Export in _export folder that does not commit in Git. Force to export PDF.
EXPORT_PATH_PNG = '_export/LetterproefVanDeGarde.png' 
EXPORT_PATH_PDF = '_export/LetterproefVanDeGarde.pdf' 
COVER_IMAGE_PATH = 'images/VanDeGardeOriginalCover.png'

def findTheFont(styleNames, italic=False):
    u"""Find available fonts and guess closest styles for regular, medium and bold."""
    # Any TypeNetwork TYPETR Productus or Proforma installed in the system?
    # Some hard wired foundry name here. This could be improved. Maybe we can add a public
    # "Meta-info about typefaces somewhere in PageBot, so foundries and designers can add their own
    # data there.
    FAMILY_NAMES = FONT_NAME_PATTERNS
    fontNames = context.installedFonts(FONT_NAME_PATTERNS)
    foundryName = 'TN | TYPETR' # TODO: Get from font if available
    if not fontNames: # Not installed, find something else that is expected to exist in OSX:
        foundryName = 'Apple OSX Font'
        FAMILY_NAMES = SYSTEM_FAMILY_NAMES
        for pattern in FAMILY_NAMES:
            fontNames = context.installedFonts(pattern)
            if fontNames:
                break

    # Find matching styles. 
    for styleName in styleNames:
        for fontName in fontNames:
            if styleName is None:
                if fontName in FAMILY_NAMES: # Some fonts are named by plain family name for the Regular.
                    return foundryName, fontName
                continue
            if styleName in fontName:
                return foundryName, fontName
    return None, None # Nothing found.

def italicName(fontName):
    if not '-' in fontName:
        return fontName + '-Italic'
    return fontName + 'Italic'
    
def makeDocument():
    u"""Create Document instance with a single page. Fill the page with elements
    and perform a conditional layout run, until all conditions are solved."""
    
    foundryName, bookName = findTheFont((None, 'Book', 'Regular')) # Find these styles in order.
    _, mediumName = findTheFont(('Medium', 'Book', 'Regular'))
    mediumName = mediumName or bookName # In case medium weight does not exist.
    _, boldName = findTheFont(('Bold', 'Medium'))

    print('Found fonts', bookName, mediumName, boldName)
    
    bookItalicName = italicName(bookName)
    mediumItalicName = italicName(mediumName)
    boldItalicName = italicName(boldName)

    # Get the fonts, so we can dig in the information.
    bookFont = findTheFont(bookName)
    mediumFont = findTheFont(mediumName)
    boldFont = findTheFont(boldName)
    bookItalicFont = findTheFont(bookItalicName)
    mediumItalicFont = findTheFont(mediumItalicName)
    boldItalicFont = findTheFont(boldItalicName)
       
    # Some parameters from the original book
    paperColor = color(rgb='#F4EbC9') # Approximation of paper color of original specimen.
    redColor = color(rgb='#AC1E2B') # Red color used in the original specimen
    
    RedBoxY = mm(118) # Vertical position of the Red Box, on Bodoni chapter.
    columnX = mm(80) # Original 80MM, by we don't adjust, so optically a bit more.
    columnW = mm(60)
    leftPadding = rightPadding = mm(52) # Exception page padding for columns
    
    blurb = Blurb() # Blurb text generator
    
    doc = Document(w=PageWidth, h=PageHeight, originTop=False, startPage=1, autoPages=10)
    # Get default view from the document and set the viewing parameters.
    view = doc.view
    c = view.context
    view.style['fill'] = 1
    # TODO: There is a bug that makes view page size grow, if there are multiple pages and padding > 0
    # TODO: Add optional showing of mid-page line gradient, to suggest bended book pages.
    view.padding = 0 # 20*MM # To show cropmarks and such, make >=20*MM or INCH.
    view.showPageCropMarks = False # Won't show if there is not padding in the view.
    view.showPageRegistrationMarks = False
    view.showPageFrame = True
    view.showPageNameInfo = False
    view.showElementOrigin = False
    view.showElementDimensions = False #ShowDimensions
    view.showElementInfo = False
    view.showTextOverflowMarker = False # Don't show marker in case Filibuster blurb is too long.
 
    labelFont = boldFont
    padding = mm(3, 3, 3, 3)
    fontNameSize = pt(16)
    aboutSize = pt(10)
    glyphSetSize = pt(11)
    glyphSetLeading = mm(5)
    captionSize = pt(7)
    pageNumberSize = pt(12)
    glyphTracking = em(0.2) # Tracking of glyphset samples
    rt = em(0.02) # Relative tracking
    capHeight = labelFont.info.capHeight / labelFont.info.unitsPerEm * fontNameSize

    border = dict(line=INLINE, dash=None, stroke=redColor, strokeWidth=1)

    # -----------------------------------------------------------------------------------
    # Cover from image scan.
    page = doc[1]   
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
    # Add image of cover scan.
    # TODO: Make other positions and scaling work on image element.
    newImage(path=COVER_IMAGE_PATH, parent=page, conditions=[Fit2Sides()], h=H, w=W)
    page.solve()

    # -----------------------------------------------------------------------------------
    # Empty left page.
    page = page.next   
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)
                    
    # -----------------------------------------------------------------------------------
    # Full red page with white chapter title.
    page = page.next   
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
    # Fill full page with red color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=redColor)
    
    bs = c.newString('BOEKLETTER', style=dict(font=boldName, xTextAlign=RIGHT, textFill=paperColor, 
        fontSize=24, rTracking=0.1))#, xTextAlign=RIGHT))
    newTextBox(bs, parent=page, y=page.h-176*MM, conditions=[Left2Left(), Fit2Right(), Fit2Bottom()])
    page.solve()
        
    # -----------------------------------------------------------------------------------
    # Empty left page.
    page = page.next 
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)
            
    # -----------------------------------------------------------------------------------
    # Title page of family.
    page = page.next # Get the single front page from the document.    
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding

    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)
                
    bs = c.newString(labelFont.info.familyName.upper(), style=dict(font=boldName, textFill=paperColor, 
        fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = bs.size
    # TODO: h is still bit of a guess with padding and baseline position. Needs to be solved more structured.
    tbName = newTextBox(bs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1], 
        conditions=[Right2RightSide()], fill=redColor, padding=padding)
    tbName.top = page.h-RedBoxY
    tbName.solve() # Make it go to right side of page.
    
    bs = context.newString(foundryName.upper(), style=dict(font=boldName, textFill=0, 
        fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = bs.size
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbFoundry = newTextBox(bs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1],
        fill=None, padding=padding, borders=border)
    tbFoundry.top = page.h-RedBoxY
    tbFoundry.right = tbName.left   
    
    # Make blurb text about design and typography.
    aboutText = blurb.getBlurb('article_summary', noTags=True)
    bs = context.newString(aboutText, style=dict(font=bookName, textFill=0, fontSize=aboutSize, 
        tracking=0, rTracking=rt, rLeading=1.3, hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbAbout = newTextBox(bs, parent=page, x=columnX, w=columnW, conditions=[Fit2Bottom()])
    tbAbout.top = tbFoundry.bottom - 8*MM
    
    # -----------------------------------------------------------------------------------
    # Page 2 of a family chapter. Glyph overview and 3 columns.

    page = page.next
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding

    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)

    # Glyph set 
    
    caps = u'ABCDEFGHIJKLMNOPQRSTUVWXYZ\n'
    lc = caps.lower()
    figures = u'1234567890\n'
    capAccents = u'ÁÀÄÂÉÈËÊÇÍÌÏÎÓÒÖÔØÚÙÜÛÑ\n'
    lcAccents = capAccents.lower()
    punctuations = u',.;:?![]()-–—“”‘’'
    
    bs = context.newString(caps, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize, 
        leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))
    bs += context.newString(lc, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize, 
        leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))

    if bookName != bookItalicName:
        bs += context.newString(caps, style=dict(font=bookItalicName, textFill=0, fontSize=glyphSetSize, 
            leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))
        bs += context.newString(lc, style=dict(font=bookItalicName, textFill=0, fontSize=glyphSetSize, 
            leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))

    bs += context.newString(figures, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize,     
        leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))
    if bookName != bookItalicName:
        bs += context.newString(figures, style=dict(font=bookItalicName, textFill=0, fontSize=glyphSetSize, 
            leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))

    bs += context.newString(capAccents, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize, 
        leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))
    bs += context.newString(lcAccents, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize, 
        leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))

    if bookName != bookItalicName:
        bs += context.newString(capAccents, style=dict(font=bookItalicName, textFill=0, fontSize=glyphSetSize, 
            leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))
        bs += context.newString(lcAccents, style=dict(font=bookItalicName, textFill=0, fontSize=glyphSetSize, 
            leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))

    bs += context.newString(punctuations, style=dict(font=bookName, textFill=0, fontSize=glyphSetSize, 
        leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))
    if bookName != bookItalicName:
        bs += context.newString(punctuations + '\n', style=dict(font=bookItalicName, textFill=0, 
            fontSize=glyphSetSize, leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))
    else:
        bs += '\n'
        
    if bookName != boldName:
        bs += context.newString(caps+lc+figures+capAccents+lcAccents+punctuations, 
            style=dict(font=boldName, textFill=0, 
            fontSize=glyphSetSize, leading=glyphSetLeading, tracking=0, rTracking=glyphTracking))

    tbGlyphSet = newTextBox(bs, parent=page, w=112*MM, x=leftPadding, conditions=[Top2Top()]) 

    bs = context.newString(labelFont.info.familyName.upper(), style=dict(font=boldName, textFill=paperColor, 
        fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = bs.size
    # TODO: h is still bit of a guess with padding and baseline position. Needs to be solved more structured.
    tbName = newTextBox(bs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1], 
        conditions=[Left2LeftSide()], fill=redColor, padding=padding)
    tbName.top = page.h-RedBoxY
    tbName.solve() # Make it go to right side of page.

    bs = context.newString(foundryName.upper(), style=dict(font=boldName, textFill=0, fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = bs.size
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbFoundry = newTextBox(bs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1],
        fill=None, padding=padding, borders=border)
    tbFoundry.top = page.h-RedBoxY
    tbFoundry.left = tbName.right   

    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True)
    bs = context.newString(specText, style=dict(font=bookName, textFill=0, fontSize=6.5, tracking=0, rTracking=rt, leading=6.5,
        hyphenation='en'))
    # TODO: Last line of text blocks in original is bold.
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbSpec6 = newTextBox(bs, parent=page, x=leftPadding, w=50*MM, h=30*MM)
    tbSpec6.top = tbFoundry.bottom - 8*MM

    bs = context.newString('6 1/2 set\nop 6 pt gegoten (links)', style=dict(font=bookName, fontSize=captionSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=0.05, leading=8, openTypeFeatures=dict(frac=True)))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbCaption6 = newTextBox(bs, parent=page, x=page.pl, w=leftPadding - page.pl - 3*MM, h=30*MM)
    tbCaption6.top = tbSpec6.top
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True)
    bs = context.newString(specText, style=dict(font=bookName, textFill=0, fontSize=6.5, tracking=0, 
        rTracking=rt, leading=7, hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbSpec7 = newTextBox(bs, parent=page, x=leftPadding, w=50*MM, h=35*MM)
    tbSpec7.top = tbSpec6.bottom - 5*MM

    bs = context.newString('op 7 pt gegoten (links)', style=dict(font=bookName, fontSize=captionSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=0.05, leading=8))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbCaption7 = newTextBox(bs, parent=page, x=page.pl, w=leftPadding - page.pl - 3*MM, h=30*MM)
    tbCaption7.top = tbSpec7.top # TODO: Align with first baseline, instead of box top.
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True)
    bs = context.newString(specText, style=dict(font=bookName, textFill=0, fontSize=6.5, tracking=0, 
        rTracking=rt, leading=8, hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbSpec8 = newTextBox(bs, parent=page, h=tbSpec6.top - tbSpec7.bottom)
    tbSpec8.top = tbSpec6.top
    tbSpec8.left = tbSpec6.right + 5*MM
    tbSpec8.w = page.w - page.pr - tbSpec8.left

    bs = context.newString('op 8 pt gegoten (rechts)', style=dict(font=bookName, fontSize=captionSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=0.05, leading=8))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbCaption8 = newTextBox(bs, parent=page, x=page.pl, w=leftPadding - page.pl - 3*MM)
    tbCaption8.bottom = tbSpec8.bottom # TODO: Align with the position of the lowest base line.
    
    # TODO: Calculate the right amount
    bs = context.newString('Corps 6 – per 100 aug.: romein 417, cursief 444, vet 426 letters', 
        style=dict(font=bookName, fontSize=captionSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=rt, leading=8))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbCaptionTotal = newTextBox(bs, parent=page, x=page.pl, w=page.w - page.pl - page.pr)
    tbCaptionTotal.top = tbSpec8.bottom - MM
    
    # Page number
    bs = context.newString(str(pn), 
        style=dict(font=bookName, fontSize=pageNumberSize, 
        textFill=redColor, xTextAlign=LEFT, rTracking=rt, leading=8))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbPageNumber = newTextBox(bs, parent=page, x=leftPadding, w=10*MM)
    tbPageNumber.bottom = 20*MM
            
    # -----------------------------------------------------------------------------------
    # Page 3, 3 columns.
    
    page = page.next
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
            
    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)

    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    bs = context.newString(specText, style=dict(font=bookName, textFill=0, fontSize=8.5, tracking=0, 
        rTracking=rt, leading=8, hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbText1 = newTextBox(bs, parent=page, h=110*MM, w=50*MM, conditions=[Top2Top(), Left2Left()])
    page.solve()
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    bs = context.newString(specText, style=dict(font=bookName, textFill=0, fontSize=8.5, tracking=0, 
        rTracking=rt, leading=9, hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    x = tbText1.right + 5*MM
    tbText2 = newTextBox(bs, parent=page, x=x, y=tbText1.y, h=tbText1.h, w=page.w - x - rightPadding)
    page.solve()
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    bs = context.newString(specText, style=dict(font=bookName, textFill=0, fontSize=8.5, tracking=0, 
        rTracking=rt, leading=10, hyphenation='en'))
    x = tbText1.left
    tbText3 = newTextBox(bs, parent=page, x=x, h=64*MM, w=page.w - x - rightPadding, mt=10*MM, 
        conditions=[Float2TopLeft()])
    
    # TODO: Add red captions here.

    # Red label on the left
    bs = context.newString(labelFont.info.styleName.upper(), style=dict(font=boldName, textFill=paperColor, 
        fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = bs.size
    # TODO: h is still bit of a guess with padding and baseline position. Needs to be solved more structured.
    tbName = newTextBox(bs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1], 
        conditions=[Right2RightSide()], fill=redColor, padding=padding)
    tbName.top = page.h-RedBoxY
    
    # Page number
    bs = context.newString(str(pn), 
        style=dict(font=bookName, fontSize=pageNumberSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=rt, leading=8))
    tbPageNumber = newTextBox(bs, parent=page, x=page.w - rightPadding - 10*MM, w=10*MM)
    tbPageNumber.bottom = 20*MM
                
    # -----------------------------------------------------------------------------------
    # Page 4, 3 columns.
    
    page = page.next
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
            
    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)
    x = leftPadding
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    bs = context.newString(specText, style=dict(font=bookName, textFill=0, fontSize=10.5, tracking=0, 
        rTracking=rt, leading=10, hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    tbText1 = newTextBox(bs, parent=page, x=x, h=55*MM, w=page.w - x - page.pl, conditions=[Top2Top()])
    page.solve()
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    bs = context.newString(specText, style=dict(font=bookName, textFill=0, fontSize=10.5, tracking=0, 
        rTracking=rt, leading=11, hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    newTextBox(bs, parent=page, mt=5*MM, x=x, h=60*MM, w=page.w - x - page.pl, conditions=[Float2Top()])
    page.solve()
        
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    bs = context.newString(specText, style=dict(font=bookName, textFill=0, fontSize=10.5, tracking=0, 
        rTracking=rt, leading=12, hyphenation='en'))
    # TODO: Something wrong with left padding or right padding. Should be symmetric.
    newTextBox(bs, parent=page, mt=5*MM, x=x, h=65*MM, w=page.w - x - page.pl, conditions=[Float2Top()])
    page.solve()
        
    # TODO: Add red captions here.

    # Red label on the right
    bs = c.newString('10.5pt', style=dict(font=boldName, textFill=paperColor, 
        fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = bs.size
    # TODO: h is still bit of a guess with padding and baseline position. Needs to be solved more structured.
    tbName = newTextBox(bs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1], conditions=[Left2LeftSide()], 
        fill=redColor, padding=padding)
    tbName.top = page.h-RedBoxY
    
    # Page number, even on left side.
    bs = c.newString(str(pn), 
        style=dict(font=bookName, fontSize=pageNumberSize, 
        textFill=redColor, xTextAlign=LEFT, rTracking=rt, leading=8))
    tbPageNumber = newTextBox(bs, parent=page, x=leftPadding, w=10*MM)
    tbPageNumber.bottom = 20*MM
                
    # -----------------------------------------------------------------------------------
    # Page 5, 2 columns.
    
    page = page.next
    # Hard coded padding, just for simple demo, instead of filling padding an columns in the root style.
    page.margin = 0
    page.padding = pagePadding
            
    # Fill with paper color
    # TODO: Just background color could be part of page fill instead of extra element.
    newRect(z=-1, parent=page, conditions=[Fit2Sides()], fill=paperColor)

    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    bs = c.newString(specText, style=dict(font=bookName, textFill=0, fontSize=12.5, tracking=0, rTracking=rt, leading=12,
        hyphenation='en'))
    newTextBox(bs, parent=page, x=x, h=64*MM, w=page.w - page.pl - rightPadding, mt=10*MM, conditions=[Top2Top(), Left2Left()])
    
    # Make blurb text about design and typography.
    specText = blurb.getBlurb('article', noTags=True) + ' ' + blurb.getBlurb('article', noTags=True)
    bs = c.newString(specText, style=dict(font=bookName, textFill=0, fontSize=12.5, tracking=0, rTracking=rt, leading=13,
        hyphenation='en'))
    newTextBox(bs, parent=page, x=x, h=64*MM, w=page.w - page.pl - rightPadding, mt=10*MM, conditions=[Float2TopLeft()])
    
    # TODO: Add red captions here.

    # Red label on the left
    bs = c.newString(labelFont.info.styleName.upper(), style=dict(font=boldName, textFill=paperColor, 
        fontSize=fontNameSize, tracking=0, rTracking=0.3))
    tw, th = bs.size
    # TODO: h is still bit of a guess with padding and baseline position. Needs to be solved more structured.
    tbName = newTextBox(bs, parent=page, h=capHeight+3*padding[0], w=tw+2*padding[1], conditions=[Right2RightSide()], 
        fill=redColor, padding=padding)
    tbName.top = page.h-RedBoxY
    
    # Page number
    bs = c.newString(str(pn), 
        style=dict(font=bookName, fontSize=pageNumberSize, 
        textFill=redColor, xTextAlign=RIGHT, rTracking=rt, leading=8))
    tbPageNumber = newTextBox(bs, parent=page, x=page.w - rightPadding - 10*MM, w=10*MM)
    tbPageNumber.bottom = 20*MM

    # Solve remaining layout and size conditions.
       
    score = doc.solve()
    if score.fails:
        print('Condition fails', score.fails)
    return doc # Answer the doc for further doing.


d = makeDocument()
d.export(EXPORT_PATH_PNG) 
d.export(EXPORT_PATH_PDF) 


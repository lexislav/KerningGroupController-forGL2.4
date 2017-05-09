#MenuTitle: Kerning Groups Controller 0.1 for GL2.3+
#encoding: utf-8
"""
KerningGroupsController-forGL2.3.py
Created by Alexandr Hudeček on 2017-05-17.
Copyright (c) 2017 odoka.cz. All rights reserved..
"""

import vanilla
import os

thisFont = Glyphs.font
# builing a more accessible kerning dictionary
# it's a dictionary of lists. newKernDic[master.id][left, right, value]
kernDic = thisFont.kerningDict()
newKernDic = {}
for thisMaster in thisFont.masters:
	kernList = []
	for key1 in kernDic[thisMaster.id]:
		for key2 in kernDic[thisMaster.id][key1]:
			pairInList = [key1, key2, kernDic[thisMaster.id][key1][key2]]
			kernList.append(pairInList)
		newKernDic[thisMaster.id] = kernList

# building popup list
# each value contains a list of glyphs involved. groupsL/R[groupName][glyph, glyph, glyph...]
groupsL = {}
groupsR = {}
for thisGlyph in thisFont.glyphs:
	if thisGlyph.leftKerningGroup != None:
		if not thisGlyph.leftKerningGroup in groupsL:
			groupsL[thisGlyph.leftKerningGroup] = []
		groupsL[thisGlyph.leftKerningGroup].append(thisGlyph.name)

	if thisGlyph.rightKerningGroup != None:
		if not thisGlyph.rightKerningGroup in groupsR:
			groupsR[thisGlyph.rightKerningGroup] = []
		groupsR[thisGlyph.rightKerningGroup].append(thisGlyph.name)


class AppController:

    #WINDOW SETTINGS
    editX = 180
    editY = 22
    textY  = 17
    spaceX = 10
    spaceY = 20
    windowWidth  = spaceX*3+editX*1.5
    windowHeight = 405
    popupAdjust = 3

    #init opens the window
    def __init__(self):
        self.w = self.getWindow()
        self.w.open()
        pass

    def getWindow(self):

        #open window
        w = vanilla.FloatingWindow(
			( self.windowWidth, self.windowHeight ), # default window size
			"Kerning Groups Controller", # window title
			minSize = ( self.windowWidth, self.windowHeight ), # minimum size (for resizing)
			maxSize = ( self.windowWidth + 240, self.windowHeight + 300), # maximum size (for resizing)
			autosaveName = "com.OdOka.KerningGroupsController.mainwindow" # stores last window position and size
		)

        #UI
        height = self.spaceY

        w.text0 = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "Group", sizeStyle='regular' )
        w.radio = vanilla.RadioGroup( (self.spaceX+130, height, 120, self.textY), ["Left", "Right"], isVertical = False, sizeStyle='regular', callback=self.switchList)
        w.radio.set(0)
        height += self.spaceY+self.textY
        w.text1 = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "Choose Group", sizeStyle='regular' )
        w.popupGroup = vanilla.PopUpButton( (self.spaceX+130, height-self.popupAdjust, -10, self.editY), [str(x) for x in sorted(groupsL)], sizeStyle='regular' )
        height += self.spaceY+self.textY
        w.text2 = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "Choose glyph", sizeStyle='regular' )
        w.popupGlyph = vanilla.PopUpButton( (self.spaceX+130, height-self.popupAdjust, -10, self.editY), [str(x) for x in sorted(groupsL)], sizeStyle='regular' )
        height += self.spaceY+self.textY
        w.text3 = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "What to do", sizeStyle='regular' )
        w.radioOptions = vanilla.RadioGroup( (self.spaceX+130, height, 150, self.textY*5), ["copy kerning values","relative change in %","absolute change","do not kern"], isVertical = True, sizeStyle='regular')
        w.radioOptions.set(0)
        height += self.textY*5 + self.editY/2
        w.text4 = vanilla.TextBox( (self.spaceX+130, height, 40, self.textY), "Value", sizeStyle='regular' )
        w.value = vanilla.EditText( (self.spaceX+165+self.spaceX, height, 40, self.editY), "", sizeStyle = 'regular' )
        height += self.spaceY+self.editY
        w.text5 = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "Assign new group", sizeStyle='regular' )
        w.popupAssign = vanilla.PopUpButton( (self.spaceX+130, height-self.popupAdjust, -10, self.editY), [str(x) for x in sorted(groupsL)], sizeStyle='regular' )
        height += self.spaceY+self.editY
        w.text6 = vanilla.TextBox((self.spaceX, height, 80, 20), "Apply to:", sizeStyle = 'regular')
        w.radioApplyTo = vanilla.RadioGroup((self.spaceX+130, height, -15, 40), [ "To current font only", "To all open fonts" ], sizeStyle = 'regular' )
        w.radioApplyTo.set(0)

        #height += 40 + 20

        # w.textApply = vanilla.TextBox((15, height, 80, 20), "Apply:", sizeStyle = 'regular')
        # w.checkBoxRenameIndividualGlyphs = vanilla.CheckBox((80, height, -15, 19), "Rename individual glyphs", value=False, sizeStyle = 'regular')
        # height += 19
        # w.checkBoxUpdateGlyphInfo = vanilla.CheckBox((80, height, -15, 19), "Apply Update Glyph Info", value=True, sizeStyle = 'regular')
        # height += 19
        # w.checkBoxAddSuffixesToLigatures = vanilla.CheckBox((80, height, -15, 19), "Add suffixes to ligatures", value=False, sizeStyle = 'regular')
        # height += 19
        # w.checkBoxRenameSuffixes = vanilla.CheckBox((80, height, -15, 19), "Rename suffixes", value=False, sizeStyle = 'regular')
        # height += 19
        #
        # height += 20
        #
        # w.textOptions = vanilla.TextBox((15, height, 80, 20), "Remove:", sizeStyle = 'regular')
        # w.checkBoxDeleteUnnecessaryGlyphs = vanilla.CheckBox((80, height, -15, 19), "Delete Unnecessary Glyphs", value = False, sizeStyle = 'regular')
        # height += 19
        # w.checkBoxRemoveGlyphOrder = vanilla.CheckBox((80, height, -15, 19), "original glyph order ", value=False, sizeStyle = 'regular')
        # height += 19
        # w.checkBoxRemoveAllCustomParameters = vanilla.CheckBox((80, height, -15, 19), "all custom parameters", value=False, sizeStyle = 'regular')
        # height += 19
        # w.checkBoxRemoveAllMastersCustomParameters = vanilla.CheckBox((80, height, -15, 19), "all masters custom parameters", value=False, sizeStyle = 'regular')
        # height += 19
        # w.checkBoxRemoveAllFeatures = vanilla.CheckBox((80, height, -15, 19), "all OpenType features, classes, prefixes", value=False, sizeStyle = 'regular')
        # height += 19
        # w.checkBoxRemovePUA = vanilla.CheckBox((80, height, -15, 19), "remove PUA", value=False, sizeStyle = 'regular')
        # height += 19

        w.buttonProcess = vanilla.Button((-15 - 80, -15 - 20, -15, -15), "Process", sizeStyle = 'regular', callback=self.process)
        w.setDefaultButton(w.buttonProcess)

        w.spinner = vanilla.ProgressSpinner((15, -15 - 16, 16, 16), sizeStyle = 'regular')

        return w

    #def updateWindow(self, sender):
    #    self.w.textEditGlyphsNames._nsObject.setEditable_(self.w.checkBoxDeleteGlyphs.get())

    def getSettings(self):
        out = {
            #"input": self.w.radioInput.get(),
            "options": {
                # "UpdateGlyphInfo": self.w.checkBoxUpdateGlyphInfo.get(),
                # "RemoveGlyphOrder": self.w.checkBoxRemoveGlyphOrder.get(),
                # "RemoveAllCustomParameters": self.w.checkBoxRemoveAllCustomParameters.get(),
                # "RemoveAllMastersCustomParameters": self.w.checkBoxRemoveAllMastersCustomParameters.get(),
                # "AddSuffixesToLigatures": self.w.checkBoxAddSuffixesToLigatures.get(),
                # "RenameSuffixes": self.w.checkBoxRenameSuffixes.get(),
                # "RenameIndividualGlyphs": self.w.checkBoxRenameIndividualGlyphs.get(),
                # "RemoveAllFeatures": self.w.checkBoxRemoveAllFeatures.get(),
                # "RemovePUA": self.w.checkBoxRemovePUA.get(),
                # "DeleteUnnecessaryGlyphs": self.w.checkBoxDeleteUnnecessaryGlyphs.get()
            }
        }
        return out

    def switchList(self, sender):
		try:
			if self.w.radio.get() == 0:
				self.w.popupGroup.setItems(sorted(groupsL))
			elif self.w.radio.get() == 1:
				self.w.popupGroup.setItems(sorted(groupsR))
		except Exception, e:
			print "Rename Kerning Group Error (switchList): %s" % e

    def process(self, sender):
        self.w.spinner.start()
        worker = AppWorker()
        worker.start(self.getSettings())
        self.w.spinner.stop()
        self.displayLog(worker.getLog())

    def displayLog(self, s):
        log = vanilla.FloatingWindow((360, 480), 'Log')
        log.textEditor = vanilla.TextEditor((0, 0, -1, -1))
        log.textEditor.set(s)
        log.open()



class AppWorker:

    def __init__(self):
        pass

    def printLog(self, message, addLine):
        self.outputLog += message + '\n'
        if addLine == True:
            self.outputLog += '\n'
            print message + '\n'
        else:
            print message

    def get_all_font_names(self):
        self.allGlyphsNames = []
        for glyph in self.font.glyphs:
            self.allGlyphsNames.append(glyph.name)
        return True

    def processFont(self, font, onlySelected, options):
        message = '# Proccesing font: ' + self.font.familyName + ' (contains %s glyphs)' % self.glyphs_total
        messlength = len(message)
        self.printLog(message, False)
        message = '-' * messlength
        self.printLog(message, True)

        Glyphs.redraw()
        return True



    def start(self, settings):

        self.outputLog = ''
        self.printLog('==== Starting ====',False)
        self.printLog('===== Done. =====',False)



    def log(self, s):

        self.outputLog += s + '\n'



    def getLog(self):

        return self.outputLog

# Script start
app = AppController()

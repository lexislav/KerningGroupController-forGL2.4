#MenuTitle: Kerning Groups Controller 0.1 for GL2.3+
#encoding: utf-8
"""
KerningGroupsController-forGL2.3.py
Created by Alexandr Hudeček on 2017-05-17.
Copyright (c) 2017 odoka.cz. All rights reserved.
"""

import vanilla
import os

try:
    thisFont = Glyphs.font
    selectedMaster = thisFont.selectedFontMaster
    masterID = selectedMaster.id
    run = True
    if thisFont == None:
        run = False
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

except:
    print "No font or another startup error."
    pass

class AppController:

    #WINDOW SETTINGS
    editX = 180
    editY = 22
    textY  = 17
    spaceX = 10
    spaceY = 20
    windowWidth  = spaceX*3+editX*1.5
    windowHeight = 365
    popupAdjust = 3

    #properties
    selectedGroupGlyphs = []
    selectedGroupName = ""

    def refreshSelectedGroupGlyphs(self, group):
        self.selectedGroupGlyphs = []
        for glyphName in group[self.selectedGroupName]:
            self.selectedGroupGlyphs.append(glyphName)
            # print glyphName,' '

    #init opens the window
    def __init__(self):
        if not run:
            return
        if groupsL:
            self.selectedGroupName = sorted(groupsL)[0]
            self.refreshSelectedGroupGlyphs(groupsL)
        self.w = self.getWindow()
        self.w.open()
        pass

    def getWindow(self):

        #open window
        w = vanilla.FloatingWindow(
    ( self.windowWidth, self.windowHeight ), # default window size
    "Kerning Groups Controller", # window title
    minSize = ( self.windowWidth, self.windowHeight ), # minimum size (for resizing)
    maxSize = ( self.windowWidth + 540, self.windowHeight + 140), # maximum size (for resizing)
    autosaveName = "com.OdOka.KerningGroupsController.mainwindow" # stores last window position and size
    )

        #UI
        height = self.spaceY

        w.text0 = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "Group", sizeStyle='regular' )
        w.radio = vanilla.RadioGroup( (self.spaceX+130, height, 120, self.textY), ["Left", "Right"], isVertical = False, sizeStyle='regular', callback=self.switchList)
        w.radio.set(0)
        height += self.spaceY+self.textY
        w.text1 = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "Choose Group", sizeStyle='regular' )
        w.popupGroup = vanilla.PopUpButton( (self.spaceX+130, height-self.popupAdjust, -15, self.editY), [str(x) for x in sorted(groupsL)], sizeStyle='regular', callback=self.adjustGlyphsList)
        height += self.spaceY+self.textY
        w.text2 = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "Choose glyph", sizeStyle='regular' )
        w.workWithGlyphs = vanilla.EditText( (self.spaceX + 130, height, -15, self.editY), "", sizeStyle = 'regular' )
        #w.popupGlyph = vanilla.PopUpButton( (self.spaceX+130, height-self.popupAdjust, -10, self.editY), [str(x) for x in sorted(self.selectedGroupGlyphs)], sizeStyle='regular' )
        height += self.spaceY+self.textY
        w.textGM = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "Glyphs in group", sizeStyle='small' )
        glyphsInGroupHelper = "No groups. No glyphs."
        if self.selectedGroupName <> "":
            glyphsInGroupHelper = ','.join(sorted(self.selectedGroupGlyphs))
        w.textG = vanilla.TextBox( (self.spaceX+130, height, -15, -15), glyphsInGroupHelper, sizeStyle='small' )
        height += self.spaceY+self.textY*2 + self.spaceY
        w.text3 = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "What to do", sizeStyle='regular' )
        w.radioOptions = vanilla.RadioGroup( (self.spaceX+130, height, 150, self.textY*5), ["copy kerning values","relative change in %","absolute change","do not kern"], isVertical = True, sizeStyle='regular')
        w.radioOptions.set(0)
        height += self.textY*5 + self.editY/2
        w.text4 = vanilla.TextBox( (self.spaceX+130, height, 40, self.textY), "Value", sizeStyle='regular' )
        w.value = vanilla.EditText( (self.spaceX+165+self.spaceX, height, 40, self.editY), "", sizeStyle = 'regular' )
        height += self.spaceY+self.editY
        w.text5 = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "Assign new group", sizeStyle='regular' )
        w.assignNewGroup = vanilla.EditText( (self.spaceX + 130, height, -15, self.editY), "", sizeStyle = 'regular' )
        #w.popupAssign = vanilla.PopUpButton( (self.spaceX+130, height-self.popupAdjust, -10, self.editY), [str(x) for x in sorted(groupsL)], sizeStyle='regular' )
        height += self.spaceY+self.textY
        #w.textEG = vanilla.TextBox( (self.spaceX, height, 120, self.textY), "Existing groups", sizeStyle='small' )
        #w.textEGL = vanilla.TextBox( (self.spaceX+130, height, -15, -15), ','.join(sorted(groupsL)), sizeStyle='small' )
        #height += self.spaceY+self.textY*2 + self.spaceY
        #all font deactivated
        #w.text6 = vanilla.TextBox((self.spaceX, height, 80, 20), "Apply to:", sizeStyle = 'regular')
        #w.radioApplyTo = vanilla.RadioGroup((self.spaceX+130, height, -15, 40), [ "To current font only", "To all open fonts" ], sizeStyle = 'regular' )
        #w.radioApplyTo.set(0)

        # w.checkBoxRenameIndividualGlyphs = vanilla.CheckBox((80, height, -15, 19), "Rename individual glyphs", value=False, sizeStyle = 'regular')
        # w.textOptions = vanilla.TextBox((15, height, 80, 20), "Remove:", sizeStyle = 'regular')

        w.buttonProcess = vanilla.Button((-15 - 80, -15 - 20, -15, -15), "Go", sizeStyle = 'regular', callback=self.process)
        w.setDefaultButton(w.buttonProcess)

        w.spinner = vanilla.ProgressSpinner((15, -15 - 16, 16, 16), sizeStyle = 'regular')

        return w

    #def updateWindow(self, sender):
    #    self.w.textEditGlyphsNames._nsObject.setEditable_(self.w.checkBoxDeleteGlyphs.get())

    def getSettings(self):
        out = {
                "side": "left" if self.w.radio.get() == 0 else "right",
                "selectedGroup": self.selectedGroupName,
                "proceedGlyphs": self.w.workWithGlyphs.get().replace(" ","").split(","),
                "whatToDo": self.w.radioOptions.get(),
                "valueToSet": self.w.value.get(),
                "newGroup": self.w.assignNewGroup.get()
        }
        if out["proceedGlyphs"] == [""]:
            out["proceedGlyphs"] = []
        return out

    def switchList(self, sender):
        index = 0
        try:
            if self.w.radio.get() == 0:
                if groupsL:
                    self.w.popupGroup.setItems(sorted(groupsL))
                    self.selectedGroupName = sorted(groupsL)[index]
                    self.refreshSelectedGroupGlyphs(groupsL)
                    self.w.textG.set(','.join(sorted(self.selectedGroupGlyphs)))
                else:
                    self.w.popupGroup.setItems([])
                    self.selectedGroupName = ""
                    self.w.textG.set("No group, No glyphs.")
            elif self.w.radio.get() == 1:
                if groupsR:
                    self.w.popupGroup.setItems(sorted(groupsR))
                    self.selectedGroupName =  sorted(groupsR)[index]
                    self.refreshSelectedGroupGlyphs(groupsR)
                    self.w.textG.set(','.join(sorted(self.selectedGroupGlyphs)))
                else:
                    self.w.popupGroup.setItems([])
                    self.selectedGroupName = ""
                    self.w.textG.set("No group, No glyphs.")
        except Exception, e:
            print "Kerning Group Controller Error (switchList): %s" % e

    def adjustGlyphsList(self, sender):
        index = self.w.popupGroup.get()
        try:
            if self.w.radio.get() == 0:
                self.selectedGroupName = sorted(groupsL)[index]
                self.refreshSelectedGroupGlyphs(groupsL)
                self.w.textG.set(','.join(sorted(self.selectedGroupGlyphs)))
            elif self.w.radio.get() == 1:
                self.selectedGroupName =  sorted(groupsR)[index]
                self.refreshSelectedGroupGlyphs(groupsR)
                self.w.textG.set(','.join(sorted(self.selectedGroupGlyphs)))
        except Exception, e:
            print "Kerning Group Controller Error (switchList): %s" % e


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

    def nameMaker(self, kernGlyph):
        if kernGlyph[0] == "@":
            return kernGlyph[7:]
        else:
            return thisFont.glyphForId_(kernGlyph).name

    def wtd_to_strings(self, argument):
        switcher = {
            0: "copied",
            1: "added in %",
            2: "set",
        }
        return switcher.get(argument, "nothing")

    def proceedGlyphs(self, settings):
        #vyjmout glyph ze skupiny
        for G in settings["proceedGlyphs"]:
            Gnamed = "@MMK_R_" + G
            if settings["newGroup"] != "":
                GnewGroup = settings["newGroup"]
            else:
                GnewGroup = G

            #all kernign pairs for glyph (both sides for now)
            leftPairs = []
            rightPairs = []
            for L in thisFont.kerning[masterID]:
                if L == "@MMK_L_" + settings["selectedGroup"]:
                    for R in thisFont.kerning[masterID][L]:
                        leftPairs.append(self.nameMaker(R))
                else:
                    if "@MMK_R_" + settings["selectedGroup"] in thisFont.kerning[masterID][L]:
                        rightPairs.append(self.nameMaker(L))
            glyphOnLeftSide = ", ".join(sorted(leftPairs))
            glyphOnRightSide = ", ".join(sorted(rightPairs))
            #set glyphs to proceed
            proceedPairGlyphs = []

            valueToSet = 0
            try:
                valueToSet = int(settings["valueToSet"])
            except ValueError:
                self.printLog('No value. Set to 0.',False)
                pass

            self.printLog('Proceeding Glyph %s' % G,False)
            self.printLog('was removed from group %s' % settings["selectedGroup"],False)
            self.printLog('and assigned to new group %s' % GnewGroup,False)
            # smazat skupinu
            # přiřadit novou skupinu #NOTE: vytvářet novou skupinu podle názvu znaku? Trošku nebezpečné, pokud už tajková skupina existuje…
            if settings["side"] == "left":
                thisFont.glyphs[G].leftKerningGroup = GnewGroup
            elif settings["side"] == "right":
                thisFont.glyphs[G].rightKerningGroup = GnewGroup


            if settings["whatToDo"] == 0:
                self.printLog('kerning will be copied from existing pairs', False)
            if settings["whatToDo"] == 1:
                self.printLog('kerning will be adjusted for %s  (percent)' % valueToSet, False)
            if settings["whatToDo"] == 2:
                self.printLog('kerning will set to %s' % valueToSet, False)
            if settings["whatToDo"] == 2:
                self.printLog('kerning won''t be set', False)

            self.printLog('In pairs on left side (leading glyph)',False)
            self.printLog(glyphOnLeftSide,False)
            self.printLog('In pairs on right side (leading glyph)',False)
            self.printLog(glyphOnRightSide,False)

            # for znak in proceedPairGlyphs:
            # zkopírovat kerning z řídícho znaku, upravit pomocí value
            # Set kerning for 'T' and all members of kerning class 'a'
            # For LTR fonts, always use the .rightKerningKey for the first (left) glyph of the pair, .leftKerningKey for the second (right) glyph.
            #font.setKerningForPair(font.selectedFontMaster.id, font.glyphs['T'].rightKerningKey, font.glyphs['a'].leftKerningKey, -60)
        else:
            self.printLog('No glyph to work with :-/',False)

        #upravit všechny páry dle libosti
        #vytvořit novou skupinu pro glyph
        return

    def start(self, settings):
        self.outputLog = ''
        self.printLog('==== Starting ====',False)
        if len(settings["proceedGlyphs"]) > 0:
            self.proceedGlyphs(settings)
        else:
            self.printLog('No glyph to work with :-/',False)
        self.printLog('===== Done. =====',False)

    def log(self, s):
        self.outputLog += s + '\n'


    def getLog(self):
        return self.outputLog

# Script start
app = AppController()

#MenuTitle: Kerning Groups Controller 0.2 for GL2.3+
#encoding: utf-8
"""
KerningGroupsController-forGL2.3.py v0.2.1
Created by Alexandr Hudeček on 2017-05-17.
Copyright (c) 2017 odoka.cz. All rights reserved.
"""

import vanilla
import os

#globals definitions
thisFont = None
selectedMaster = None
masterID = None
run = True
kernDic = None
groupsL = {}
groupsR = {}



try:
    thisFont = Glyphs.font
    selectedMaster = thisFont.selectedFontMaster
    masterID = selectedMaster.id
    if thisFont == None:
        run = False
except:
    print "No font or another startup error."
    pass

def refreshGlobals():
    #reset values
    global groupsL
    global groupsR
    global kernDic
    groupsL = {}
    groupsR = {}
    kernDic = thisFont.kerningDict()
    for thisGlyph in thisFont.glyphs:
        if thisGlyph.rightKerningGroup != None:
    		if not thisGlyph.rightKerningGroup in groupsL:
    			groupsL[thisGlyph.rightKerningGroup] = []
    		groupsL[thisGlyph.rightKerningGroup].append(thisGlyph.name)
        if thisGlyph.leftKerningGroup != None:
            if not thisGlyph.leftKerningGroup in groupsR:
    			groupsR[thisGlyph.leftKerningGroup] = []
            groupsR[thisGlyph.leftKerningGroup].append(thisGlyph.name)
    return True

refreshGlobals()

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

    def updateWindow(self, settings):
        refreshGlobals()
        self.w.popupGroup.set(0)
        if settings["side"] == "left":
            self.selectedGroupName = sorted(groupsL)[0]
            self.refreshSelectedGroupGlyphs(groupsL)
        else:
            self.selectedGroupName = sorted(groupsR)[0]
            self.refreshSelectedGroupGlyphs(groupsR)
        self.adjustGroupList(settings["side"])
        self.w.textG.set(','.join(sorted(self.selectedGroupGlyphs)))

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

    def adjustGroupList(self,side):
        if side =="left":
            updateThoseGroups = groupsL
        else:
            updateThoseGroups = groupsR
        self.w.popupGroup.setItems([str(x) for x in sorted(updateThoseGroups)])
        self.adjustGlyphsList
        return


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
        settings = self.getSettings()
        worker.start(settings)
        self.w.spinner.stop()
        self.displayLog(worker.getLog())
        self.updateWindow(settings)
        # self.w.close()

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

    def processFont(self):
        message = '# Proccesing font: ' + thisFont.familyName
        messlength = len(message)
        self.printLog(message, False)
        message = '-' * messlength
        self.printLog(message, True)
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
        # go trought all glyphs named in dialog
        for G in settings["proceedGlyphs"]:
            if G in thisFont.glyphs:
                Gnamed = "@MMK_R_" + G
                GnewGroup = settings["newGroup"]
                GwasGroup = settings["selectedGroup"]
                GgroupPreface = True
                # new group named by glyph if not specified
                if GnewGroup != "":
                    GpairName = GnewGroup
                else:
                    GpairName = G
                    GgroupPreface = False

                #all kernign pairs for group leading glyph (both sides for now)
                leftPairs = []
                rightPairs = []
                for L in thisFont.kerning[masterID]:
                    if L == "@MMK_L_" + GwasGroup:
                        for R in thisFont.kerning[masterID][L]:
                            leftPairs.append(self.nameMaker(R))
                    else:
                        if "@MMK_R_" + GwasGroup in thisFont.kerning[masterID][L]:
                            rightPairs.append(self.nameMaker(L))
                glyphOnLeftSide = ", ".join(sorted(leftPairs))
                glyphOnRightSide = ", ".join(sorted(rightPairs))
                #all kernign pairs for glyph (both sides for now)

                leftPairsG = []
                rightPairsG = []
                for L in thisFont.kerning[masterID]:
                    if L == "@MMK_L_" + G:
                        for R in thisFont.kerning[masterID][L]:
                            leftPairsG.append(self.nameMaker(R))
                    else:
                        if "@MMK_R_" + G in thisFont.kerning[masterID][L]:
                            rightPairsG.append(self.nameMaker(L))
                glyphOnLeftSideG = ", ".join(sorted(leftPairsG))
                glyphOnRightSideG = ", ".join(sorted(rightPairsG))

                #set glyphs to proceed
                proceedPairGlyphs = []
                deleteTheseGlyphs = []
                if settings["side"] == "left":
                    proceedPairGlyphs = leftPairs
                    deleteTheseGlyphs = leftPairsG
                elif settings["side"] == "right":
                    proceedPairGlyphs = rightPairs
                    deleteTheseGlyphs = rightPairsG

                # value set
                valueToSet = 0
                try:
                    valueToSet = int(settings["valueToSet"])
                except ValueError:
                    self.printLog('No value. Set to 0.',False)
                    pass

                #glyph from group and assign new
                self.printLog('',False)
                self.printLog('Proceeding Glyph %s' % G,False)
                self.printLog('was removed from group %s' % GwasGroup,False)
                deletePairs = False
                if settings["side"] == "left":
                    thisFont.glyphs[G].rightKerningGroup = GnewGroup
                    if GnewGroup in groupsL:
                        deletePairs = True
                    # else:
                    #     GnewGroup = "@MMK_L_" + GnewGroup
                elif settings["side"] == "right":
                    thisFont.glyphs[G].leftKerningGroup = GnewGroup
                    if GnewGroup in groupsR:
                        deletePairs = True
                    # else:
                    #     GnewGroup = "@MMK_R_" + GnewGroup
                if GnewGroup == "":
                    self.printLog('and will be assignet to no group.',False)
                else:
                    self.printLog('and assigned to new group %s' % GnewGroup,False)

                #create pairs for every leading glyph decission model
                createPairs = False
                if GnewGroup != "" and G == settings["proceedGlyphs"][0]:
                    createPairs = True
                if GnewGroup == "":
                    createPairs = True

                #Moving to existing group. Existing glyph's pairs will be deleted, not necessry anymore
                pairPreface = ""
                if deletePairs:
                    createPairs = False
                    self.printLog('Glyph moved to existing group. No pairs needed anymore.', False)
                    self.printLog('Pairs to delete on left side',False)
                    self.printLog(glyphOnLeftSideG,False)
                    self.printLog('Pairs to delete on right side',False)
                    self.printLog(glyphOnRightSideG,False)
                    for pairForG in proceedPairGlyphs:
                        if settings["side"] == "left":
                            if GgroupPreface:
                                pairPreface = "@MMK_L_"
                            else:
                                pairPreface = ""
                            thisFont.removeKerningForPair(masterID, pairPreface+GwasGroup, "@MMK_R_"+pairForG)
                            print("Trying to remove " + GwasGroup + "_" + pairForG)
                        elif settings["side"] == "right":
                            if GgroupPreface:
                                pairPreface = "@MMK_R_"
                            else:
                                pairPreface = ""
                            thisFont.removeKerningForPair(masterID, "@MMK_L_"+pairForG, pairPreface+GwasGroup)
                            print("Trying to remove: " + pairForG + "_" + GwasGroup)

                #Creting new group. For every leading Glyph a pairs will be creted
                if createPairs:
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

                    for pairForG in proceedPairGlyphs:
                        recalculatedValue = 0.0
                        if settings["side"] == "left":
                            # print("Pair LR: " + settings["selectedGroup"] + "_" + pairForG)
                            if GgroupPreface:
                                pairPreface = "@MMK_L_"
                            else:
                                pairPreface = ""
                            wasValue = thisFont.kerningForPair(masterID, "@MMK_L_"+GwasGroup, "@MMK_R_"+pairForG)
                            if settings["whatToDo"] == 0:
                                recalculatedValue = wasValue
                            if settings["whatToDo"] == 1:
                                recalculatedValue = wasValue + self.percentage(wasValue,valueToSet)
                            if settings["whatToDo"] == 2:
                                recalculatedValue = valueToSet
                            # print(recalculatedValue)
                            if settings["whatToDo"] != 2:
                                thisFont.setKerningForPair(masterID, pairPreface+GpairName, "@MMK_R_"+pairForG, recalculatedValue)
                            print pairPreface+GpairName + " / "+ "@MMK_R_"+pairForG
                        elif settings["side"] == "right":
                            # print("Pair LR: " + pairForG + "_" + settings["selectedGroup"])
                            if GgroupPreface:
                                pairPreface = "@MMK_R_"
                            else:
                                pairPreface = ""
                            wasValue = thisFont.kerningForPair(masterID, "@MMK_L_"+pairForG, pairPreface+GwasGroup)
                            # print(wasValue)
                            if settings["whatToDo"] == 0:
                                recalculatedValue = wasValue
                            if settings["whatToDo"] == 1:
                                recalculatedValue = wasValue + self.percentage(wasValue,valueToSet)
                            if settings["whatToDo"] == 2:
                                recalculatedValue = valueToSet
                            # print(recalculatedValue)
                            if settings["whatToDo"] != 2:
                                thisFont.setKerningForPair(masterID, "@MMK_L_"+pairForG, "@MMK_R_"+GpairName, recalculatedValue)
                            print "@MMK_L_"+pairForG+" / "+pairPreface+GpairName
            else:
                self.printLog('',False)
                self.printLog("Wrong glyph name: " + G, True)
        else:
            if G == "":
                self.printLog('No glyph to work with :-/',False)
            else:
                self.printLog('No more glyphs to work with :-/',False)
        return

    def percentage(self, wasValue, percents):
        return float(wasValue)*float(percents) / 100

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

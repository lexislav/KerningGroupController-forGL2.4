#MenuTitle: Kerning Groups Controller 0.1 for GL2.3+
#encoding: utf-8
"""
KerningGroupsController-forGL2.3.py
Created by Alexandr Hudeček on 2017-05-17.
Copyright (c) 2017 odoka.cz. All rights reserved.
"""

import vanilla
import os

class AppController:

    def __init__(self):
        pass

    def run(self):
        self.w = self.getWindow()
        self.w.open()

    def getWindow(self):

        out = vanilla.FloatingWindow((355, 335), "Window Name")
        height = 20

        out.textProcess = vanilla.TextBox((15, height, 80, 20), "Process:", sizeStyle = 'regular')
        out.radioInput = vanilla.RadioGroup((80, height, -15, 40), [ "All glyphs in current font", "All glyphs in all fonts" ], sizeStyle = 'regular')
        #out.radioInput.set(AppWorker.INPUT_SELECTED_CURRENT_FONT)

        height += 40 + 20

        out.textApply = vanilla.TextBox((15, height, 80, 20), "Apply:", sizeStyle = 'regular')
        out.checkBoxRenameIndividualGlyphs = vanilla.CheckBox((80, height, -15, 19), "Rename individual glyphs", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxUpdateGlyphInfo = vanilla.CheckBox((80, height, -15, 19), "Apply Update Glyph Info", value=True, sizeStyle = 'regular')
        height += 19
        out.checkBoxAddSuffixesToLigatures = vanilla.CheckBox((80, height, -15, 19), "Add suffixes to ligatures", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRenameSuffixes = vanilla.CheckBox((80, height, -15, 19), "Rename suffixes", value=False, sizeStyle = 'regular')
        height += 19

        height += 20

        out.textOptions = vanilla.TextBox((15, height, 80, 20), "Remove:", sizeStyle = 'regular')
        out.checkBoxDeleteUnnecessaryGlyphs = vanilla.CheckBox((80, height, -15, 19), "Delete Unnecessary Glyphs", value = False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveGlyphOrder = vanilla.CheckBox((80, height, -15, 19), "original glyph order ", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveAllCustomParameters = vanilla.CheckBox((80, height, -15, 19), "all custom parameters", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveAllMastersCustomParameters = vanilla.CheckBox((80, height, -15, 19), "all masters custom parameters", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemoveAllFeatures = vanilla.CheckBox((80, height, -15, 19), "all OpenType features, classes, prefixes", value=False, sizeStyle = 'regular')
        height += 19
        out.checkBoxRemovePUA = vanilla.CheckBox((80, height, -15, 19), "remove PUA", value=False, sizeStyle = 'regular')
        height += 19

        out.buttonProcess = vanilla.Button((-15 - 80, -15 - 20, -15, -15), "Process", sizeStyle = 'regular', callback=self.process)
        out.setDefaultButton(out.buttonProcess)

        out.spinner = vanilla.ProgressSpinner((15, -15 - 16, 16, 16), sizeStyle = 'regular')

        return out

    #def updateWindow(self, sender):
    #    self.w.textEditGlyphsNames._nsObject.setEditable_(self.w.checkBoxDeleteGlyphs.get())

    def getSettings(self):
        out = {
            "input": self.w.radioInput.get(),
            "options": {
                "UpdateGlyphInfo": self.w.checkBoxUpdateGlyphInfo.get(),
                "RemoveGlyphOrder": self.w.checkBoxRemoveGlyphOrder.get(),
                "RemoveAllCustomParameters": self.w.checkBoxRemoveAllCustomParameters.get(),
                "RemoveAllMastersCustomParameters": self.w.checkBoxRemoveAllMastersCustomParameters.get(),
                "AddSuffixesToLigatures": self.w.checkBoxAddSuffixesToLigatures.get(),
                "RenameSuffixes": self.w.checkBoxRenameSuffixes.get(),
                "RenameIndividualGlyphs": self.w.checkBoxRenameIndividualGlyphs.get(),
                "RemoveAllFeatures": self.w.checkBoxRemoveAllFeatures.get(),
                "RemovePUA": self.w.checkBoxRemovePUA.get(),
                "DeleteUnnecessaryGlyphs": self.w.checkBoxDeleteUnnecessaryGlyphs.get()
            }
        }
        return out

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
app.run()

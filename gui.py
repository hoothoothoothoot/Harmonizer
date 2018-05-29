import os.path

from appJar import gui
from tkinter import Tk
from tkinter import filedialog
import pyautogui

from harmonizer import Harmonizer

'''
appJar lib made by Richard Jarvis
git : https://github.com/jarvisteach/appJar
docs : http://appjar.info/

Class GUI
Manages Gui for project Harmonizer
'''

FILE_NOT_FOUND = "File does not exist"
HALF_SCREEN_SIZE = str(pyautogui.size()[0]/2)+"x"+str(pyautogui.size()[1])
Q_SCREEN_SIZE = str(pyautogui.size()[0]/2)+"x"+str(pyautogui.size()[1]/2)
THEME = "plastik"

class Gui(object):

	def __init__(self):
		'''
		Creates window of size 650x300
		'''

		self.file_path_in = ""
		self.file_path_out = ""

		self.harm = Harmonizer()

		self.app = gui("Harmonizer", "650x300", useTtk=True)
		self.app.setTtkTheme(THEME)

		self.app.setIcon("bestwhale.gif")
		self.app.setPadding([0,15])
		self.app.setInPadding([20,5])
		self.app.setResizable(True)

		self.app.addLabel("Input", "Select input file *", 0, 0)
		self.app.addLabel("Output", "Select output file ", 1, 0)
		self.app.addEntry("Select input file *", 0, 1, colspan=3)
		self.app.addButton("Select Input", self.selectInputFile, 0, 4)
		self.app.addEntry("Select output file ", 1, 1, colspan=3)
		self.app.addButton("Select Output", self.selectOutputFile, 1, 4)

		self.app.addButton("GO", self.main, 2, 1, 1)
		self.app.addButton("Clear", self.clear, 2, 3, 1)

		self.app.enableEnter(self.main)
		self.app.setFocus("Select input file *")
		self.app.setLabelAlign("Input", "center")
		self.app.setLabelAlign("Output", "center")
		self.app.setAllEntryWidths(30)
		self.app.setAllLabelWidths(8)
		self.app.setAllButtonWidths(10)

		self.app.go()

	def selectInputFile(self):
		'''
		Opens a dialog window to choose input file
		Store path of file in self.Entry
		'''
		Tk().withdraw()
		self.file_path_in = filedialog.askopenfilename()
		if ".csv" in self.file_path_in:
			self.app.setEntry("Select input file *", self.file_path_in, False)
		else:
			self.app.errorBox("WRONG INPUT FILE", "Please select a CSV file")

	def selectOutputFile(self):
		'''
		Opens a dialog window to choose output file
		Store path of file in self.Entry
		'''
		Tk().withdraw()
		self.file_path_out = filedialog.askopenfilename()
		if ".csv" in self.file_path_out:
			self.app.setEntry("Select output file ", self.file_path_out, False)
		else:
			self.app.errorBox("WRONG INPUT FILE", "Please select a CSV file")

	def clear(self):
		self.app.clearAllEntries()
		self.harm = Harmonizer()

	def main(self):
		'''
		Creates a Harmonizer

		@see Harmonizer.construct

		@see self.displayResults
		'''
		self.harm = Harmonizer()
		self.file_path_in = self.app.getEntry("Select input file *")
		self.file_path_out = self.app.getEntry("Select output file ")
		if not self.file_path_in:
			self.app.errorBox("NO INPUT FILE", "Please select input file")
		elif not ".csv" in self.file_path_in:
			self.app.errorBox("WRONG INPUT FILE", "Please select a CSV file")
		elif not os.path.exists(self.file_path_in):
			self.app.errorBox("FILE NOT FOUND", "File does not exist")
		elif os.stat(self.file_path_in).st_size == 0:
			self.app.errorBox("EMPTY FILE", "File is empty")
		elif not os.path.isfile(self.file_path_in):
			self.app.errorBox("NOT A FILE", "Please select a file")
		elif not self.file_path_out:
			self.harm.construct(self.file_path_in)
			self.displayResults()
		else:
			if not ".csv" in self.file_path_out:
				self.app.errorBox("WRONG INPUT FILE", "Please select a CSV file")
			else:
				self.harm.construct(self.file_path_in, self.file_path_out)
				self.displayResults()
		
	def close(self):
		'''
		Stops sub window 
		@see self.displayResults
		'''
		self.app.stopSubWindow()
		self.app.destroySubWindow("Results")

	def displayResults(self):
		'''
		Displays the results from Harmonizer.construct

		@see self.main
		'''
		tab = ["Actual grade", "Average"]
		for i in range(self.harm.nmarkers):
			tab.append("Marker "+str(i+1))
		self.app.startSubWindow("Results")
		self.app.setSize(Q_SCREEN_SIZE)
		self.app.setTtkTheme(THEME)
		self.app.setPadding([10,10])
		self.app.setSticky("news")
		self.app.addGrid("Grid", [tab], 0, 0, 2)
		for line in self.harm.data:
			self.app.addGridRow("Grid", line)
		self.app.setSticky("")
		self.app.setPadding([5,10])
		self.app.setInPadding([20,5])
		self.app.addButton("OK", self.close, 1, 0, 1)
		self.app.addButton("Details", self.displayCalcs, 1, 1, 1)
		self.app.showSubWindow("Results")

	def closeCalcs(self):
		'''
		Stops sub window 
		@see self.displayCalcs
		'''
		self.app.stopSubWindow()
		self.app.destroySubWindow("Calculations")

	def displayCalcs(self):
		'''
		Displays all probabilities 

		@see self.displayResults
		'''
		self.app.startSubWindow("Calculations")
		self.app.setSize(HALF_SCREEN_SIZE)
		self.app.setTtkTheme(THEME)
		self.app.setPadding([10, 10])
		self.app.setSticky("news")
		self.app.addGrid("Grid2", [["Probabilities"]])
		for group in self.harm.toPrint():
			for line in group:
				self.app.addGridRow("Grid2", [line])
		self.app.setSticky("")
		self.app.setPadding([5,10])
		self.app.setInPadding([20,5])
		self.app.addButton("Done", self.closeCalcs)
		self.app.showSubWindow("Calculations")

harmony = Gui()
import csv
import sys
import os

'''
Class CSV
Manages CSV for project Harmonizer
'''

FILE_NOT_FOUND = "File does not exist"

class CSV(object):

	def __init__(self, csvInput, csvOutput):
		'''
		Creates a CSV manager with @param csvInput as @self input
		and @param csvOutput as @self output
		'''
		self.input = csvInput
		self.output = csvOutput

	def fillFile(self):
		return True

	#############
	### INPUT ###
	#############

	def extractGradesColumn(self, column):
		'''
		Extracts @param column of grades in @self input CSV file
		'''
		try:
			fd = open(self.input, newline='')
			file = csv.reader(fd, dialect='excel', delimiter=',', quotechar='"')
			marks = []
			for line in file:
				marks.append(line[column])
			return marks
		except FileNotFoundError:
			print(FILE_NOT_FOUND)

	def extractGradesRows(self):
		'''
		Extract each row of grades in @self input CSV file
		'''
		try:
			fd = open(self.input, newline='')
			file = csv.reader(fd, dialect='excel', delimiter=',', quotechar='"')
			marks = []
			for line in file:
				marks.append(line)
			return marks
		except FileNotFoundError:
			print(FILE_NOT_FOUND)

	def getNumberOfMarkers(self):
		'''
		Counts the length of a row in @self input CSV file
		The length of a row is the number of markers
		'''
		try:
			if os.stat(self.input).st_size == 0:
				return 0
			else:
				fd = open(self.input, newline='')
				file = csv.reader(fd, dialect='excel', delimiter=',', quotechar='"')
				nmarkers = len(next(file))
				fd.seek(0)
				return nmarkers
		except FileNotFoundError:
			print(FILE_NOT_FOUND)

	##############
	### OUTPUT ###
	##############

	def printGroundTruth(self, harmonizer):
		'''
		Prints in @self output CSV file the new data from @param harmonizer

		@see Harmonizer.getGroundTruthAll
		@see Harmonizer.defineAvgOfReviews

		@see self.extractGradesRows
		'''
		fd = open(self.output, 'w', newline='')
		file = csv.writer(fd, dialect='excel', delimiter=',', quotechar='"')
		for i in range(len(harmonizer.paper.grades)):
			file.writerow([harmonizer.getGroundTruthAll()[i][0]]
				+[str(harmonizer.defineAvgOfReviews(i+1))]
				+self.extractGradesRows()[i])

	def extractData(self):
		'''
		Extracts the new data
		'''
		fd = open(self.output, newline='')
		file = csv.reader(fd, dialect='excel', delimiter=',', quotechar='"')
		data = []
		for line in file:
			data.append(line)
		return data

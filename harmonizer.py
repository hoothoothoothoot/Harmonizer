import numpy as np
import time
import sys

from paper import Paper
from marker import Marker
from csvManager import CSV

'''
Author : hoot

Harmonizer is part of the Bayesian Peer Review project. 

This class computes probabilities of having a grade given reviews from markers, following the bayes theorem :

p(A | B) = p(B | A)*p(A) / p(B)

A being the grade, and B the review(s) from markers. 
'''

class Harmonizer(object):

	def __init__(self):
		'''
		Creates an empty Harmonizer with 
		@self nmarkers the number of markers
		@self marker the markers
		@self paper the paper
		@self data the actual grades and the grades from markers
		'''
		self.nmarkers = 0
		self.markers = []
		self.paper = Paper()
		self.data = []

	def construct(self, csvFileIn, csvFileOut='grades_with_groundtruths.csv'):
		'''
		Assigns data to @self nmarkers, markers, paper and data from
		@param csvFileIn the CSV file that contains the grades 
		@param csvFileOut the CSV file that will store the @self data
		using a @self csvManager 

		@see self.getNumberOfMarkers
		@see self.defineMeanOfReviews
		@see self.defineAvgOfReviews
		@see self.getPaperReviews

		@see CSV.extractGradesColumn
		@see CSV.printGroundTruth
		@see CSV.extractData
		'''
		self.csvManager = CSV(csvFileIn, csvFileOut)
		self.nmarkers = self.csvManager.getNumberOfMarkers()
		if self.nmarkers == 0:
			print("File is empty")
		else:
			for i in range(self.nmarkers):
				self.markers.append(Marker(self.csvManager.extractGradesColumn(i)))

			for i in range(1,len(self.markers[1].reviews)+1):
				self.paper.add(self.defineMeanOfReviews(i), self.defineAvgOfReviews(i), self.getPaperReviews(i))

			self.csvManager.printGroundTruth(self)
			self.data = self.csvManager.extractData()
			self.main()

	#######################
	###### COMPUTING ######
	#######################

	def associate(self, marker):
		'''
			
		@return tuple values of associated self.paper and @param marker

		(grade, review)

		'''
		papers = []
		reviews = []
		values = []

		for review in self.markers[marker].reviews:
			reviews.append(review.grade)

		for grade in self.paper.grades:
			papers.append(grade)
		
		for i in range(len(papers)):
			values.append((papers[i], reviews[i]))
		
		return values

	def computeGivenMarker(self, ag, idM, mark):
		'''
		Computes the probability of having @param ag given @param mark of id @param idM
		or p(ag | mark)
		'''
		p = 0
		values = self.associate(idM-1)
		countV = values.count((ag,mark))

		countM = 0
		for i in range(len(self.markers[idM-1].reviews)):
			if mark == self.markers[idM-1].reviews[i].grade:
				countM += 1
		
		countA = self.paper.grades.count(ag)
		
		if countA == 0 or countM == 0:
			p = 0
		elif countV == 0:
			p = 0
		else:
	 		p = countV / countM
		
		return p

	def computeGivenActualGrade(self, idM, mark, ag):
		'''
		Computes the probability of having @param mark of id @param idM given @param ag
		or p(mark | ag) = (p(mark) * p(ag | mark)) / p(ag)

		@see self.computeGivenMarker
		@see self.determinePofMarker
		@see self.determinePofAg
		'''
		p_AgGivenMarker = self.computeGivenMarker(ag, idM, mark)
		p_Marker = self.determinePofMarker(idM, mark)
		p_Ag = self.determinePofAg(ag)
		return (p_AgGivenMarker * p_Marker) / p_Ag

	def determinePofAg(self, ag):
		'''
		Computes the probability of having @param ag
		or p(ag)
		'''
		total = len(self.paper.grades)
		countAg = self.paper.grades.count(ag)
		return countAg / total

	def determinePofMarker(self, idM, mark):
		'''
		Computes the probability of having @param mark of id @param idM 
		or p(mark)
		'''
		total = len(self.markers[idM-1].reviews)
		countM = 0
		for i in range(len(self.markers[idM-1].reviews)):
			if mark == self.markers[idM-1].reviews[i].grade:
				countM += 1
		return countM / total

	def determineProportion(self, ag, marks):
		'''
		Computes the probability of having @param ag 
		given @param marks the reviews r given by teachers
		or p(ag | r1, r2,.., rn) ~ p(ag) * p(r1 | ag) * p(r2 | ag) *..* p(rn | ag)

		@see self.determinePofAg
		@see self.computeGivenActualGrade
		'''
		p_Ag = self.determinePofAg(ag)
		p_Marks = 1
		for i in range(1, len(marks)+1):
			p_Marks *= self.computeGivenActualGrade(i, marks[i-1], ag)
		return p_Ag * p_Marks

	def getValuesOfPaperGrades(self):
		# return : each value of self.paper.grades in a list
		valuesOfAg = []
		for i in range(max(self.paper.grades)+1):
			if self.paper.grades.count(i) != 0: # and i != ag:
				valuesOfAg.append(i)
		return valuesOfAg

	def compute(self, ag, marks):
		'''
		Computes the probability of having @param ag 
		given @param marks the reviews r given by teachers
		with the normalizing constant
		# p(ag | r1, r2, .., rn) = N * p(ag) * p(r1 | ag) * p(r2 | ag) *..* p(rn | ag)

		@see self.determineProportion
		@see self.getValuesOfPaperGrades
		'''
		numerator = self.determineProportion(ag, marks)
		norm = 0
		
		valuesOfAg = self.getValuesOfPaperGrades()
		
		for value in valuesOfAg:
			norm += self.determineProportion(value, marks)

		N = 1 / norm

		return numerator * N

	def computeWithOneMarker(self, marker):
		'''
		Computes the probability of having @list papergrades given reviews of @param marker
		or for each grade in @list papergrades we have :
		p(grade1 | r1, r2, .., rn)
		p(grade2 | r1, r2, .., rn)
		...
		p(graden | r1, r2, .., rn)

		@see self.getPaperReviews
		@see self.getValuesOfPaperGrades
		@see self.compute
		'''
		marks = self.getPaperReviews(marker)
		papergrades = self.getValuesOfPaperGrades()

		probs = []
		for grade in papergrades:
			probs.append(self.compute(grade, marks))

		return probs

	def computeAll(self):
		'''
		Computes probabilities for all grades and all markers

		@see self.computeWithOneMarker
		'''
		probs = []
		for i in range(1,len(self.paper.grades)+1):
			probs.append(self.computeWithOneMarker(i))
		return probs

	#########################
	###### HARMONIZING ######
	#########################

	def getGroundTruthWithOneMarker(self, marker):
		'''
		A grade is added to newGrades if p(grade | review) > 0.5
		Determines the new grade for a paper

		@see self.compute(grade, marks)
		@return list newGrades 
		'''
		marks = self.getPaperReviews(marker)
		papergrades = self.getValuesOfPaperGrades()

		newGrades = []

		for grade in papergrades:
			if self.compute(grade, marks) > 0.5:
				newGrades.append(grade)
			else:
				pass
		return newGrades

	def getGroundTruthAll(self):
		'''
		Determines the new grades for each @self paper.grade

		@see self.getGroundTruthWithOneMarker
		'''
		newGrades = []
		for i in range(1,len(self.paper.grades)+1):
			newGrades.append(self.getGroundTruthWithOneMarker(i))
		return newGrades

	#########################
	###### STRUCTURING ######
	#########################

	def getPaperReviews(self, idR):
		'''
		@return list paperReviews from @param idR (id of reviews)

		a review is added to paperReviews if review.id matches @param idR

		paperReviews are the reviews to associate with a paper
		'''
		paperReviews = []
		for marker in self.markers:
			for review in marker.reviews:
				if idR == review.id:
					paperReviews.append(review.grade)
		return paperReviews

	def defineMeanOfReviews(self, idR):
		'''
		@return int mean of reviews that have id @param idR
		'''
		return int(round(np.mean(self.getPaperReviews(idR))))

	def defineAvgOfReviews(self, idR):
		'''
		@return float mean of reviews that have id @param idR
		'''
		return np.mean(self.getPaperReviews(idR))

	def toPrintOne(self, marker):
		'''
		@see self.getPaperReviews
		@see self.getValuesOfPaperGrades
		@see self.compute
		@return line of calculation "p(grade | m1, m2,.., mn) = prob"
		'''
		marks = self.getPaperReviews(marker)
		papergrades = self.getValuesOfPaperGrades()

		calc = []
		for grade in papergrades:
			calc.append("p( "+str(grade)+" | "+str(marks)+" ) = "+str(self.compute(grade, marks)))

		return calc

	def toPrint(self):
		'''
		@see self.toPrintOne
		@return all lines of calculation :
		"
		p(grade1 | marks1) = prob
		p(grade2 | marks1) = prob
		.
		.
		p(graden | marks1) = prob
		p(grade1 | marks2) = prob
		.
		.
		p(graden | marksn) = prob

		"
		'''
		calcs = []
		for i in range(1,len(self.paper.grades)+1):
			calcs.append(self.toPrintOne(i))
		return calcs

	def main(self):
		self.computeAll()
		for group in self.toPrint():
			for line in group:
				print(line)

#######################	
###### LAUNCHING ######
#######################
	
if len(sys.argv) == 1:
	print("Please give an input file")
elif len(sys.argv) > 2:
	harm = Harmonizer()
	harm.construct(sys.argv[1], sys.argv[2])
else:
	harm = Harmonizer()
	harm.construct(sys.argv[1])

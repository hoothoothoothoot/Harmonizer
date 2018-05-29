from review import Review

from random import *
import numpy as np
import csv

'''
The class Marker manages and stores Review reviews from markers after being extracted from csv files
'''

class Marker(object):

	def __init__(self, marks): 
		'''
		Creates a marker 
		For each review in @param marks, appends review to @self reviews
		Assigns id to each review in @self reviews

		@see Review.assignID
		'''
		self.reviews = []

		for review in marks:
			self.reviews.append(Review(int(review)))

		for i in range(1, len(marks)+1):
			self.reviews[i-1].assignID(i)

	def toprint(self):
		for review in self.reviews:
			print("Grade given n°{1} is : {0}".format(review.grade, review.id))
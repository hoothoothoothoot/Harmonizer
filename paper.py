'''
The class Paper stores the grades as given from markers

'''
class Paper(object):


	def __init__(self):
		'''
		self.grades are the average in int of all reviews given by markers
		self.fgrades are the average in float of all reviews given by markers
		self.reviews contains arrays of reviews given by markers

		@see Harmonizer.defineMeanOfReviews(idR)
		@see Harmonizer.defineAvgOfReviews(idR)
		@see Harmonizer.getPaperReviews(idR)
		'''
		self.grades = []
		self.fgrades = []
		self.reviews = []

	def add(self, grade, fgrades, reviews):
		#adds @param grade, @param fgrades @param reviews to @this grades, @this fgrades and @this reviews
		self.grades.append(grade)
		self.fgrades.append(fgrades)
		self.reviews.append(reviews)

	def toprint(self):
		for i in range(len(self.grades)):
			print("Paper grade n°{1} : {0}".format(self.grades[i], i+1))
			print("Paper average grade n°{1} : {0}".format(self.fgrades[i], i+1))
			print("Reviews {0} : {1}".format(i+1, self.reviews[i]))
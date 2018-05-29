class Review(object):
	'''
	The class Review stores reviews of markers
	'''

	def __init__(self, grade):
		'''
		Creates a Review with @self id
		and @param grade as @self grade
		'''
		self.id = 0
		self.grade = grade

	def assignID(self, idR):
		# adds @param idR to @this id
		self.id = idR

	def toprint(self):
		print("Review : {0}".format(self.grade))
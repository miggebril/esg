class ESGTopicKey:

	def __init__(self, company, year):
		self.company = company
		self.year = year

	def __hash__(self):
		return hash((self.company, self.year))

	def __eq__(self, other):
		return (self.company, self.year) == (other.company, other.year)

	def __ne__(self, other):
		return not(self == other)

	def __repr__(self):
		return f'{self.company} {self.year}'
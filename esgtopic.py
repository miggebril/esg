class ESGTopic:
	count = 0

	def __init__(self, company, year, token=""):
		self.company = company
		self.year = year
		self.token = token

	def inc(self):
		self.count += 1

	def setToken(self, token):
		self.token = token

	def __hash__(self):
		return hash((self.company, self.year, self.token))

	def __eq__(self, other):
		return (self.company, self.year, self.token, self.count) == (other.company, other.year, other.token, other.count)

	def __ne__(self, other):
		return not(self == other)

	def __repr__(self):
		return f'{self.company} {self.year} {self.token} x {self.count}'

class ESGTokenKey:

	def __init__(self, company, year, token=""):
		self.company = company
		self.year = year
		self.token = token

	def __hash__(self):
		return hash((self.company, self.year, self.token))

	def __eq__(self, other):
		return (self.company, self.year, self.token) == (other.company, other.year, other.token)

	def __ne__(self, other):
		return not(self == other)

	def __repr__(self):
		return f'{self.company} {self.year}: {self.token}'
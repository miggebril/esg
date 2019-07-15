import pymongo
import logging
from esgtopic import ESGTopic

def create(host="localhost", port=27017, dbName="reports"):
	try:
		client = pymongo.MongoClient(f"mongodb://{host}:{port}/")
		db = client[dbName]
			
		data = db['reportTokens']
		data.create_index([("company", pymongo.ASCENDING), ("year", pymongo.ASCENDING), ("token", pymongo.ASCENDING)], name='dataKey', unique=True)
		
		return db
	except Exception as ex:
		logging.exception(f"Error creating database context {dbName}")


def insertTokens(company, year, topics):
	try:
		db = create()
		db["reportTokens"].insert_many([{'company' : company, 'year' : year, 'token' : t.token, 'count' : t.count } for t in topics])
	except Exception as e:
		logging.exception(f"Error creating inserting to context")


def getTokens(company, year):
	try:
		db = create()
		results = list(db['reportTokens'].find(query))
		if results is None:
			return iter([])

		return results
	except Exception as ex:
		logging.exception(f"Error retrieving a record in database context {dbName}")

def getAllTokens():
	try:
		db = create()
		return db["reportTokens"].find_many({})
	except Exception as e:
		logging.exception(f"Error retrieving records in database context {dbName}")

def updateTokens(company, year, tokens, upsert=False):
	try:

		query = { 'company' : company, 'year' : year }

		db = create()
		if upsert:
			db["reportTokens"].update_one(query, {
				'$set' : { 'tokens' : tokens }
				})

		db["reportTokens"].update_one(query, {
			'$set' : { 'tokens' : tokens }
			}, upsert=upsert)

	except Exception as ex:
		logging.exception(f"Error: {ex}")
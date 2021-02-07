import pymongo

def con():
	connect = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
	return connect["khoj"]

def uncrawled(db):
	return db["home_uncrawled"]

def site(db):
	return db["home_sitedetail"]

def keyExtract(db):
	return db["home_keyextract"]

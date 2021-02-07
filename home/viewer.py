from khojadmin.includes.crawler import Sites
import pymongo

con = pymongo.MongoClient("localhost",27017)
db = con.khoj
keyx= db.home_keyextract
uncrawl = db.home_uncrawled
indexx = db.home_index
testx = con.test.model1
rnkx = db.home_rankhandler
rnk = db.home_siterank
sitex = db.home_sitedetail
def uncrawled():
	return uncrawl

def test():
	return testx

	uncrawl.insert_one({"url":"https://www.khec.edu.np/"})
	return

def index():
	return indexx
def key():
	return keyx

def rank():
	return rnk

def ranker():
	return rnkx

def site():
	return sitex

def item():
	item = dict()
	item['url'] = 'url1'
	item['domain']=".com"
	b = "I lost my kitab"
	c = "dd is a kitab chorni"
	item['description']=b
	item['display']=True
	item['priority']=1
	item['title']='kitab lost'
	item['lang']='en'
	item['words_links']="d3ds3"
	item['icon']="/favicon.ico"
	item['visit_count']=0
	u1 = ['url3','url2','url5','url6']
	u2 = ['url1','url6','url7']
	Sites(item,'en',u2)

def find(value):
	for i in value.find():
		print(i)

def cleardb():
	indexx.remove({})
	keyx.remove({})
	rnkx.remove({})
	rnk.remove({})
	sitex.remove({})
	uncrawl.remove({})
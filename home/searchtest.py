import pymongo
con = pymongo.MongoClient("localhost",27017)
db = con.khoj
key = db.home_keyextract
from bson.objectid import ObjectId

text = "kitab chorni"
ids = [ObjectId(i) for i in ["5fb66b4a9ecd682eaec8c7cc", "5fb66b80ba0c4b305c658c08"]]
print(ids)
data = key.aggregate([
        {"$match":{"$text":{"$search":text},"file":{"$in":ids}}},
        {"$unwind":"$original"},
        {"$match":{"original.ktype":"body"}},
        {"$sort":{"original.order":1}},
        {"$group":{"_id":"$_id","file":{"$first":"$file"},"keys":{"$push":"$original"}}},
        {"$project":{"_id":0,"file":1,"keys":{"$slice":["$keys",3]}}},
        {"$unwind":"$keys"},
        {"$lookup":{"from":"home_keyextract","let":{"site":"$file","ord":"$keys"},"pipeline":[
            {"$match":{"$expr":{"$eq":["$file","$$site"]}}},
            {"$unwind":"$original"},
            {"$match":{"original.ktype":"body","$expr":{"$and":[
                {"$gt":["$original.order",{"$sum":["$$ord.order",-25]}]},
                {"$lt":["$original.order",{"$sum":["$$ord.order",25]}]}
            ]}}},
            {"$sort":{"original.order":1}},
            {"$group":{"_id":"$file","content":{"$push":"$original"}}},
            {"$project":{"_id":0,"value":"$content"}}
            ],"as":"content"}},
        {"$unwind":"$content"},
        {"$lookup":{
            "from":"home_sitedetail","localField":"file","foreignField":"_id","as":"site"}
        },{"$unwind":"$site"},
        {"$group":{"_id":"$file","content":{"$push":"$content"},"url":{"$first":"$site.url"},"title":{"$first":"$site.title"}}},
        ])
result = []

for i in data:
    tmp=[]
    for j in i["content"]:
        for k in j["value"]:
            tmp.append(k) if k not in tmp else False
    i["content"]=' '.join([t["original"] for t in tmp])
    result.append(i)
print(result)
        
        
        
    

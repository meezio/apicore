from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from ..exceptions import Http400Exception, Http404Exception, Http409Exception

# TODO host, port, ssl, login, password from config file
client = MongoClient(connect=False)


class Db:
    db = client["wiri"]  # TODO from config file

    @classmethod
    def getMany(cls, collection, offset=0, limit=0, sort=None):
        data = list(cls.db[collection].find({}, skip=offset, limit=limit, sort=sort))

        for row in data:
            if "_id" in row:
                row["uuid"] = row.pop("_id")

        return data

    @classmethod
    def get(cls, collection, identifier, key="_id"):
        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        data = cls.db[collection].find_one({key: identifier})
        if data:
            if "_id" in data:
                data["uuid"] = data.pop("_id")
            return data
        else:
            raise Http404Exception()

    @classmethod
    def getleftJoin(cls, collection, identifier, rightField, key="_id", projects=[]):
        data = cls._leftJoin(collection, identifier, rightField, key, projects)
        if data:
            data = data.pop()
            if "_id" in data:
                data["uuid"] = data.pop("_id")
            return data
        else:
            raise Http404Exception()

    @classmethod
    def getManyleftJoin(cls, collection, rightField, offset=0, limit=0, sort=None, projects=[]):
        pass

    @classmethod
    def getleftJoinMany(cls, collection, identifier, rightField, key="_id", projects=[]):
        pass

    @classmethod
    def getManyleftJoinMany(cls, collection, offset=0, limit=0, sort=None, projects=[]):
        pass

    @classmethod
    def _leftJoin(cls, collection, identifier, rightField, key="_id", projects=[]):
        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        pipeline = [
            {"$match": {key: identifier}},
            {"$lookup": {"from": rightField, "localField": rightField, "foreignField": "_id", "as": rightField}}
        ]
        for project in projects:
            pipeline.append({"$project": project})
        print(pipeline)

        data = list(cls.db[collection].aggregate(pipeline))

        if data:
            if "_id" in data:
                data["uuid"] = data.pop("_id")
            return data
        else:
            raise Http404Exception()

    @classmethod
    def post(cls, data, collection):
        try:
            return cls.db[collection].insert_one(data).inserted_id
        except errors.DuplicateKeyError:
            raise Http409Exception("Already registered")

    @classmethod
    def patch(cls, data, collection, identifier, key="_id"):
        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        cls.db[collection].update_one({key: identifier}, {'$set': data})

    @classmethod
    def patchMany(cls, data, collection, mongofilter):
        cls.db[collection].update_many(mongofilter, {'$set': data})

    @classmethod
    def put(cls, data, collection, identifier, key="_id"):
        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        cls.db[collection].replace_one({key: identifier}, data, True)

    @classmethod
    def delete(cls, collection, identifier, key="_id"):
        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        cls.db[collection].delete_one({key: identifier})

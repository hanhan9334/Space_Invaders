import pymongo
import config

client = pymongo.MongoClient(config.mongo_db_url)
db = client.space_invaders


def insertOneToDb(name, score):
    db.rankings.insert_one(
        {
            'name': name,
            'score': score
        }
    )


def getFivethRanking():
    rankings = db.rankings.find().sort("score", -1)
    fivthUser = rankings[4]
    return fivthUser


def getAllRankings():
    rankings = db.rankings.find().sort("score", -1)
    listNames = []
    listScores = []

    for ranking in rankings:
        listNames.append(ranking['name'])
        listScores.append(ranking['score'])

    print(listScores)
    print(listNames)
    return listNames, listScores


def saveScoreToDb(name, score):
    rankings = db.rankings.find()
    number = db.rankings.estimated_document_count()

    if number < 5:
        insertOneToDb(name, score)
        status = 1
    elif number >= 5:
        fivthUser = getFivethRanking()
        if int(fivthUser['score']) < score:
            status = 1
            db.rankings.update_one({"score": fivthUser['score']}, {
                                   "$set": {"name": name, "score": score}})


getAllRankings()

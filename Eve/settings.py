import os
from collections import OrderedDict
import bson



MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'books'

RECOURCE_METHODS = ['GET','POST']
ITEM_METHODS = ['GET','PATCH','PUT']

schema={
	'title': {
		'type': 'string'
	},
	'isbn': {
		'type': 'string'
	},
	'author': {
		'type': 'string'
	},
	'keywords': {
		'type': 'list'
	},
	'avg_rating': {
		'type': 'float'
	},
	'tropetags': {
		'type': 'list'
	},
	'genre': {
		'type': 'list'
	},
	'sentiment': {
		'type': 'string'
	},
	'imageURL': {
		'type': 'string'
	}
}


metadata={
	'schema': schema,
}

keysearch = {
	'datasource': {
		'source': 'metadata',
        'aggregation': {
            'pipeline': [
				{'$unwind' : "$keywords" },
				{'$match'  : {'keywords' : {'$in': '$keywordquery'} } },
				{'$group'  : {'_id':{"isbn":"$isbn", "title": "$title", "author": "$author", "imageURL":"$imageURL"}, 'numMatches': {'$sum':1} } },
				{'$match'  : {'numMatches' : {'$gt': 2} } },
				{"$sort": OrderedDict([("numMatches", -1), ("_id", -1)])}
            ]
        }
    }
}

tropesearch = {
	'datasource': {
		'source': 'metadata',
        'aggregation': {
            'pipeline': [
				{'$unwind' : "$tropetags" },
				{'$match'  : {'tropetags' : {'$in': '$tropetagquery'} } },
				{'$group'  : {'_id':{"isbn":"$isbn", "title": "$title", "author": "$author", "imageURL":"$imageURL"}, 'numMatches': {'$sum':1} } },
				{'$match'  : {'numMatches' : {'$gt': 2} } },
				{"$sort": OrderedDict([("numMatches", -1), ("_id", -1)])}
            ]
        }
    }
}


DOMAIN={'metadata':metadata,'keysearch':keysearch,'tropesearch':tropesearch}


X_DOMAINS = '*'
PAGINATION_DEFAULT = 50
	
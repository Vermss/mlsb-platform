'''
Name: Dallas Fraser
Date: 2016-04-12
Project: MLSB API
Purpose: Some random helper functions
'''
import unittest
from json import loads as loader


def loads(data):
    try:
        data = loader(data)
    except:
        data = loader(data.decode('utf-8'))
    return data

def pagination_response(pagination, route):
    """Returns a pagination repsonse that can be dump into json"""
    items = []
    for item in pagination.items:
        items.append(item.json())
    response = {}
    response['has_next'] = pagination.has_next
    response['has_prev'] = pagination.has_prev
    response['items'] = items
    
    response['next_url'] = (route + "?page={}".format(pagination.next_num)
                            if pagination.has_next
                            else None) 
    response['prev_url'] = (route + "?page={}".format(pagination.prev_num)
                            if pagination.has_prev
                            else None)
    response['total'] = pagination.total
    response['pages'] = pagination.pages
    return response


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testLoads(self):
        pass

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testLoads']
    unittest.main()

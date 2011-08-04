'''
Created on Jul 21, 2011

@author: papabear
'''
import unittest
import BizLayer
from Item import genPK
import json
from mock import Mock

class Test(unittest.TestCase):


    def setUp(self):
        self._bl = BizLayer.BizLayer()
        self._item1Review1 = "Nice place - 3x18 courses to choose from"
        self._item1Review2 = "visited on weekend. 45m wait for tee"
        self._item1 = {'name':"Far Corner Golf Course", 'category':"Recreational",'createdBy':"Ottodelupe", 
                      'address':"5 Barker Road, Boxford, MA", 'phone':"978 352 8300", 'descr':"Championship set of courses",
                      'url':"http://www.farcornergolf.com", 'email':"farcornergolfclub@comcast.net",
                      'lat':42.7288, 'lon':-71.0775,
                      'rating':"5", 'reviews':[self._item1Review1, self._item1Review2]}
        self._item1['pk'] = genPK(self._item1['name'], self._item1['category'])
        self._item1JsonRtn = {'pk': self._item1['pk'], 'name': self._item1['name'], 'category':self._item1['category'], 
                            'createdBy':self._item1['createdBy'], 'address':self._item1['address'], 'phone':self._item1['phone'],
                            'descr':self._item1['descr'], 'url':self._item1['url'], 'email':self._item1['email'],
                            'lat':self._item1['lat'], 'lon':self._item1['lon'], 'rating':self._item1['rating'],
                            'reviews':self._item1['reviews']}
        
        self._item2Review1 = "not bad for so close to civilization"
        self._item2Review2 = "lots of urban folks spoil the natural beauty"
        self._item2 = {'name':"Harold Parker State Forest", 'category':"Recreational", 'createdBy':"Ottodelupe", 
                      'address':"133 Jenkins Road, Andover, MA", 'phone':"978 686 3391", 
                      'lat':42.6129, 'lon':-71.0915, # per cargps, pkg lot at 42-36-47, -71-05-25
                      'url':"http://www.mass.gov/dcr/parks/northeast/harp.htm",
                      'descr':"Deep woods with many trails. Some camping sites available",
                      'rating':"4",
                      'reviews':[self._item2Review1, self._item2Review2]}
        self._item2['pk'] = genPK(self._item2['name'], self._item2['category'])
        self._item2JsonRtn = {'pk': self._item2['pk'], 'name': self._item2['name'], 'category':self._item2['category'], 
                            'createdBy':self._item2['createdBy'], 'address':self._item2['address'], 'phone':self._item2['phone'],
                            'descr':self._item2['descr'], 'url':self._item2['url'],
                            'lat':self._item2['lat'], 'lon':self._item2['lon'], 'rating':self._item2['rating'],
                            'reviews':self._item2['reviews']}

        
    def tearDown(self):
        pass


###
# Interface testing means seeing (1) if I get the right stuff out and
# second, do I get the right status codes when the wrong stuff goes in
###
    def testGetSingleItem(self):
        '''
        create a JSON that represents a search criteria, send it to the GET method,
        check to see that I get a valid json back. Send a bogus json. Do I get 
        pass
        
        create the dbconn mock, with expected return values, pass as optional
        arg to the biz layer get call. biz layer get uses the mock instead of 
        creating a real dbconn to read from
        '''
        jsonInput = '{\"pk\": \"%s\", \"name\": \"%s\", \"category\":\"%s\" , \"createdBy\":\"%s\" , \"address\":\"%s\"}' \
                % (self._item1['pk'], self._item1['name'], self._item1['category'], self._item1['createdBy'], self._item1['address'])
        dbConnMock = Mock()
        dbConnMock.read.return_value = [self._item1JsonRtn]
                
        rtnJson = self._bl.GET(jsonInput, dbConnMock)
        rtn = json.JSONDecoder().decode(rtnJson)
        self.assertEqual(rtn[0]['pk'], self._item1['pk'], "PK mismatch")
        self.assertEqual(rtn[0]['name'], self._item1['name'], "name mismatch")
        self.assertEqual(rtn[0]['category'], self._item1['category'], "category mismatch")
        self.assertEqual(rtn[0]['createdBy'], self._item1['createdBy'], "createdBy mismatch")
        self.assertEqual(rtn[0]['phone'], self._item1['phone'], "phone mismatch")
        self.assertEqual(rtn[0]['address'], self._item1['address'], "address mismatch")
        
    def testGetMultipleItems(self):
        '''
        json search criteria that will return multiple matches. Iterate over them to
        make sure valid json array comes back
        '''
        jsonInput = '{\"category\":\"%s\", \"lat\":%f, \"lon\":%f}' % ("Recreational", 42.7079, -71.1278)
        dbConnMock = Mock()
        dbConnMock.read.return_value = [self._item1JsonRtn, self._item2JsonRtn]
        
        rtnJson = self._bl.GET(jsonInput, dbConnMock)
        rtn = json.JSONDecoder().decode(rtnJson)
        for i in rtn:
            self.assertEqual(i['category'], "Recreational", "Categories don't match")
    
                                        
    def testGetReviews(self):
        '''
        json search criteria that returns single item, but that item has mulitple reviews
        Does the returned json have the right set of reviews?
        '''
        jsonInput = '{\"category\":\"%s\",\"name\":\"%s\"}' % (self._item1['category'], self._item1['name'])
        dbConnMock = Mock()
        dbConnMock.read.return_value = [self._item1JsonRtn]
        
        rtnJson = self._bl.GET(jsonInput, dbConnMock)
        rtn = json.JSONDecoder().decode(rtnJson)
        self.assertEqual(rtn[0]['reviews'][0], self._item1Review1, "mismatched review 1")
        self.assertEqual(rtn[0]['reviews'][1], self._item1Review2, "mismatched review 2")
        
    def testPut(self):
        '''
        PUT == Create
        Send a json that represents a new item
        Does the lat/lon get geocoded properly?
        If so, do a get and make sure that the returned json matches the json sent in
        '''
        # Used http://www.getaddress.net/ to do the geocoding of the below lat/lon
        # expectation is that geocoding is done on client side, and address plus lat/lon are
        # sent to server side when item is created.
        item = {'name':"Knox Stone NY19", 'category':"Historical", 'createdBy':"HenryKnox", 'lat':42.8014,
                'lon':-73.7336, 'address':"1258 Hwy 9, Cohoes, NY 12047, USA"}
        jsonInput = '{\"name\":\"%s\", \"category\":\"%s\", \"createdBy\":\"%s\", \"address\":\"%s\", \"lat\":%f, \"lon\":%f}' \
                % ("Knox Stone NY19", "Historical", "HenryKnox", "1258 Hwy 9, Cohoes, NY 12047, USA", 42.8014, -73.7336)     
        dbConnMock = Mock()
        dbConnMock.write.return_value = None
        
        # given that simpleDB is 'eventual consistency', doing the put and immediate get probably wouldn't work
        # for real. Given this is using mocks, probably OK.
        rtnJson = self._bl.PUT(jsonInput, dbConnMock)
        rtn = json.JSONDecoder().decode(rtnJson)
        # PK doesn't come back as part of the json. So compare name & category
        # Unlike get, which can return 1 or more items, put only returns 1
        self.assertEqual(rtn['name'], item['name'],"mismatched name: %s != %s" % (rtn['name'], item['name']))
        self.assertEqual(rtn['category'], item['category'],"mismatched category: %s != %s" % (rtn['category'], item['category']))
        self.assertEqual(rtn['address'], item['address'], "mismatched address: %s != %s" % (rtn['address'], item['address']))
        
        
    @unittest.skip("not yet implemented")
    def testPutExists(self):
        '''
        PUT == Create
        SEnd a json that represents an item that already exists
        Do we get back the right error code?
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testPutMultiple(self):
        '''
        Only allowed to PUT single items
        Do we get the right error code back if we try multples?
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testPost(self):
        '''
        Post == Update
        Send a json that has a PK entry and some updates (a new review and an updated phone number)
        Did the post return 200?
        If so, do a GET and see if the returned json has the updates reflected, and no other changes
        '''
        self.fail("not yet implemented")
    
    @unittest.skip("not yet implemented")    
    def testPostMultiple(self):
        '''
        Only allowed to POST single items
        Do we get the right error code back if we try multples?
        '''
        self.fail("not yet implemented")
    
    @unittest.skip("not yet implemented")
    def testDelete(self):
        '''
        Send a json that represents an existing item
        Do we get back a 200?
        If so, do a get and make sure that we get nullset back
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testDeleteDoesntExists(self):
        '''
        Send a json that represents an item that doesnt exist
        Do we get back the right error code?
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testDeleteMultiple(self):
        '''
        Only allowed to DELETE single items
        Do we get the right error code back if we try multples?
        '''
        self.fail("not yet implemented")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

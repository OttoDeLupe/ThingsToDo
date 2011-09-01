'''
Created on Jul 21, 2011

@author: papabear
'''
import unittest
import json
from mock import Mock
import Utils
from BizLayer import t2dApp
import os

# This will be imported by the biz Layer when testing.
# Will be set to a new Mock for every test by setUp()
# Set return values on a per-test basis.
dbConn = None 

# Set Test Mode, env checked on bizlayer side to determine
# whether to use the mock dbConn or a real one
os.environ['T2DTestMode'] ='true'


class BizLayerTest(unittest.TestCase):

    def ConvertTestDataToJson(self, testDataList):
        jsonData = []
        for d in testDataList:
            jsonData.append(d)
        return jsonData 
            
    def setUp(self):
        global dbConn  # needs to be global so can be imported by BizLayer when under test
        dbConn = Mock()
        self.testData = Utils.Utils();
        self.testJsonRtn = self.ConvertTestDataToJson(self.testData._testData)
        
    def tearDown(self):
        pass

  
    def testGetItemByKey(self):
        '''
        Provide a known good key. Do I get the right item values back?
        '''
        name = self.testData._testData[0]['name']
        pk = self.testData._testData[0]['pk']
        category = self.testData._testData[0]['category']
        createdBy = self.testData._testData[0]['createdBy']
        address = self.testData._testData[0]['address']
        phone = self.testData._testData[0]['phone']    

        dbConn.read.return_value = self.testJsonRtn[0]
        url = '/t2d/%s' % pk
        response = t2dApp.request(url)
        
        rtnJson = response.data
        self.assertEquals(response.headers['Content-Type'], 'text/plain')
        self.assertEquals(response.status, '200 OK')      
          
        rtn = json.JSONDecoder().decode(rtnJson)
        self.assertEqual(rtn['pk'],        pk, "PK mismatch")
        self.assertEqual(rtn['name'],      name, "name mismatch")
        self.assertEqual(rtn['category'],  category, "category mismatch")
        self.assertEqual(rtn['createdBy'], createdBy, "createdBy mismatch")
        self.assertEqual(rtn['phone'],     phone, "phone mismatch")
        self.assertEqual(rtn['address'],   address, "address mismatch")

    def testGetItemWithNonExistantResource(self):
        '''
        Provide a valid key where the resource doesn't exist. 
        Do I get the right status code?
        '''     
        dbConn.read.return_value = None
        url = '/t2d/foobar'
        response = t2dApp.request(url)
        self.assertEquals(response.status, '404 Not Found')      
   
    def testGetItemWithInvalidlyFormatedKey(self):
        '''
        try to get an item with a bogus key (one that is not of the right format)
        Do we get the proper status code back?
        '''
        url = '/t2d/#^%$@*&^!'
        response = t2dApp.request(url)
        self.assertEquals(response.status, '400 Bad Request')   
    
    def testGetItemWithMultipleReviews(self):
        '''
        get an item that has multiple reviews
        Does the returned json have the right set of reviews?
        '''
        pk = self.testData._testData[0]['pk']
        dbConn.read.return_value = self.testJsonRtn[0]
        url = '/t2d/%s' % pk
        response = t2dApp.request(url)
        
        rtnJson = response.data
        self.assertEquals(response.headers['Content-Type'], 'text/plain')
        self.assertEquals(response.status, '200 OK')      
          
        rtn = json.JSONDecoder().decode(rtnJson)
        self.assertEqual(rtn['review'][0], self.testData._testData[0]['review'][0], "mismatched review %s vs %s" % (rtn['review'][0], self.testData._testData[0]['review'][0]))
        self.assertEqual(rtn['review'][1], self.testData._testData[0]['review'][1], "mismatched review %s vs %s" % (rtn['review'][1], self.testData._testData[0]['review'][1]))
       
        
      
    def testGetMultipleItems(self):
        '''
        search criteria that will return multiple matches. Iterate over them to
        make sure what comes back is a list of items of the right category
        '''
        searchCriteria = '?category=Recreational&lat=42.7979&lon=-71.1278'
        url = '/t2dList%s' % searchCriteria
        dbConn.read.return_value = [self.testJsonRtn[0], self.testJsonRtn[1]]
        response = t2dApp.request(url)
        self.assertEquals(response.status, '200 OK')
        rtn = json.JSONDecoder().decode(response.data)
        for i in rtn:
            self.assertEqual(i['category'], "Recreational", "Categories don't match")
            
    def testGetZeroItems(self):
        '''
        search criteria that matches no items. Should get back an empty list
        with a OK status
        '''
        addr = self.testData._testData[2]['address']
        # The URL has a category and address. But the item at the address isn't
        # in the category. Hence, should return zero items
        url = '/t2dList?category=Recreational&address=%s' % addr
        dbConn.read.return_value = []
        response = t2dApp.request(url)
        self.assertEquals(response.status, '200 OK')
        rtn = json.JSONDecoder().decode(response.data)
        self.assertEqual(len(rtn), 0, "Incorrect number of items returned")
        
    def testGetOneItem(self):
        '''
        search criteria that matches a single item. Should get back a 
        list with one element that matches the item in question
        '''
        addr = self.testData._testData[2]['address']
        cat = self.testData._testData[2]['category']
        url = '/t2dList?category=%s&address=%s' % (cat, addr)
        dbConn.read.return_value = [self.testJsonRtn[2]]
        response = t2dApp.request(url)
        self.assertEquals(response.status, '200 OK')
        rtn = json.JSONDecoder().decode(response.data)
        self.assertEqual(len(rtn), 1, "Incorrect number of items returned")
        self.assertEqual(rtn[0]['address'], addr, "Addresses do not match")
        self.assertEqual(rtn[0]['category'], cat, "Categories do not match")
        
    def testGetMultipleItemsBogusCategory(self):
        '''
        Must pass in a valid category to search
        '''
        url = '/t2dList?category=foobar'
        response = t2dApp.request(url)
        self.assertEquals(response.status, '404 Not Found')
        
    def testGetMultipleItemsNoCategory(self):
        '''
        Gotta pass a category plus either lat/lon or address.
        If min params not satisfied, it's an error
        '''
        url = '/t2dList?lat=42.7979&lon=-71.1278'
        response = t2dApp.request(url)
        self.assertEquals(response.status, '400 Bad Request')
        
    def testGetMultipleItemsNoAddrLatLon(self):
        '''
        Gotta pass a category plus either lat/lon or address.
        If min params not satisfied, it's an error
        '''
        url = '/t2dList?category=Recreational'
        response = t2dApp.request(url)
        self.assertEquals(response.status, '400 Bad Request')
        
        
    def testPutMultipleItems(self):
        '''
        invalid to try to put more than 1 item
        '''
        response = t2dApp.request('/t2dList', 'PUT', "anythinggoeshere")
        self.assertEquals(response.status, '405 Method Not Allowed')
           
    def testPostMultipleItems(self):
        '''
        invalid to try to post more than 1 item
        '''
        response = t2dApp.request('/t2dList', 'POST', "anythinggoeshere")
        self.assertEquals(response.status, '405 Method Not Allowed')
    
    def testDeleteMultipleItems(self):
        '''
        invalid to try to delete more than 1 item
        '''
        response = t2dApp.request('/t2dList', 'DELETE', "anythinggoeshere")
        self.assertEquals(response.status, '405 Method Not Allowed')
        
"""   
                                   

    def testPut(self):
        '''
        PUT == Create
        Send a json that represents a new item
        If so, do a get and make sure that the returned json matches the json sent in
        '''
        # Used http://www.getaddress.net/ to do the geocoding of the below lat/lon
        # expectation is that geocoding is done on client side, and address plus lat/lon are
        # sent to server side when item is created.
        name = self.testData._testData[2]['name']
        category = self.testData._testData[2]['category']
        createdBy = self.testData._testData[2]['createdBy']
        address = self.testData._testData[2]['address']
        lat = float(self.testData._testData[2]['lat'])
        lon = float(self.testData._testData[2]['lon'])
        
        jsonInput = '{\"name\":\"%s\", \"category\":\"%s\", \"createdBy\":\"%s\", \"address\":\"%s\", \"lat\":%f, \"lon\":%f}' \
                % (name, category, createdBy, address, lat, lon)     
        dbConnMock = Mock()
        dbConnMock.write.return_value = None
        dbConnMock.read.return_value = None
        
        # given that simpleDB is 'eventual consistency', doing the put and immediate get probably wouldn't work
        # for real. Given this is using mocks, probably OK.
        rtnJson = self._bl.PUT(jsonInput, dbConnMock)
        rtn = json.JSONDecoder().decode(rtnJson)
        # PK doesn't come back as part of the json. So compare name & category
        # Unlike get, which can return 1 or more items, put only returns 1
        self.assertEqual(rtn['name'], name,"mismatched name: %s != %s" % (rtn['name'], name))
        self.assertEqual(rtn['category'], category,"mismatched category: %s != %s" % (rtn['category'], category))
        self.assertEqual(rtn['address'], address, "mismatched address: %s != %s" % (rtn['address'], address))
        
        

    def testPutExists(self):
        '''
        PUT == Create
        Trying to create an item that already exists is an error
        '''
        pk = self.testData._testData[0]['pk']
        name = self.testData._testData[0]['name']
        category = self.testData._testData[0]['category']
        createdBy = self.testData._testData[0]['createdBy']
        address = self.testData._testData[0]['address']
        jsonInput = '{\"pk\": \"%s\", \"name\": \"%s\", \"category\":\"%s\" , \"createdBy\":\"%s\" , \"address\":\"%s\"}' \
                % (pk, name, category, createdBy, address)
        dbConnMock = Mock()
        dbConnMock.read.return_value = [self.testJsonRtn[0]]
        dbConnMock.write.return_value = None
        
        self.assertRaises(AttributeError, self._bl.PUT, jsonInput, dbConnMock)
        
        



    def testPutMultiple(self):
        '''
        Only allowed to PUT single items
        Do we get the right error code back if we try multiples?
        '''
        self.fail("not yet implemented")

   
    def testPost(self):
        '''
        Post == Update
        Send a json that has a PK entry and some updates (a new review and an updated phone number)
        Did the post return 200?
        If so, do a GET and see if the returned json has the updates reflected, and no other changes
        '''
        self.fail("not yet implemented")
    
        
    def testPostMultiple(self):
        '''
        Only allowed to POST single items
        Do we get the right error code back if we try multples?
        '''
        self.fail("not yet implemented")
    
    
    def testDelete(self):
        '''
        Send a json that represents an existing item
        Do we get back a 200?
        If so, do a get and make sure that we get nullset back
        '''
        self.fail("not yet implemented")

    
    def testDeleteDoesntExists(self):
        '''
        Send a json that represents an item that doesnt exist
        Do we get back the right error code?
        '''
        self.fail("not yet implemented")

    
    def testDeleteMultiple(self):
        '''
        Only allowed to DELETE single items
        Do we get the right error code back if we try multples?
        '''
        self.fail("not yet implemented")
"""

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    t2dApp.run()
    unittest.main()

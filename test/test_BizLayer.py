'''
Created on Jul 21, 2011

@author: papabear
'''
import unittest
import os
import json
import logging

import Shared
from BizLayer import t2dApp
from mock import Mock
import Utils


 
# Set Test Mode, env checked on bizlayer side to determine
# whether to use the mock dbConn or a real one
os.environ['T2DTestMode'] ='true'
logging.basicConfig(filename="t2dLog.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')

class BizLayerTest(unittest.TestCase):
    """
    Main Use Case
    search based on lat/lon & optional category. Get a list of items w/in bounding box that match.
    Returned item data is a subset: PK, name, address, url, phone, rating, description.
    Select one of the items & drill down based on PK to get all item data
    """
    
    def ConvertTestDataToJson(self, testDataList):
        jsonData = []
        for d in testDataList:
            jsonData.append(d)
        return jsonData 
            
    def setUp(self):
        Shared.dbMock = Mock()
        self.testData = Utils.Utils();
        self.testJsonRtn = self.ConvertTestDataToJson(self.testData._testData)
        
    def tearDown(self):
        pass

  
    def testGetItemByKey(self):
        '''
        testGetItemByKey
        Provide a known good key. Do I get the right item values back?
        '''
        name = self.testData._testData[0]['name']
        pk = self.testData._testData[0]['pk']
        category = self.testData._testData[0]['category']
        createdBy = self.testData._testData[0]['createdBy']
        address = self.testData._testData[0]['address']
        phone = self.testData._testData[0]['phone']    

        Shared.dbMock.read.return_value = self.testJsonRtn[0]
        url = '/t2d/%s' % pk
        response = t2dApp.request(url) 
        
        rtnJson = response.data
        self.assertEquals(response.status, '200 OK')      
        self.assertEquals(response.headers['Content-Type'], 'text/plain')
          
        rtn = json.JSONDecoder().decode(rtnJson)
        self.assertEqual(rtn['pk'],        pk, "PK mismatch")
        self.assertEqual(rtn['name'],      name, "name mismatch")
        self.assertEqual(rtn['category'],  category, "category mismatch")
        self.assertEqual(rtn['createdBy'], createdBy, "createdBy mismatch")
        self.assertEqual(rtn['phone'],     phone, "phone mismatch")
        self.assertEqual(rtn['address'],   address, "address mismatch")
        
    def testGetItemWithNonExistantResource(self):
        '''
        testGetItemWithNonExistantResource
        Provide a valid key where the resource doesnt exist. 
        Do I get the right status code?
        '''     
        Shared.dbMock.read.return_value = None
        url = '/t2d/foobar'
        response = t2dApp.request(url)
        self.assertEquals(response.status, '404 Not Found')      
   
    def testGetItemWithInvalidlyFormatedKey(self):
        '''
        testGetItemWithInvalidlyFormatedKey
        try to get an item with a bogus key (one that is not of the right format)
        Do we get the proper status code back?
        '''
        url = '/t2d/#^%$@*&^!'
        response = t2dApp.request(url)
        self.assertEquals(response.status, '400 Bad Request')   
    
    def testGetItemWithMultipleReviews(self):
        '''
        testGetItemWithMultipleReviews
        get an item that has multiple reviews
        Does the returned json have the right set of reviews?
        '''
        pk = self.testData._testData[0]['pk']
        Shared.dbMock.read.return_value = self.testJsonRtn[0]
        url = '/t2d/%s' % pk
        response = t2dApp.request(url)
        
        rtnJson = response.data
        self.assertEquals(response.status, '200 OK')      
        self.assertEquals(response.headers['Content-Type'], 'text/plain')
          
        rtn = json.JSONDecoder().decode(rtnJson)
        self.assertEqual(rtn['review'][0], self.testData._testData[0]['review'][0], "mismatched review %s vs %s" % (rtn['review'][0], self.testData._testData[0]['review'][0]))
        self.assertEqual(rtn['review'][1], self.testData._testData[0]['review'][1], "mismatched review %s vs %s" % (rtn['review'][1], self.testData._testData[0]['review'][1]))
       
        
      
    def testGetMultipleItems(self):
        '''
        testGetMultipleItems
        search criteria that will return multiple matches. Iterate over them to
        make sure what comes back is a list of items of the right category
        '''
        searchCriteria = '?category=Recreational&lat=42.7979&lon=-71.1278'
        url = '/t2dList%s' % searchCriteria
        Shared.dbMock.read.return_value = [self.testJsonRtn[0], self.testJsonRtn[1]]
        response = t2dApp.request(url)
        self.assertEquals(response.status, '200 OK')
        rtn = json.JSONDecoder().decode(response.data)
        for i in rtn:
            self.assertEqual(i['category'], "Recreational", "Categories don't match")
            
    def testGetZeroItems(self):
        '''
        testGetZeroItems
        search criteria that matches no items. Should get back an empty list
        with a OK status
        '''
        addr = self.testData._testData[2]['address']
        # The URL has a category and address. But the item at the address isn't
        # in the category. Hence, should return zero items
        url = '/t2dList?category=Recreational&address=%s' % addr
        Shared.dbMock.read.return_value = []
        response = t2dApp.request(url)
        self.assertEquals(response.status, '200 OK')
        rtn = json.JSONDecoder().decode(response.data)
        self.assertEqual(len(rtn), 0, "Incorrect number of items returned")
        
    def testGetOneItem(self):
        '''
        testGetOneItem
        search criteria that matches a single item. Should get back a 
        list with one element that matches the item in question
        '''
        addr = self.testData._testData[2]['address']
        cat = self.testData._testData[2]['category']
        url = '/t2dList?category=%s&address=%s' % (cat, addr)
        Shared.dbMock.read.return_value = [self.testJsonRtn[2]]
        response = t2dApp.request(url)
        self.assertEquals(response.status, '200 OK')
        rtn = json.JSONDecoder().decode(response.data)
        self.assertEqual(len(rtn), 1, "Incorrect number of items returned")
        self.assertEqual(rtn[0]['address'], addr, "Addresses do not match")
        self.assertEqual(rtn[0]['category'], cat, "Categories do not match")
        
    def testGetMultipleItemsBogusCategory(self):
        '''
        testGetMultipleItemsBogusCategory
        Must pass in a valid category to search
        '''
        url = '/t2dList?category=foobar'
        response = t2dApp.request(url)
        self.assertEquals(response.status, '404 Not Found')
        
    def testGetMultipleItemsNoCategory(self):
        '''
        testGetMultipleItemsNoCategory
        Gotta pass a category plus either lat/lon or address.
        If min params not satisfied, its an error
        '''
        url = '/t2dList?lat=42.7979&lon=-71.1278'
        response = t2dApp.request(url)
        self.assertEquals(response.status, '400 Bad Request')
        
    def testGetMultipleItemsNoAddrLatLon(self):
        '''
        testGetMultipleItemsNoAddrLatLon
        Gotta pass a category plus either lat/lon or address.
        If min params not satisfied, its an error
        '''
        url = '/t2dList?category=Recreational'
        response = t2dApp.request(url)
        self.assertEquals(response.status, '400 Bad Request')
        
        
    def testPutMultipleItems(self):
        '''
        testPutMultipleItems
        invalid to try to put more than 1 item
        '''
        response = t2dApp.request('/t2dList', method='PUT', data="anythinggoeshere")
        self.assertEquals(response.status, '405 Method Not Allowed')
           
    def testPostMultipleItems(self):
        '''
        testPostMultipleItems
        invalid to try to post more than 1 item
        '''
        response = t2dApp.request('/t2dList', method='POST', data="anythinggoeshere")
        self.assertEquals(response.status, '405 Method Not Allowed')
    
    def testDeleteMultipleItems(self):
        '''
        testDeleteMultipleItems
        invalid to try to delete more than 1 item
        '''
        response = t2dApp.request('/t2dList', method='DELETE', data="anythinggoeshere")
        self.assertEquals(response.status, '405 Method Not Allowed')

    def testPutNewItem(self):
        '''
        testPutNewItem
        PUT == Create
        Try to add a new item to the app.
        Expectation is that geocoding is done on client side so that
        both lat/lon and address are provided in the submission
        '''
        name = 'Morse Parker House'
        category = 'Historical'
        createdBy = 'Mr Morse'
        address = '104 Washington Street, Boxford, MA 01921'
        lat = 42.713 # 42-42.775
        lon = -71.053 # -71-03.208
        jsonInput = '{\"name\":\"%s\", \"category\":\"%s\", \"createdBy\":\"%s\", \"address\":\"%s\", \"lat\":%f, \"lon\":%f}' \
                    % (name, category, createdBy, address, lat, lon)
        Shared.dbMock.write.return_value = None
        Shared.dbMock.read.return_value = None
        url = '/t2d/'
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEquals(response.status, '200 OK')      

    def testPutEmptyItem(self):
        jsonInput = ''
        url = '/t2d/'
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEquals(response.status, '400 Bad Request')
        
    def testPutItemMissingRequiredAttributes(self):
        '''
        testPutItemMissingRequiredAttributes
        Make sure that if we dont supply name, category and createdBy,
        that we get the right error code
        '''
        address = '104 Washington Street, Boxford, MA 01921'
        lat = 42.713 # 42-42.775
        lon = -71.053 # -71-03.208
        jsonInput = '{\"address\":\"%s\", \"lat\":%f, \"lon\":%f}' % (address, lat, lon)
        Shared.dbMock.write.return_value = None
        Shared.dbMock.read.return_value = None
        url = '/t2d/'
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEquals(response.status, '400 Bad Request')

    def testPutItemMissingLocation(self):
        '''
        testPutItemMissingLocation
        One of address or lat/lon is required in addition to name, category, createdBy
        '''
        name = 'Morse Parker House'
        category = 'Historical'
        createdBy = 'Mr Morse'
        jsonInput = '{\"name\":\"%s\", \"category\":\"%s\", \"createdBy\":\"%s\"}' \
                    % (name, category, createdBy)
        Shared.dbMock.write.return_value = None
        Shared.dbMock.read.return_value = None
        url = '/t2d/'
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEquals(response.status, '400 Bad Request')      

    def testPutItemWithJustLatLon(self):
        '''
        testPutItemWithJustLatLon
        Should be able to create an item with only Lat/Lon in addition to
        required name, category and createdBy
        '''
        name = 'Morse Parker House'
        category = 'Historical'
        createdBy = 'Mr Morse'
        lat = 42.713 # 42-42.775
        lon = -71.053 # -71-03.208
        jsonInput = '{\"name\":\"%s\", \"category\":\"%s\", \"createdBy\":\"%s\", \"lat\":%f, \"lon\":%f}' \
                    % (name, category, createdBy, lat, lon)
        Shared.dbMock.write.return_value = None
        Shared.dbMock.read.return_value = None
        url = '/t2d/'
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEquals(response.status, '200 OK')

    def testPutItemWithJustAddress(self):
        '''
        testPutItemWithJustAddress
        Should be able to create an item with only Address in addition to
        required name, category and createdBy
        '''
        name = 'Morse Parker House'
        category = 'Historical'
        createdBy = 'Mr Morse'
        address = '104 Washington Street, Boxford, MA 01921'
        jsonInput = '{\"name\":\"%s\", \"category\":\"%s\", \"createdBy\":\"%s\", \"address\":\"%s\"}' \
                    % (name, category, createdBy, address)
        Shared.dbMock.write.return_value = None
        Shared.dbMock.read.return_value = None
        url = '/t2d/'
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEquals(response.status, '200 OK')

    def testPutItemWithNoAddressAndMissingLon(self):
        '''
        testPutItemWithNoAddressAndMissingLon
        If no address, and specifying a lat/lon, need to have both the lat and lon
        '''
        name = 'Morse Parker House'
        category = 'Historical'
        createdBy = 'Mr Morse'
        lat = 42.713 # 42-42.775
        jsonInput = '{\"name\":\"%s\", \"category\":\"%s\", \"createdBy\":\"%s\", \"lat\":%f}' \
                    % (name, category, createdBy, lat)
        Shared.dbMock.write.return_value = None
        Shared.dbMock.read.return_value = None
        url = '/t2d/'
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEquals(response.status, '400 Bad Request')      

    def testPutItemInvalidCategory(self):
        '''
        testPutItemInvalidCategory
        Even if all required args are there, a valid category must be sent
        '''
        name = 'Morse Parker House'
        category = 'Nonsensical'
        createdBy = 'Mr Morse'
        address = '104 Washington Street, Boxford, MA 01921'
        jsonInput = '{\"name\":\"%s\", \"category\":\"%s\", \"createdBy\":\"%s\", \"address\":\"%s\"}' \
                    % (name, category, createdBy, address)
        Shared.dbMock.write.return_value = None
        Shared.dbMock.read.return_value = None
        url = '/t2d/'
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEquals(response.status, '400 Bad Request')      
        
        
    def testPutAlreadyExistingItem(self):
        '''
        testPutAlreadyExistingItem
        Cant create an item that already exists. Can only update (ie POST) it
        '''
        name = self.testData._testData[0]['name']
        category = self.testData._testData[0]['category']
        createdBy = self.testData._testData[0]['createdBy']
        address = self.testData._testData[0]['address']
        jsonInput = '{\"name\":\"%s\", \"category\":\"%s\", \"createdBy\":\"%s\", \"address\":\"%s\"}' \
                    % (name, category, createdBy, address)
        Shared.dbMock.read.return_value = None
        Shared.dbMock.write.return_value = None
        url = '/t2d/'
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEquals(response.status, '200 OK')
        # Now that its there, try putting it in again. This should fail
        Shared.dbMock.read.return_value = self.testJsonRtn[0]
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEquals(response.status, '409 Conflict')
        
    def testPostUpdateExistingItem(self):
        '''
        testPostUpdateExistingItem
        As post updates an already existing item, there dont have to be checks on
        required args. Just update existing fields or add new ones
        In this case, add a new review and make sure that we get all the reviews back
        '''
        # Put (Create) an item
        name = self.testData._testData[7]['name']
        pk = self.testData._testData[7]['pk']
        category = self.testData._testData[7]['category']
        createdBy = self.testData._testData[7]['createdBy']
        address = self.testData._testData[7]['address']
        jsonInput = '{\"name\":\"%s\", \"category\":\"%s\", \"createdBy\":\"%s\", \"address\":\"%s\"}' \
                    % (name, category, createdBy, address)
        Shared.dbMock.write.return_value = None
        Shared.dbMock.read.return_value = None
        url = '/t2d/'
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEqual(response.status, '200 OK', 'PUT failed')

        # now update it
        Shared.dbMock.read.return_value = self.testJsonRtn[7]
        jsonInput = '{\"pk\":\"%s\", \"review\":\"%s\"}' \
                    % (pk, self.testData._testData[7]['review'][0])
        response = t2dApp.request(url, method='POST', data=jsonInput)
        self.assertEqual(response.status, '200 OK', 'POST failed (received %s)' % response.status)

        # now read it back to be sure the update took.
        Shared.dbMock.read.return_value = self.testJsonRtn[7]
        url = '/t2d/%s' % pk
        response = t2dApp.request(url)
        rtnJson = response.data
        self.assertEqual(response.status, '200 OK', 'GET failed')
        self.assertEquals(response.headers['Content-Type'], 'text/plain')
          
        rtn = json.JSONDecoder().decode(rtnJson)
        self.assertEqual(rtn['review'][0], self.testData._testData[7]['review'][0], "mismatched review %s vs %s" % (rtn['review'][0], self.testData._testData[7]['review'][0]))

    def testPostUpdateNonExistingItem(self):
        '''
        testPostUpdateNonExistingItem
        Try to update a non-existing item. It should get a 404
        '''
        pk = self.testData._testData[7]['pk']
        Shared.dbMock.read.return_value = None
        url = '/t2d/'
        jsonInput = '{\"pk\":\"%s\", \"review\":\"%s\"}' \
                    % (pk, self.testData._testData[7]['review'][0])
        response = t2dApp.request(url, method='POST', data=jsonInput)
        self.assertEqual(response.status, '404 Not Found', 'POST failed (received %s)' % response.status)

    def testPostUpdateWithNewFields(self):
        '''
        testPostUodateWithNewFields
        Try to update an existing item with new columns
        Should fail with a 400
        '''
        # Put (Create) an item
        name = self.testData._testData[7]['name']
        pk = self.testData._testData[7]['pk']
        category = self.testData._testData[7]['category']
        createdBy = self.testData._testData[7]['createdBy']
        address = self.testData._testData[7]['address']
        jsonInput = '{\"name\":\"%s\", \"category\":\"%s\", \"createdBy\":\"%s\", \"address\":\"%s\"}' \
                    % (name, category, createdBy, address)
        Shared.dbMock.write.return_value = None
        Shared.dbMock.read.return_value = None
        url = '/t2d/'
        response = t2dApp.request(url, method='PUT', data=jsonInput)
        self.assertEqual(response.status, '200 OK', 'PUT failed')

        # now update it
        Shared.dbMock.read.return_value = self.testJsonRtn[7]
        jsonInput = '{\"pk\":\"%s\", \"ARandomKey\":\"%s\"}' % (pk, 'random key value data')
        response = t2dApp.request(url, method='POST', data=jsonInput)
        self.assertEqual(response.status, '400 Bad Request', 'POST failed (received %s)' % response.status)
    
    def testDelete(self):
        '''
        testDelete
        Try to delete an existing resource. Do we get back a 200?
        If so, try to do a get - do we get a 404?
        '''
        pk = self.testData._testData[0]['pk']
        Shared.dbMock.read.return_value = None
        Shared.dbMock.delete.return_value = None
        url = '/t2d/%s' % pk
        response = t2dApp.request(url, method='DELETE')
        self.assertEquals(response.status, '200 OK')      
        response = t2dApp.request(url)  # GET
        self.assertEquals(response.status, '404 Not Found')

    def testDeleteWithInvalidlyFormatedKey(self):
        '''
        testDeleteWithInvalidlyFormatedKey
        try to delete an item with a bogus key (one that is not of the right format)
        Do we get the proper status code back?
        '''
        url = '/t2d/#^%$@*&^!'
        response = t2dApp.request(url, method='DELETE')
        self.assertEquals(response.status, '400 Bad Request')   

    def testDeleteWithMissingResource(self):
        '''
        testDeleteWithMissingResource
        Try to delete an item that doesnt exist
        Do we get a 404 back?
        '''
        pk = self.testData._testData[0]['pk']
        Shared.dbMock.delete.return_value = None
        url = '/t2d/%s' % pk
        response = t2dApp.request(url, method='DELETE')
        self.assertEquals(response.status, '200 OK')      
        # Now try to delete it again. Should get a 404
        Shared.dbMock.delete.side_effect = AttributeError('Key Not Found')
        response = t2dApp.request(url, method='DELETE')
        self.assertEquals(response.status, '404 Not Found')

    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #logging.basicConfig(filename="t2dLog.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')
    t2dApp.run()
    unittest.main()

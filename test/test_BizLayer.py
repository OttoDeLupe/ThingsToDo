'''
Created on Jul 21, 2011

@author: papabear
'''
import unittest
import BizLayer
import json
from mock import Mock
import Utils

class Test(unittest.TestCase):

    def ConvertTestDataToJson(self, testDataList):
        jsonData = []
        for d in testDataList:
            jsonData.append(d)
        return jsonData 
            
    def setUp(self):
        self._bl = BizLayer.BizLayer()
        self.testData = Utils.Utils();
        self.testJsonRtn = self.ConvertTestDataToJson(self.testData._testData)
        
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
        name = self.testData._testData[0]['name']
        pk = self.testData._testData[0]['pk']
        category = self.testData._testData[0]['category']
        createdBy = self.testData._testData[0]['createdBy']
        address = self.testData._testData[0]['address']
        phone = self.testData._testData[0]['phone']
        
        jsonInput = '{\"pk\": \"%s\", \"name\": \"%s\", \"category\":\"%s\" , \"createdBy\":\"%s\" , \"address\":\"%s\"}' \
                % (pk, name, category , createdBy, address)
        dbConnMock = Mock()
        dbConnMock.read.return_value = [self.testJsonRtn[0]]
                
        rtnJson = self._bl.GET(jsonInput, dbConnMock)
        rtn = json.JSONDecoder().decode(rtnJson)
        self.assertEqual(rtn[0]['pk'],        pk, "PK mismatch")
        self.assertEqual(rtn[0]['name'],      name, "name mismatch")
        self.assertEqual(rtn[0]['category'],  category, "category mismatch")
        self.assertEqual(rtn[0]['createdBy'], createdBy, "createdBy mismatch")
        self.assertEqual(rtn[0]['phone'],     phone, "phone mismatch")
        self.assertEqual(rtn[0]['address'],   address, "address mismatch")
        
    def testGetMultipleItems(self):
        '''
        json search criteria that will return multiple matches. Iterate over them to
        make sure valid json array comes back
        '''
        jsonInput = '{\"category\":\"%s\", \"lat\":%f, \"lon\":%f}' % ("Recreational", 42.7079, -71.1278)
        dbConnMock = Mock()
        dbConnMock.read.return_value = [self.testJsonRtn[0], self.testJsonRtn[1]]
        
        rtnJson = self._bl.GET(jsonInput, dbConnMock)
        rtn = json.JSONDecoder().decode(rtnJson)
        for i in rtn:
            self.assertEqual(i['category'], "Recreational", "Categories don't match")
    
                                        
    def testGetReviews(self):
        '''
        json search criteria that returns single item, but that item has mulitple reviews
        Does the returned json have the right set of reviews?
        '''
        category = self.testData._testData[0]['category']
        name = self.testData._testData[0]['name']
        jsonInput = '{\"category\":\"%s\",\"name\":\"%s\"}' % (category, name)
        dbConnMock = Mock()
        dbConnMock.read.return_value = [self.testJsonRtn[0]]
        
        rtnJson = self._bl.GET(jsonInput, dbConnMock)
        rtn = json.JSONDecoder().decode(rtnJson)
        self.assertEqual(rtn[0]['review'][0], self.testData._testData[0]['review'][0], "mismatched review %s vs %s" % (rtn[0]['review'][0], self.testData._testData[0]['review'][0]))
        self.assertEqual(rtn[0]['review'][1], self.testData._testData[0]['review'][1], "mismatched review %s vs %s" % (rtn[0]['review'][1], self.testData._testData[0]['review'][1]))
        
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
        
        


"""   
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
    unittest.main()

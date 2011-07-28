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
        item_name = "Far Corner Golf Course"
        item_category = "Recreational"
        item_pk = genPK(item_name, item_category)
        item_createdby = "Ottodelupe"
        item_address = "5 Barker Road, Boxford, MA"
        item_phone = "978 352 8300"
        dbConnMock = Mock()
        dbConnMock.read.return_value = [{'pk': item_pk, 'name': item_name, 'category':item_category, 'createdBy':item_createdby, 'address':item_address, 'phone':item_phone}]
        jsonStr = '{\"pk\": \"%s\", \"name\": \"%s\", \"category\":\"%s\" , \"createdBy\":\"%s\" , \"address\":\"%s\"}' % (item_pk, item_name, item_category, item_createdby, item_address)
        rtnJson = self._bl.GET(jsonStr, dbConnMock)
        rtn = json.JSONDecoder().decode(rtnJson)
        self.assertEqual(rtn[0]['pk'], item_pk)
        self.assertEqual(rtn[0]['name'], item_name)
        self.assertEqual(rtn[0]['category'], item_category)
        self.assertEqual(rtn[0]['createdBy'], item_createdby)
        self.assertEqual(rtn[0]['address'], item_address)
        self.assertEqual(rtn[0]['phone'], item_phone)
        
    def testGetMultipleITems(self):
        '''
        json search criteria that will return multiple matches. Iterate over them to
        make sure valid json array comes back
        '''
        pass

    def testGetReviews(self):
        '''
        json search criteria that returns single item, but that item has mulitple reviews
        Does the returned json have the right set of reviews?
        '''
        pass

    def testGetReturns404(self):
        '''
        make sure that when accessing a bogus resource, we get back a 404
        '''

    def testGetReturns400(self):
        '''
        make sure that under the right conditions we get back a 400
        '''
        pass

    def testGetReturns500(self):
        '''
        make sure that under the right conditions we get back a 500
        '''
        pass

    def testPost(self):
        '''
        Post == Update
        Send a json that has a PK entry and some updates (a new review and an updated phone number)
        Did the post return 200?
        If so, do a GET and see if the returned json has the updates reflected, and no other changes
        '''

    def testPostMultiple(self):
        '''
        Only allowed to POST single items
        Do we get the right error code back if we try multples?
        '''
        pass
    
    def testPostReturns404(self):
        '''
        make sure that when accessing a bogus resource, we get back a 404
        '''

    def testPostReturns400(self):
        '''
        make sure that under the right conditions we get back a 400
        '''
        pass

    def testpostReturns500(self):
        '''
        make sure that under the right conditions we get back a 500
        '''
        pass

    def testPut(self):
        '''
        PUT == Create
        Send a json that represents a new item
        Do we get back a 200?
        If so, do a get and make sure that the returned json matches the json sent in
        '''
        pass

    def testPutExists(self):
        '''
        PUT == Create
        SEnd a json that represents an item that already exists
        Do we get back the right error code?
        '''
        pass

    def testPutMultiple(self):
        '''
        Only allowed to PUT single items
        Do we get the right error code back if we try multples?
        '''
        pass

    def testPutReturns404(self):
        '''
        make sure that when accessing a bogus resource, we get back a 404
        '''

    def testPutReturns400(self):
        '''
        make sure that under the right conditions we get back a 400
        '''
        pass

    def testPutxsReturns500(self):
        '''
        make sure that under the right conditions we get back a 500
        '''
        pass

    def testDelete(self):
        '''
        Send a json that represents an existing item
        Do we get back a 200?
        If so, do a get and make sure that we get nullset back
        '''
        pass

    def testDeleteDoesntExists(self):
        '''
        Send a json that represents an item that doesnt exist
        Do we get back the right error code?
        '''
        pass

    def testDeleteMultiple(self):
        '''
        Only allowed to DELETE single items
        Do we get the right error code back if we try multples?
        '''
        pass

    def testDeleteReturns404(self):
        '''
        make sure that when accessing a bogus resource, we get back a 404
        '''

    def testDeleteReturns400(self):
        '''
        make sure that under the right conditions we get back a 400
        '''
        pass

    def testDeleteReturns500(self):
        '''
        make sure that under the right conditions we get back a 500
        '''
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

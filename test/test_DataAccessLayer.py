'''
Created on Jun 27, 2011

@author: papabear
'''
import unittest
import DataAccessLayer
import Item
import sys
import boto
import Utils

class DALTestCase(unittest.TestCase):
    def setUp(self):
        '''
        create and populate the store - this actually tests the write calls
        '''
        self._testDAL = DataAccessLayer.DataAccessLayer()
        self.assertTrue(self._testDAL)
        self.testData = Utils.Utils();
        
        otherArgs = {}
        try:
            for i in self.testData._testData:      
                name = i['name']
                createdBy = i['createdBy']
                category = i['category']
    
                if 'phone' in i:
                    otherArgs['phone'] = i['phone']
                if 'address' in i:
                    otherArgs['address'] = i['address']
                if 'url' in i:
                    otherArgs['url'] = i['url']
                if 'email' in i:
                    otherArgs['email'] = i['email']
                if 'rating' in i:
                    otherArgs['rating'] = i['rating']
                if 'review' in i:
                    otherArgs['review'] = i['review']
                if 'descr' in i:
                    otherArgs['descr'] = i['descr']
                if 'lat' in i and 'lon' in i:
                    ll = Item.LatLon(i['lat'], i['lon'])
                    otherArgs['latlon'] = ll
    
                item = Item.ThingToDo()
                item.setAttrs(name, category, createdBy, **otherArgs)
                self._testDAL.write(item._serialized)

        except Exception as ex:
            print 'problem in setup - ', ex
        
    def tearDown(self):
        '''
        Clean out the persistence store so that we dont leave cruft behind
        this actually tests the delete calls
        '''
        try:
            for i in self.testData._testData:
                self._testDAL.delete(i['pk'])
        except Exception as ex:
            print 'problem in teardown - ', ex
        finally:
            self._testDAL = None
            self._testItems = None
  
        
        
         
        
###
# Requirement: read a single item from the persistence store given some query criteria
#     The criteria is a single name-value pair to be matched
###
    def test_readSingleItem(self):
        '''
        test_readSingleItem
        read from the persistence store using the given criteria that should select a single item
        if more than one item returned, fail
        if returned item does not match the supplied criteria, fail
        '''
        searchFor = Item.SearchFor()
        searchFor.setAttr('name', "Far Corner Golf Course")
        searchFor.setAttr('category', "Recreational")
        searchFor.setAttr('createdBy', "Ottodelupe")
        searchFor.setAttr('address', "5 Barker Road, Boxford, MA")
        where = searchFor.makeWhereClause()
        try:
            rtn = self._testDAL.read(where)
        except Exception as ex:
            print 'unable to read from persistence store - ', ex
        
        self.assertEqual(len(rtn), 1, 'returned more than one item')
        self.assertEqual(rtn[0]['name'], "Far Corner Golf Course")
        self.assertEqual(rtn[0]['category'], "Recreational")
        self.assertEqual(rtn[0]['createdBy'], "Ottodelupe")
        self.assertEqual(rtn[0]['address'], "5 Barker Road, Boxford, MA")
            
            
###
# Requirement: read a list of items from the persistence store given some query criteria
#    The criteria is a list of name-value pairs to match
###
    def test_readMultipleItemsFromCategory(self):
        '''
        test_readMultipleItemsFromCategory
        read from the persistence store using given criteria
        may return zero or more items
        each returned item must match the supplied criteria, otherwise, fail
        '''
        searchFor = Item.SearchFor()
        searchFor.setAttr('category', "Recreational")
        where = searchFor.makeWhereClause()
        
        try:
            rtn = self._testDAL.read(where)
        except Exception as ex:
            print 'unable to read from persistence store -', ex
        
        for i in rtn:
            self.assertEqual(i['category'], "Recreational", 'returned item does not match')
        
        
    def test_readMultipleItemsFromLatLon(self):
        '''
        test_readMultipleItemsFromLatLon
        '''
        ll = Item.LatLon(42.69095, -71.1277)
        searchFor = Item.SearchFor()
        searchFor.setAttr('latlon', ll)
        searchFor.setAttr('offset', 10)
        where = searchFor.makeWhereClause()
        try:
            rtn = self._testDAL.read(where)
        except Exception as ex:
            print 'unable to read from persistence store -', ex
        
        for i in rtn:
            self.assertEqual(i, searchFor, 'returned item does not match')
        
        
    def test_readItemsBogusCriteria(self):
        '''
        test_readItemsBogusCriteria
        read from the store using bogus criteria (should match zero items)
        confirm proper exception generated
            '''
        searchFor = Item.SearchFor()
        searchFor.setAttr('category', "FooBar")
        where = searchFor.makeWhereClause()
        
        try:
            rtn = self._testDAL.read(where)
        except Exception as ex:
            print 'unable to read from persistence store -', ex
        
        self.assertFalse(rtn)

    def test_deleteNonExistantItem(self):
        '''
        test_deleteNonExistantItem
        Try to delete an item that doesnt exist.
        Make sure we get the right exception raised
        '''
        self.assertRaises(AttributeError, self._testDAL.delete, '33616161-6262-6263-6363-646464656565')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

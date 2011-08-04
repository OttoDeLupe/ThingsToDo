'''
Created on Jun 27, 2011

@author: papabear
'''
import unittest
import DataAccessLayer
import Item
import sys
import boto

class DALTestCase(unittest.TestCase):
    def setUp(self):
        '''
        create and populate the store - this actually tests the write calls
        '''
        self._testDAL = DataAccessLayer.DataAccessLayer()
        self.assertTrue(self._testDAL)
        self.generateTestItems()
        
        try:
            for i in self._testItems:
                self._testDAL.write(i._pk, i._serialized)
        except:
            print "problem in setup - %s" % sys.exc_info()[0]
        
    def tearDown(self):
        '''
        Clean out the persistence store so that we dont leave cruft behind
        this actually tests the delete calls
        '''
        try:
            for i in self._testItems:
                self._testDAL.delete(i._pk)
        except:
            print "problem in teardown - %s" % sys.exc_info()[0]
        finally:
            self._testDAL = None
            self._testItems = None
    
    def generateTestItems(self):
        self._testItems = []
        i = Item.ThingToDo()
        i.setAttrs("Weir Hill", "Recreational", "Ottodelupe",
                    **{'address':"Stevens Street North Andover, MA"})
        self._testItems.append(i)
        
        i = Item.ThingToDo()
        i.setAttrs("Stevens-Coolidge Place", "Historical", "Ottodelupe",
                    **{'address':"137 Andover Street, North Andover, MA",
                       'url':"http://www.thetrustees.org/places-to-visit/northeast-ma/stevens-coolidge-place.html",
                       'phone':"978.682.3580",
                       'email':"neregion@ttor.org"})
        self._testItems.append(i)
        
        i = Item.ThingToDo()
        i.setAttrs("Museum of Printing", "Cultural", "Ottodelupe",
                    **{'url':"http://www.museumofprinting.org/",
                       'phone':"978 686 0450",
                       'address':"800 Massachusetts Ave, North Andover, MA"})
        self._testItems.append(i)
        
        i = Item.ThingToDo()
        i.setAttrs("North Andover Historical Society", "Historical", "Ottodelupe",
                    **{'url':"http://www.northandoverhistoricalsociety.org/",
                       'phone':"978-686-4035",
                       'address':"153 Academy Road, North Andover, MA"})
        self._testItems.append(i)
        
        i = Item.ThingToDo()
        i.setAttrs("Harold Parker State Forest", "Recreational", "Ottodelupe",
                    **{'address':"133 Jenkins Road, Andover, MA",
                       'phone':"978 686 3391",
                       'latlon':Item.LatLon(42.6129, -71.0915),
                       'url':"http://www.mass.gov/dcr/parks/northeast/harp.htm"})
        self._testItems.append(i)
        
        i = Item.ThingToDo()
        i.setAttrs("Ward Reservation", "Recreational", "Ottodelupe",
                    **{'url':"http://www.thetrustees.org/places-to-visit/northeast-ma/ward-reservation.html",
                       'latlon':Item.LatLon(42.6405, -71.1120),
                       'phone':"978 682 3580",
                       'email':"neregion@ttor.org"})
        self._testItems.append(i)
        
        i = Item.ThingToDo()
        i.setAttrs("Old Burying Ground", "Historical", "Ottodelupe",
                    **{'latlon':Item.LatLon(42.688, -71.116),
                       'address':"Academy Road, North Andover, MA"})
        self._testItems.append(i)
        
        i = Item.ThingToDo()
        i.setAttrs("Far Corner Golf Course", "Recreational", "Ottodelupe",
                   **{'address':"5 Barker Road, Boxford, MA",
                      'url':"http://www.farcornergolf.com",
                      'phone':"978 352 8300"})
        self._testItems.append(i)


        
        
         
        
###
# Requirement: read a single item from the persistence store given some query criteria
#     The criteria is a single name-value pair to be matched
###
    def test_readSingleItem(self):
        '''
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
        except:
            print "unable to read from persistence store - %s" % sys.exc_info()[0]
        
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
        read from the persistence store using given criteria
        may return zero or more items
        each returned item must match the supplied criteria, otherwise, fail
        '''
        searchFor = Item.SearchFor()
        searchFor.setAttr('category', "Recreational")
        where = searchFor.makeWhereClause()
        
        try:
            rtn = self._testDAL.read(where)
        except:
            print "unable to read from persistence store - %s" % sys.exc_info()[0]
        
        for i in rtn:
            self.assertEqual(i['category'], "Recreational", 'returned item does not match')
        
        
    def test_readMultipleItemsFromLatLon(self):
        ll = Item.LatLon(42.69095, -71.1277)
        searchFor = Item.SearchFor()
        searchFor.setAttr('latlon', ll)
        searchFor.setAttr('offset', 10)
        where = searchFor.makeWhereClause()
        try:
            rtn = self._testDAL.read(where)
        except:
            print "unable to read from persistence store - %s" % sys.exc_info()[0]
        
        for i in rtn:
            self.assertEqual(i, searchFor, 'returned item does not match')
        
        
    def test_readItemsBogusCriteria(self):
        '''
        read from the store using bogus criteria (should match zero items)
        confirm proper exception generated
            '''
        searchFor = Item.SearchFor()
        searchFor.setAttr('category', "FooBar")
        where = searchFor.makeWhereClause()
        
        try:
            rtn = self._testDAL.read(where)
        except:
            print "unable to read from persistence store - %s" % sys.exc_info()[0]
        
        self.assertFalse(rtn)
                                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

'''
Created on Jun 28, 2011

@author: papabear
'''
import unittest
import Item
import sys
import Utils
import uuid
#import DataAccessLayer

class ItemTest(unittest.TestCase):
    _dbConn = None

    def setUp(self):
        _dbConn = None
        self.testData = Utils.Utils();


    def tearDown(self):
        _dbConn = None

###
# Requirement: Able to instantiate an item when minimum attributes specified
# - Name
# - createdBy
# - One of Address or Lat/Lon (to support Geocoding)
# - Category
###
    def testInstantiateItemWithAddress(self):
        '''
        testInstantiateItemWithAddress
        '''
        name = self.testData._testData[3]['name']
        createdBy = self.testData._testData[3]['createdBy']
        category = self.testData._testData[3]['category']
        otherArgs = {'address':self.testData._testData[3]['address']}
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,**otherArgs)

        except AssertionError:
            self.fail("Assertion Error creating Item")
        except:
            self.fail("problem creating item - %s" % sys.exc_info()[0]) 
        
        self.assertEquals(item.getName(), name, "names don't match: %s != %s" % (item.getName(), name))
        self.assertEquals(item.getCategory(), category, "categories don't match: %s != %s" % (item.getCategory(), category))
        self.assertEquals(item.getAddress(), otherArgs['address'], "addresses don't match: %s != %s" % (item.getAddress(), otherArgs['address']))
        
    def testInstantiateItemWithLatLon(self):
        '''
        testInstantiateItemWithLatLon
        '''
        ll = Item.LatLon(self.testData._testData[3]['lat'], self.testData._testData[3]['lon'])
        name = self.testData._testData[3]['name']
        createdBy = self.testData._testData[3]['createdBy']
        category = self.testData._testData[3]['category']
        otherArgs = {'latlon':ll}
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,**otherArgs)  
        except AssertionError:
            self.fail("Assertion Error creating Item")
        except:
            self.fail("problem creating item - %s" % sys.exc_info()[0]) 
        
        self.assertEquals(item.getName(), name, "names don't match: %s != %s" % (item.getName(), name))
        self.assertEquals(item.getCategory(), category, "categories don't match: %s != %s" % (item.getCategory(), category))
        self.assertEquals(item.getLatLon()._lat, ll._lat, "lats don't match: %s != %s" % (item.getLatLon()._lat, ll._lat))
        self.assertEquals(item.getLatLon()._lon, ll._lon, "lons don't match: %s != %s" % (item.getLatLon()._lon, ll._lon))
        
    def testInstantiateItemMaxArgs(self):
        '''
        testInstantiateItemMaxArgs
        '''
        ll = Item.LatLon(self.testData._testData[3]['lat'], self.testData._testData[3]['lon'])
        name = self.testData._testData[3]['name']
        createdBy = self.testData._testData[3]['createdBy']
        category = self.testData._testData[3]['category']
        tele = self.testData._testData[3]['phone']
        addr = self.testData._testData[3]['address']
        website = self.testData._testData[3]['url']
        otherArgs = {'latlon': ll, 'phone':tele, 'address':addr, 'url':website}
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy, **otherArgs)

        except AssertionError:
            self.fail("Assertion Error creating Item")
        except:
            self.fail("problem creating item - %s" % sys.exc_info()[0]) 
        
        self.assertEquals(item.getName(), name, "names don't match: %s != %s" % (item.getName(), name))
        self.assertEquals(item.getCategory(), category, "categories don't match: %s != %s" % (item.getCategory(), category))
        self.assertEquals(item.getLatLon()._lat, ll._lat, "lats don't match: %s != %s" % (item.getLatLon()._lat, ll._lat))
        self.assertEquals(item.getLatLon()._lon, ll._lon, "lons don't match: %s != %s" % (item.getLatLon()._lon, ll._lon))
        self.assertEquals(item.getPhone(), tele, "telephone #s don't match: %s != %s" % (item.getPhone(), tele))
        self.assertEquals(item.getAddress(), addr, "addresses don't match: %s != %s" % (item.getAddress(), addr))
        self.assertEquals(item.getUrl(), website, "names don't match: %s != %s" % (item.getUrl(), website))
### 
# Requirement: Unable to create an item when minimum attributes NOT specified
###  
    def testInstantiateItemMissingArgs(self):
        '''
        testInstantiateItemMissingArgs
        '''
        name = self.testData._testData[3]['name']
        createdBy = self.testData._testData[3]['createdBy']
        category = self.testData._testData[3]['category']
        tele = self.testData._testData[3]['phone']
        website = self.testData._testData[3]['url']
        otherArgs = {'phone':tele, 'url':website}
        # missing address AND latlon
        item = Item.ThingToDo()
        
        self.assertRaises(AttributeError, item.setAttrs, name,category,createdBy, **otherArgs)

###
# Requirement: Only enumerated categories allowed
###
    def testInstantiateItemBogusCategory(self):
        '''
        testInstantiateItemBogusCategory
        '''
        name = self.testData._testData[3]['name']
        createdBy = self.testData._testData[3]['createdBy']
        category = "Nonsense"
        otherArgs = {'address':self.testData._testData[3]['address']}
        
        item = Item.ThingToDo()
        self.assertRaises(AttributeError, item.setAttrs, name,category,createdBy, **otherArgs)
            
###
# Requirement: Be able to create an item with all args
###
    def testCreateAllArgs(self):
        '''
        testCreateAllArgs
        '''
        ll = Item.LatLon(self.testData._testData[0]['lat'], self.testData._testData[0]['lon'])
        name = self.testData._testData[0]['name']
        createdBy = self.testData._testData[0]['createdBy']
        category = self.testData._testData[0]['category']
        tele = self.testData._testData[0]['phone']
        addr = self.testData._testData[0]['address']
        website = self.testData._testData[0]['url']
        mail = self.testData._testData[0]['email']
        rate = self.testData._testData[0]['rating']
        revs = self.testData._testData[0]['review']
        description = self.testData._testData[0]['url']
        otherArgs = {'latlon':ll, 'phone':tele, 'address':addr, 'url':website, 'email':mail, 'rating':rate,
                     'review':revs, 'descr':description}
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,**otherArgs)
        except AssertionError:
            self.fail("Assertion Error creating Item")
        except Exception as e:
            self.fail("problem creating item - %s" % e) 
        
        self.assertEqual(item.getPhone(), tele)
        self.assertEqual(item.getAddress(), addr)
        self.assertEqual(item.getUrl(), website)
        self.assertEqual(item.getName(), name)
        self.assertEqual(item.getCreatedBy(), createdBy)
        self.assertEqual(item.getCategory(), category)
        self.assertEqual(item.getEmail(), mail)
        self.assertEqual(item.getDescr(), description)
        self.assertEqual(item.getRating(), rate)
        self.assertEqual(item.getReview(), revs)
        self.assertEqual(item.getLatLon()._lat, ll._lat)
        self.assertEqual(item.getLatLon()._lon, ll._lon)
        

###
# Requirement: Be able to encapsulate a lat/lon pair
###
    def testLatLon(self):
        '''
        testLatLon
        '''
        lat = 42.687
        lon = -71.110
        ll = Item.LatLon(lat, lon)
        self.assertEqual(ll._lat, lat)
        self.assertEqual(ll._lon, lon)
        
    def testLatLonBoundingBox(self):
        '''
        testLatLonBoundingBox
        '''
        lat = 42.687
        lon = -71.110
        offset = 10
        ll = Item.LatLon(lat, lon)
        ll.boundingBox(offset)
        self.assertEqual(len(ll._box), 4)
        for latlon in ll._box:
            self.assertEqual(len(latlon), 2)
        self.assertTrue(ll.getLATmax() > lat)
        self.assertTrue(ll.getLONmax() > lon)
        self.assertTrue(ll.getLATmin() < lat)
        self.assertTrue(ll.getLONmin() < lon)

###
# Requirement: search criteria is an encapsulation. Need to be able to create
#    the encapsulation & not lose criteria, or have bogus ones created
###
    def testSearchFor(self):
        '''
        testSearchFor
        '''
        searchFor = Item.SearchFor()
        searchFor.setAttr('name', "Far Corner Golf Course")
        searchFor.setAttr('category', "Recreational")
        searchFor.setAttr('createdBy', "Ottodelupe")
        searchFor.setAttr('address', "5 Barker Road, Boxford, MA")
        
        self.assertEqual(searchFor.getAttr('name'), "Far Corner Golf Course")
        self.assertEqual(searchFor.getAttr('category'), "Recreational")
        self.assertEqual(searchFor.getAttr('createdBy'), "Ottodelupe")
        self.assertEqual(searchFor.getAttr('address'), "5 Barker Road, Boxford, MA")
        self.assertRaises(KeyError, searchFor.getAttr, 'foobar')
        
        wc = searchFor.makeWhereClause()
        expected = 'category = \"Recreational\" and name = \"Far Corner Golf Course\" and createdBy = \"Ottodelupe\" and address = \"5 Barker Road, Boxford, MA\"'
        self.assertEqual(wc, expected)
        
    def testMakeWhereClause(self):
        '''
        testMakeWhereClause
        '''
        offset = 10
        ll = Item.LatLon(42.69095, -71.1277)
        ll.boundingBox(offset)
        expected = 'lat between \"%f\" and \"%f\" and lon between \"%f\" and \"%f\"' % \
            (ll.getLATmax(), ll.getLATmin(), ll.getLONmax(), ll.getLONmin())
            
        searchFor = Item.SearchFor()
        searchFor.setAttr('latlon', ll)
        searchFor.setAttr('offset', offset)

        whereclause = searchFor.makeWhereClause()
        self.assertEqual(expected, whereclause)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #suite = unittest.TestLoader().loadTestsFromTestCase(ItemTest)
    #unittest.main()
    unittest.main()

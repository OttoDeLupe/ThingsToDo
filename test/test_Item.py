'''
Created on Jun 28, 2011

@author: papabear
'''
import unittest
import Item
import sys
import Utils
import logging

logging.basicConfig(filename="t2dLog.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')

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
        lat = self.testData._testData[3]['lat']
        lon = self.testData._testData[3]['lon']
        name = self.testData._testData[3]['name']
        createdBy = self.testData._testData[3]['createdBy']
        category = self.testData._testData[3]['category']
        otherArgs = {'lat':lat, 'lon':lon}
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
        self.assertEquals(item.getLat(), lat, "lats don't match: %s != %s" % (item.getLat(), lat))
        self.assertEquals(item.getLon(), lon, "lons don't match: %s != %s" % (item.getLon(), lon))
        
    def testInstantiateItemMaxArgs(self):
        '''
        testInstantiateItemMaxArgs
        '''
        lat = self.testData._testData[3]['lat']
        lon =  self.testData._testData[3]['lon']
        name = self.testData._testData[3]['name']
        createdBy = self.testData._testData[3]['createdBy']
        category = self.testData._testData[3]['category']
        tele = self.testData._testData[3]['phone']
        addr = self.testData._testData[3]['address']
        website = self.testData._testData[3]['url']
        otherArgs = {'lat': lat, 'lon':lon, 'phone':tele, 'address':addr, 'url':website}
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
        self.assertEquals(item.getLat(), lat, "lats don't match: %s != %s" % (item.getLat(), lat))
        self.assertEquals(item.getLon(), lon, "lons don't match: %s != %s" % (item.getLon(), lon))
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
        lat = self.testData._testData[0]['lat']
        lon = self.testData._testData[0]['lon']
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
        otherArgs = {'lat':lat, 'lon':lon, 'phone':tele, 'address':addr, 'url':website, 'email':mail, 'rating':rate,
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
        self.assertEqual(item.getLat(), lat)
        self.assertEqual(item.getLon(), lon)
        
    def testUpdateExistingAttribute(self):
        '''
        testUpdatetExistingAttribute
        Update an existing attribute with a new value
        '''
        lat = self.testData._testData[0]['lat']
        lon = self.testData._testData[0]['lon']
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
        otherArgs = {'lat':lat, 'lon':lon, 'phone':tele, 'address':addr, 'url':website, 'email':mail, 'rating':rate,
                     'review':revs, 'descr':description}
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,**otherArgs)
        except AssertionError:
            self.fail("Assertion Error creating Item")
        except Exception as e:
            self.fail("problem creating item - %s" % e) 
            
        # Here's the real test
        item.setAttribute('phone', '123-456-7890')
        self.assertEqual(item.getPhone(), '123-456-7890')
        
    def testSetNonExistingAttribute(self):
        '''
        testSetNonExistingAttribute
        Add a new attribute to an existing item, should fail
        '''
        lat = self.testData._testData[0]['lat']
        lon = self.testData._testData[0]['lon']
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
        otherArgs = {'lat':lat, 'lon':lon, 'phone':tele, 'address':addr, 'url':website, 'email':mail, 'rating':rate,
                     'review':revs, 'descr':description}
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,**otherArgs)
        except AssertionError:
            self.fail("Assertion Error creating Item")
        except Exception as e:
            self.fail("problem creating item - %s" % e) 
            
        # Here's the real test
        self.assertRaises(KeyError,item.setAttribute, 'random', 'random notes') 
 
        
    def testUpdateNonMutableAttribute(self):
        '''
        testUpdateNonMutableAttribute
        Shouldn't be able to update name, category or createdBy
        '''
        lat = self.testData._testData[0]['lat']
        lon = self.testData._testData[0]['lon']
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
        otherArgs = {'lat':lat, 'lon':lon, 'phone':tele, 'address':addr, 'url':website, 'email':mail, 'rating':rate,
                     'review':revs, 'descr':description}
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,**otherArgs)
        except AssertionError:
            self.fail("Assertion Error creating Item")
        except Exception as e:
            self.fail("problem creating item - %s" % e) 
            
        # Here's the real test
        self.assertRaises(AttributeError,item.setAttribute, 'name', 'ANewName') 
###
# Requirement: Be able to encapsulate a lat/lon pair
#         SimpleDB represents floats as strings (in order to do
#          comparisons. So need to test that the conversion happens
#          correctly
###
    def testLatLonConvertToString(self):
        '''
        testLatLon
        '''
        lat = 42.687
        lon = -71.110
        ll = Item.LatLon(lat, lon)
        self.assertEqual(ll._lat, '42687000')
        self.assertEqual(ll._lon, '-71110000')
        
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
        self.assertEqual(ll.getLATmax(), '42832000')
        self.assertEqual(ll.getLONmax(), '-70965000')
        self.assertEqual(ll.getLATmin(), '42541999')
        self.assertEqual(ll.getLONmin(), '-71255000')

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
        lat = 42.69095
        lon = -71.1277
        ll = Item.LatLon(lat,lon)
        ll.boundingBox(offset)
        expected = "lat between \'%s\' and \'%s\' and lon between \'%s\' and \'%s\'" % \
            (ll.getLATmax(), ll.getLATmin(), ll.getLONmax(), ll.getLONmin())
            
        searchFor = Item.SearchFor()
        searchFor.setAttr('lat', lat)
        searchFor.setAttr('lon', lon)
        searchFor.setAttr('offset', offset)

        whereclause = searchFor.makeWhereClause()
        self.assertEqual(expected, whereclause)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

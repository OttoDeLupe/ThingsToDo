'''
Created on Jun 28, 2011

@author: papabear
'''
import unittest
import Item
import sys
#import DataAccessLayer

class ItemTest(unittest.TestCase):
    _dbConn = None

    def setUp(self):
        _dbConn = None


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
        name = "Weir Hill"
        createdBy = "Ottodelupe"
        category = "Recreational"
        otherArgs = {'address':"Stevens Street North Andover, MA"}
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,**otherArgs)

        except AssertionError:
            print "problem creating Item"
        except:
            print "problem creating item - %s" % sys.exc_info()[0] 
        
        self.assertEquals(item._name, name, "names don't match: %s != %s" % (item._name, name))
        self.assertEquals(item._category, category, "categories don't match: %s != %s" % (item._category, category))
        self.assertEquals(item._address, otherArgs['address'], "addresses don't match: %s != %s" % (item._address, otherArgs['address']))
        
    def testInstantiateItemWithLatLon(self):
        ll = Item.LatLon(42.697, -71.110)
        name = "Weir Hill"
        createdBy = "Ottodelupe"
        category = "Recreational"
        otherArgs = {'latlon':ll}
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,**otherArgs)  
        except AssertionError:
            print "problem creating Item"
        except:
            print "problem creating item - %s" % sys.exc_info()[0] 
        
        self.assertEquals(item._name, name, "names don't match: %s != %s" % (item._name, name))
        self.assertEquals(item._category, category, "categories don't match: %s != %s" % (item._category, category))
        self.assertEquals(item._latlon._lat, ll._lat, "lats don't match: %s != %s" % (item._latlon._lat, ll._lat))
        self.assertEquals(item._latlon._lon, ll._lon, "lons don't match: %s != %s" % (item._latlon._lon, ll._lon))
        
    def testInstantiateItemMaxArgs(self):
        ll = Item.LatLon(42.697, -71.110)
        tele = "978.682.3580"
        addr = "Stevens Street North Andover, MA"
        website = "http://www.thetrustees.org/places-to-visit/northeast-ma/weir-hill.html"
        name = "Weir Hill"
        createdBy = "Ottodelupe"
        category = "Recreational"
        otherArgs = {'latlon': ll, 'phone':tele, 'address':addr, 'url':website}
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy, **otherArgs)

        except AssertionError:
            print "problem creating Item"
        except:
            print "problem creating item - %s" % sys.exc_info()[0] 
        
        self.assertEquals(item._name, name, "names don't match: %s != %s" % (item._name, name))
        self.assertEquals(item._category, category, "categories don't match: %s != %s" % (item._category, category))
        self.assertEquals(item._latlon._lat, ll._lat, "lats don't match: %s != %s" % (item._latlon._lat, ll._lat))
        self.assertEquals(item._latlon._lon, ll._lon, "lons don't match: %s != %s" % (item._latlon._lon, ll._lon))
        self.assertEquals(item._phone, tele, "telephone #s don't match: %s != %s" % (item._phone, tele))
        self.assertEquals(item._address, addr, "addresses don't match: %s != %s" % (item._address, addr))
        self.assertEquals(item._url, website, "names don't match: %s != %s" % (item._url, website))
### 
# Requirement: Unable to create an item when minimum attributes NOT specified
###  
    def testInstantiateItemMissingArgs(self):
        tele = "978.682.3580"
        website = "http://www.thetrustees.org/places-to-visit/northeast-ma/weir-hill.html"
        name = "Weir Hill"
        createdBy = "Ottodelupe"
        category = "Recreational"
        otherArgs = {'phone':tele, 'url':website}
        # missing address AND latlon
        item = Item.ThingToDo()
        
        self.assertRaises(AttributeError, item.setAttrs, name,category,createdBy, **otherArgs)

###
# Requirement: Only enumerated categories allowed
###
    def testInstantiateItemBogusCategory(self):
        name = "Weir Hill"
        createdBy = "Ottodelupe"
        category = "Nonsense"
        addr = "Stevens Street North Andover, MA"
        otherArgs = {'address': addr}
        
        item = Item.ThingToDo()
        self.assertRaises(AttributeError, item.setAttrs, name,category,createdBy, **otherArgs)
            
###
# Requirement: Be able to serialize and deserialize an item
###
    def testSerialize(self):
        ll = Item.LatLon(42.697, -71.110)
        tele = "978.682.3580"
        addr = "Stevens Street North Andover, MA"
        website = "http://www.thetrustees.org/places-to-visit/northeast-ma/weir-hill.html"
        name = "Weir Hill"
        createdBy = "Ottodelupe"
        category = "Recreational"
        mail = None
        rate = None
        revs = None
        description = None
        otherArgs = {'latlon':ll, 'phone':tele, 'address':addr, 'url':website, 'email':mail, 'rating':rate,
                     'reviews':revs, 'descr':description}
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,**otherArgs)
        except AssertionError:
            print "problem creating Item"
            return
        except:
            print "problem creating item - %s" % sys.exc_info()[0] 
        
        self.assertEqual(item._serialized['phone'], tele)
        self.assertEqual(item._serialized['address'], addr)
        self.assertEqual(item._serialized['url'], website)
        self.assertEqual(item._serialized['name'], name)
        self.assertEqual(item._serialized['createdBy'], createdBy)
        self.assertEqual(item._serialized['category'], category)
#        self.assertRaises(KeyError, item._serialized['email'])
#        self.assertRaises(KeyError, item._serialized['descr'])
#        self.assertRaises(KeyError, item._serialized['rating'])
#        self.assertRaises(KeyError, item._serialized['reviews'])
        self.assertEqual(item._serialized['lat'], ll._lat)
        self.assertEqual(item._serialized['lon'], ll._lon)
        

###
# Requirement: Be able to encapsulate a lat/lon pair
###
    def testLatLon(self):
        lat = 42.687
        lon = -71.110
        ll = Item.LatLon(lat, lon)
        self.assertEqual(ll._lat, lat)
        self.assertEqual(ll._lon, lon)
        
    def testLatLonBoundingBox(self):
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

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
        addr = "Stevens Street North Andover, MA"
        name = "Weir Hill"
        createdBy = "Ottodelupe"
        category = "Recreational"
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,address=addr)

        except AssertionError:
            print "problem creating Item"
        except:
            print "problem creating item - %s" % sys.exc_info()[0] 
        
        self.assertEquals(item._name, name)
        self.assertEquals(item._category, category)
        self.assertEquals(item._address, addr)
        
    def testInstantiateItemWithLatLon(self):
        ll = Item.LatLon(42.697, -71.110)
        name = "Weir Hill"
        createdBy = "Ottodelupe"
        category = "Recreational"
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,latlon=ll)  
        except AssertionError:
            print "problem creating Item"
        except:
            print "problem creating item - %s" % sys.exc_info()[0] 
        
        self.assertEquals(item._name, name)
        self.assertEquals(item._category, category)
        self.assertEquals(item._latlon, ll)
        
    def testInstantiateItemMaxArgs(self):
        ll = Item.LatLon(42.697, -71.110)
        tele = "978.682.3580"
        addr = "Stevens Street North Andover, MA"
        website = "http://www.thetrustees.org/places-to-visit/northeast-ma/weir-hill.html"
        name = "Weir Hill"
        createdBy = "Ottodelupe"
        category = "Recreational"
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,address=addr,latlon=ll,url=website,phone=tele)

        except AssertionError:
            print "problem creating Item"
        except:
            print "problem creating item - %s" % sys.exc_info()[0] 
        
        self.assertEquals(item._name, name)
        self.assertEquals(item._category, category)
        self.assertEquals(item._address, addr)
        
### 
# Requirement: Unable to create an item when minimum attributes NOT specified
###  
    def testInstantiateItemMissingArgs(self):
        tele = "978.682.3580"
        website = "http://www.thetrustees.org/places-to-visit/northeast-ma/weir-hill.html"
        name = "Weir Hill"
        createdBy = "Ottodelupe"
        category = "Recreational"
        # missing address AND latlon
        item = Item.ThingToDo()
        
        self.assertRaises(AttributeError, item.setAttrs, name,category,createdBy, url=website, phone=tele)

###
# Requirement: Only enumerated categories allowed
###
    def testInstantiateItemBogusCategory(self):
        name = "Weir Hill"
        createdBy = "Ottodelupe"
        category = "Nonsense"
        addr = "Stevens Street North Andover, MA"
        item = Item.ThingToDo()
        self.assertRaises(AttributeError, item.setAttrs, name,category,createdBy,address=addr)
            
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
        try:
            item = Item.ThingToDo()
            self.assertTrue(item)
            item.setAttrs(name,category,createdBy,address=addr,latlon=ll,url=website,phone=tele,
                          email=mail, rating=rate, reviews=revs, descr=description)
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
        self.assertEqual(item._serialized['email'], mail)
        self.assertEqual(item._serialized['descr'], description)
        self.assertEqual(item._serialized['rating'], rate)
        self.assertEqual(item._serialized['reviews'], revs)
        self.assertEqual(item._serialized['lat'], ll._lat)
        self.assertEqual(item._serialized['lon'], ll._lon)
        
         
                
# Requirement: An update to an item is automatically persisted
###

### 
# Requirement: Be able to read an item from the persistence store
#    using just lat/lon. Should take lat/lon as a center of a geo-box
#    and return all matches inside the geo-box. The geo-box has to be
#    some +/- from the center to get the sides of the box
###

###
# Requirement: Be able to delete an item from the persistence store
###    


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

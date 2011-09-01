'''
Created on Aug 23, 2011

@author: papabear
'''
import unittest
import Utils
import Item
import binascii
import uuid


class UtilsTest(unittest.TestCase):


    def setUp(self):
        self.testData = Utils.Utils();


    def tearDown(self):
        pass

    def testRightNumberOfTestItems(self):
        self.assertEqual(9, len(self.testData._testData), "incorrect number of items in test data")
        
    def testValidPK(self):
        name = "WhatAGreatPlaceToRockAndRoll"
        category = "Recreational"
        myuuid = str(uuid.UUID(binascii.hexlify("%d%s" % (0, name[0:15]))))
        self.assertEqual(Item.genPK(name, category), myuuid)
        
    def testReviewIsKey(self):
        '''even if review was not supplied, the key has to exist'''
        for d in self.testData._testData:
            self.assertTrue('review' in d, "review key not present")
    
    def testReviewIsList(self):
        '''the value for the review has to be a list'''
        for d in self.testData._testData:
            self.assertTrue((len(d['review']) >= 0), "review value not list")
                                 
    def testLatLonNumbers(self):
        '''lat and lon should be floats, not strings'''
        for d in self.testData._testData:
            if 'lat' in d:
                self.assertTrue(type(d['lat'] is float), "lat is not a float")
            if 'lon' in d:
                self.assertTrue(type(d['lon'] is float), "lon is not a float")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
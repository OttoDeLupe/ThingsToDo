'''
Created on Aug 23, 2011

@author: papabear
'''
import unittest
import Utils
import Item


class UtilsTest(unittest.TestCase):


    def setUp(self):
        self.testData = Utils.Utils();


    def tearDown(self):
        pass

    def testRightNumberOfTestItems(self):
        self.assertEqual(9, len(self.testData._testData), "incorrect number of items in test data")

    def testPKValid(self):
        self.assertIsNotNone(self.testData)
        for d in self.testData._testData:
            self.assertEqual(Item.genPK(d['name'], d['category']), d['pk'], "invalid PK")
    
    def testReviewIsKey(self):
        '''even if review was not supplied, the key has to exist'''
        for d in self.testData._testData:
            self.assertTrue('review' in d, "review key not present")
            
    def testReviewIsList(self):
        '''the value for the review has to be a list'''
        for d in self.testData._testData:
            self.assertTrue((len(d['review']) >= 0), "review value not list")
                            
    def testPKUnique(self):
        keys = []
        for d in self.testData._testData:
            keys.append(d['pk'])
        pk = '||Far Corner Golf Course||Recreational||'
        self.assertEqual(keys.count(pk), 1, "pk not unique")
            
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
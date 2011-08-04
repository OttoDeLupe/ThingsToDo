'''
Created on Aug 2, 2011

@author: papabear
'''
import unittest


class IntegrationTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    @unittest.skip("not yet implemented")
    def testGetReturns404(self):
        '''
        make sure that when accessing a bogus resource, we get back a 404
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testGetReturns400(self):
        '''
        make sure that under the right conditions we get back a 400
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testGetReturns500(self):
        '''
        make sure that under the right conditions we get back a 500
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testPostReturns404(self):
        '''
        make sure that when accessing a bogus resource, we get back a 404
        '''
        self.fail("not yet implemented")
    
    @unittest.skip("not yet implemented")    
    def testPostReturns400(self):
        '''
        make sure that under the right conditions we get back a 400
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testpostReturns500(self):
        '''
        make sure that under the right conditions we get back a 500
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testPutReturns404(self):
        '''
        make sure that when accessing a bogus resource, we get back a 404
        '''
        self.fail("not yet implemented")
    
    @unittest.skip("not yet implemented")    
    def testPutReturns400(self):
        '''
        make sure that under the right conditions we get back a 400
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testPutxsReturns500(self):
        '''
        make sure that under the right conditions we get back a 500
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testDeleteReturns404(self):
        '''
        make sure that when accessing a bogus resource, we get back a 404
        '''
        self.fail("not yet implemented")
    
    @unittest.skip("not yet implemented")    
    def testDeleteReturns400(self):
        '''
        make sure that under the right conditions we get back a 400
        '''
        self.fail("not yet implemented")

    @unittest.skip("not yet implemented")
    def testDeleteReturns500(self):
        '''
        make sure that under the right conditions we get back a 500
        '''
        self.fail("not yet implemented")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
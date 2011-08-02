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


    def testGetReturns404(self):
        '''
        make sure that when accessing a bogus resource, we get back a 404
        '''
        pass

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
'''
Created on Jul 18, 2011

@author: papabear
'''
import DataAccessLayer
import Item
import sys

class BizLayer():
    '''
    The top level API layer. Implements the REST interface. Creates Items,
    reads/writes from/to the DataAccessLayer.    
    '''
   
    def write(self, item):
        '''
        The caller will have unpacked the data from the REST API and created an Item
        This function then gets a db connection and writes the item to it
        '''
        self._DAL = DataAccessLayer.DataAccessLayer()
        self.assertTrue(self._DAL)
        
        try:
            self._DAL.write(item._pk, item._serialized)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
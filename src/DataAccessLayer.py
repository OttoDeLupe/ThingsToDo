'''
Created on Jun 28, 2011

@author: papabear
'''
import boto
import logging
import os

AWSSECRETKEY = 'AHkuWnXxYzrX1ttLo8ecmSlgcAJuxD2XkMsKDW92'
AWSACCESSKEY = '0G11Z2V0K6ZEKXEH9H82'
if 'T2DTestMode' in os.environ:
    AWSDOMAIN = 'ThingsToDoTestDomain'
else:
    AWSDOMAIN = 'ThingsToDoDomain'

class DataAccessLayer():
    '''
    Maintain the interface to the persistence system
    '''
    def __init__(self):
        '''
        Constructor
        '''
        try:
            self._conn = boto.connect_sdb(AWSACCESSKEY,AWSSECRETKEY)
            self._domain = self._conn.get_domain(AWSDOMAIN)
            assert(self._domain)
        except boto.exception.SDBResponseError:
            logging.info('DAL-init - create new AWS domain')
            self._domain = self._conn.create_domain(AWSDOMAIN)
               
    def read(self, criteria):
        '''
        will return a list of zero or more records matching the passed search criteria
        TBD: need to account for paging/cursors
        '''
        select = 'select * from %s where %s' % (AWSDOMAIN, criteria)
        try:
            resultIter = self._domain.select(select)
        except boto.exception.SDBResponseError, e:
            logging.error('DAL-read - SDBResponseError in read: %s, %s', e.status, e.reason)
        except Exception as ex:
            logging.critical('DAL-read - unexpected exception %s', ex)
            raise
        rs = []
        try:  
            for r in resultIter:
                rs.append(r)
        except boto.exception.SDBResponseError, e:
            logging.error('DAL-read - SDBResponseError in read: %s, %s', e.status, e.reason)
        except Exception as ex:
            logging.critical('DAL-read - unexpected exception %s', ex)
            raise
        return rs if rs != [] else None
        
        
    def write(self, item):
        '''
        item will be a dict
        if the key already exists, then the values are updated
        if the key doesn't exist, it's created and then the values added
        '''
        # does key already exist?
        key = item['pk']
        try:
            foundrow = self._domain.get_item(key)
        except Exception as ex:
            logging.critical('DAL-write - unexpected exception %s', ex)
            raise
        
        if foundrow:
            # write new values to existing attributes
            logging.info('DAL-write - updating existing row')
            for attr, val in item.iteritems():
                foundrow[attr] = val
            foundrow.save(replace=True)
        else:
            logging.info('DAL-write - adding new row')
            newrow = self._domain.new_item(key)
            for attr, val in item.iteritems():
                newrow[attr] = val
            newrow.save()
            
        
    
    def delete(self, key):
        # does key already exist?
        try:
            foundrow = self._domain.get_item(key)
        except Exception as ex:
            logging.critical('DAL-delete - unexpected exception %s', ex)
            raise
        
        if foundrow:
            foundrow.delete()
        else:
            logging.error('DAL-delete - row not found')
            raise AttributeError('Key Not Found')
            
        
    
    
        
        

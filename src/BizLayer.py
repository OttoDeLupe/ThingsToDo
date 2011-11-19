'''
Created on Jul 18, 2011

@author: papabear

    The top level API layer. Implements the REST interface. Creates Items,
    reads/writes from/to the DataAccessLayer. receives json, converts to
    Item, does some operation with the item (like uses it in a read or write
    call to the DAL), gets some item(s) back, puts this into a json and
    ships it back.

    URIs: (1) thing to do (t2d), (2) collection of t2d (t2dList)
    Format: JSON - value is string, unless otherwise noted
     t2d = {"pk":value , "name":value , "category":value , "createdBy":value ,
             "address":value , "lat":float_value, "lon":float_value, "phone":value ,
             "email":value , "url":value , "description":value , "rating":value
             "reviews": [{"review":value} , {"review":value} , ...]}
     t2dList = [t2d , t2d, t2d ...]

     t2d GET t2d format, status codes 200, 400, 404, 500
     t2d POST t2d format status codes 200, 400, 500
       -> Semantically, POST = Update
     t2d PUT t2d format status codes 200, 400, 500
       -> Semantically, PUT = Create
     t2d DELETE t2d format status codes 200, 400, 500
     
     t2dList GET t2dList format status codes 200, 400, 500
     t2dList POST/PUT/DELETE: status codes 405
     -> Only allowed to create/update/delete individual t2d, not collections 
'''

import web
import os
import re
import json
import logging

import DataAccessLayer
import Item

urls = ('/t2d/(.*)', 't2d', '/t2dList', 't2dList')
t2dApp = web.application(urls, globals())
latlon_offset = 10.0

VALID_KEY = re.compile('[a-zA-Z0-9_-]{1,255}')
def isValidKey(key):
    """Checks to see if the parameter follows the allow pattern of
    keys.
    """
    if VALID_KEY.match(key) is not None:
        return True
    return False

def isTestMode():
    if 'T2DTestMode' in os.environ:
        return True
    else:
        return False

def getByKeys(pk=None, attrs=None):
    '''
    help function used by t2d.GET and t2dList.GET to query
    the data store & return what is found based on the 
    key (PK) or attributes passed
    
    BUG: if the attrs are lat/lon, this code will create a search string that will never find anything
     - there's no item that will be at the unique lat/lon passed. 
     The search criteria needs to be expanded to account for the lat/lon bounding box
     But - should this be only for t2dlist searches, or for t2d?foo=... as well?
    '''
    if isTestMode(): # check env. if in test mode, import dbconn mock
        import Shared 
        dbConn = Shared.dbMock
    else:
        dbConn = DataAccessLayer.DataAccessLayer()

    searchFor = Item.SearchFor()
    if pk is not None:
        searchFor.setAttr('pk', pk)
    elif attrs is not None:
        for k, v in attrs.iteritems():
            searchFor.setAttr(k, v)
    else:
        raise KeyError

    try:
        where = searchFor.makeWhereClause()
        logging.debug('getByKeys - looking for: %s', where)
        rtn = dbConn.read(where)
    except Exception as e:
        print e
        raise e
    logging.debug('getByKeys - found: %s', rtn)
    return rtn

def getByLatLon(lat,lon):
    if isTestMode():
        import Shared
        dbConn = Shared.dbMock
    else:
        dbConn = DataAccessLayer.DataAccessLayer()
        
    searchFor = Item.SearchFor()
    searchFor.setAttr('lat', lat)
    searchFor.setAttr('lon', lon)
    searchFor.setAttr('offset', latlon_offset)
    logging.debug('getByLatLon - looking near %s, %s', lat, lon)
    try:
        where = searchFor.makeWhereClause()
        logging.debug('getByLatLon - where clause: %s', where)
        rtn = dbConn.read(where)
    except Exception as e:
        print e
        raise e
    logging.debug('getByLatLon - found: %s', rtn)
    return rtn
        

class t2d():
    ''' REST interface implementing WebService methods for a Thing To Do (t2d)'''
    def GET(self, resource):
        '''
        dejsonize the critieria, get a db connection, search for the criteria, get a list of
        matching items back, json-ize them, send them back to the client
        '''
        if not isValidKey(resource):
            logging.info('Item-GET: invalid resource key (%s)', resource)
            web.badrequest()
            return
        
        try:
            rtn = getByKeys(resource)
        except:
            logging.info('Item-GET: invalid resource (%s)', resource)
            web.badrequest()
            return

        if rtn is None:
            logging.info('Item-GET: resource not found (%s)', resource)
            web.notfound()
            return 
            
        web.header('Content-Type', 'text/plain')
        return json.JSONEncoder().encode(rtn)
        return rtn

    def DELETE(self, resource):
        '''
        Try to delete the supplied resource
        '''
        if isTestMode(): # check env. if in test mode, import dbconn mock
            import Shared
            dbConn = Shared.dbMock
        else:
            dbConn = DataAccessLayer.DataAccessLayer()

        if not isValidKey(resource):
            logging.info('Item-DELETE: invalid resource key (%s)', resource)
            web.badrequest()
            return

        try:
            dbConn.delete(resource)
        except AttributeError:
            logging.warning('Item-DELETE: unable to delete resource (%s)', resource)
            web.notfound()
            return
        except Exception as e:
            logging.error('Item-DELETE: Unexpected exception when deleting: %s', e)
            web.badrequest()
            return
        web.ok()
        return

    def PUT(self, ignoreMe):
        '''
        PUT == Create
        '''
        jsonData = web.data()
        item = Item.ThingToDo()
        try:
            itemData = json.JSONDecoder().decode(jsonData)
        except:
            logging.error('Item-PUT: unable to decode json %s' % jsonData)
            web.badrequest()
            return
        
        if isTestMode(): # check env. if in test mode, import dbconn mock
            import Shared
            dbConn = Shared.dbMock
        else:
            dbConn = DataAccessLayer.DataAccessLayer()
        
#        if 'lat' in itemData and 'lon' in itemData:
#            itemData['latlon'] = Item.LatLon(itemData['lat'], itemData['lon'])
#            
        # name, category and createdBy are required
        if not ('name' in itemData and 'category' in itemData and 'createdBy' in itemData):
            logging.info('Item-PUT: missing required args')
            web.badrequest()
            return

        # One of address or lat/lon pair required
        if 'address' not in itemData and not ('lat' in itemData and 'lon' in itemData):
            logging.info('Item-PUT: missing address and lat/lon')
            web.badrequest()
            return

        otherArgs = {}
        for attr, val in itemData.iteritems():
            if attr == 'name' or attr == 'category' or attr == 'createdBy':
                # remove from the dict so that what remains is what setAttrs expects for keyword args
                continue
            # special handling of lat/lon so we get a textual represenation, rather than a numeric
            if attr == 'lat':
                ll = Item.LatLon(val, 0.0)
                otherArgs[attr] = ll._lat
                continue
            if attr == 'lon':
                ll = Item.LatLon(0.0, val)
                otherArgs[attr] = ll._lon
                continue
            # everything else just gets added to the keyword args
            otherArgs[attr] = val
        
        try: 
            item.setAttrs(itemData['name'], itemData['category'], itemData['createdBy'], **otherArgs)
        except:
            logging.error('Item-PUT: unable to set attributes')
            web.badrequest()
            return
        
        # If the item already exists, that's an error - caller should be using POST, not PUT
        # Make the PK and see if it exists. AttributeError if it does
        PK = Item.genPK(itemData['name'], itemData['category'])
        searchFor = Item.SearchFor()
        searchFor.setAttr('pk', PK)
        where = searchFor.makeWhereClause()
        
        try:
            rtn = dbConn.read(where)
        except Exception as ex:
            logging.error('Item-PUT: Unexpected exception checking for existing record - %s', ex)
            web.badrequest()
            return
        if rtn != None:
            logging.info('Item-PUT: item already exists (%s)', PK)
            web.conflict()
            return
        
        # now that we have an item that doesn't exist, write it to the dbconn
        try:
            dbConn.write(item._serialized)
        except Exception as ex:
            logging.error('Item-PUT: unexpected exception writing item - %s', ex)
            web.badrequest()
            return
        
        return json.JSONEncoder().encode(item._serialized)
            

    def POST(self, ignoreMe):
        '''
        Update the resource found in the PK passed in
        '''
        jsonData = web.data()

        newData = json.JSONDecoder().decode(jsonData)
        if isTestMode(): # check env. if in test mode, import dbconn mock
            import Shared
            dbConn = Shared.dbMock
        else:
            dbConn = DataAccessLayer.DataAccessLayer()

        # Find the item based on the PK passed
        # Update the record, adding new columns if they don't already exist
        
        if not isValidKey(newData['pk']):
            logging.info('Item-POST: invalid resource key (%s)', newData['pk'])
            web.badrequest()
            return
        
        try:
            existingData = getByKeys(newData['pk'])
        except:
            logging.info('Item-POST: invalid resource (%s)',newData['pk'])
            web.badrequest()
            return

        if existingData is None:
            logging.info('Item-POST: record does not exist (%s)', newData['pk'])
            web.notfound()
            return

        # Got the record - update it
        # It's not a Item.ThingToDo, however. Must turn it into one
        item = Item.ThingToDo()
        otherArgs = {}
        for attr, val in existingData.iteritems():
            if attr in ('name', 'category', 'createdBy'):
                # remove from the dict so that what remains is what setAttrs expects for keyword args
                continue
            otherArgs[attr] = val
        item.setAttrs(existingData['name'],existingData['category'],existingData['createdBy'], **otherArgs)
        # OK, breathed life into a ThingToDo, now, update based on the data passed
        for attr, val in newData.iteritems():
            if attr in ('name','category','createdBy'): continue
            try:
                item.setAttribute(attr, val)
            except KeyError:
                logging.info('Item-POST: Unknown attribute (%s)',attr)
                web.badrequest()
                return
            except Exception as e:
                logging.error('Item-POST: unexpected exception %s', e)
                web.internalerror()
                return
        web.ok()
        
        # Finally update the record
        try:
            dbConn.write(item._serialized)
        except Exception as ex:
            logging.error('Item-POST: unexpected exception writing item - %s', ex)
            web.badrequest()
            return
        web.ok()
        
        
    



class t2dList():
    """
    handles resources that are lists of t2d items
    """
    def GET(self):
        search = web.input()
        logging.info('List-GET - entering')
        # Search criteria must contain the key category
        if 'category' not in search:
            logging.info('List-GET - no category supplied')
            web.badrequest()
            return
        # OK, have a category - is it a valid category?
        if search['category'] not in Item.CATEGORIES:
            logging.info('List-GET - category (%s) not in CATEGORIES', search['category'])
            web.notfound()
            return
        # OK, have a valid category, did we get either lat/lon or address?
        if 'address' not in search:
            if 'lat' not in search and 'lon' not in search:
                logging.info('List-GET - One of address or lat/lon not supplied')
                web.badrequest()
                return
            else:
                # no address, but we do have the lat/lon
                try:
                    rtn = getByLatLon(float(search['lat']), float(search['lon']))
                except Exception as e:
                    logging.error('List-GET - unexpected exception %s', e)
                    web.internalerror()
                    return
                web.header('Content-Type', 'text/plain')
                logging.debug('List-GET - searched for lat %s lon %s', search['lat'], search['lon'])
                logging.debug('List-GET - found %s', rtn)
                logging.debug('List-GET - returned json %s', json.JSONEncoder().encode(rtn))
                return json.JSONEncoder().encode(rtn)
        else:
            # did get address, look for that
            try:
                rtn = getByKeys(None, {'category':search['category'], 'address':search['address']})
            except:
                logging.error('List-GET - unexpected exception %s', e)
                web.internalerror()
                return
            web.header('Content-Type', 'text/plain')
            return json.JSONEncoder().encode(rtn)         

    def PUT(self):
        web.nomethod()
    def POST(self):
        web.nomethod()
    def DELETE(self):
        web.nomethod()

if __name__ == "__main__": 
    logging.basicConfig(filename="t2dLog.log", level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')
    t2dApp.run()

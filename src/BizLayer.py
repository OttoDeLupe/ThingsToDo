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
import uuid
import json

import DataAccessLayer
import Item

urls = ('/t2d/(.*)', 't2d', '/t2dList', 't2dList')
t2dApp = web.application(urls, globals())

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
    where = searchFor.makeWhereClause()

    try:
        rtn = dbConn.read(where)
    except Exception as e:
        print e
        raise e
    return rtn


class t2d():
    ''' REST interface implementing WebService methods for a Thing To Do (t2d)'''
    def GET(self, resource):
        '''
        dejsonize the critieria, get a db connection, search for the criteria, get a list of
        matching items back, json-ize them, send them back to the client
        '''
        if not isValidKey(resource):
            web.badrequest()
            return
        
        try:
            rtn = getByKeys(resource)
        except:
            web.badrequest()
            return

        if rtn is None:
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
            web.badrequest()
            return

        try:
            dbConn.delete(resource)
        except AttributeError:
            web.notfound()
            return
        except:
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
        itemData = json.JSONDecoder().decode(jsonData)
        if isTestMode(): # check env. if in test mode, import dbconn mock
            import Shared
            dbConn = Shared.dbMock
        else:
            dbConn = DataAccessLayer.DataAccessLayer()
        
        if 'lat' in itemData and 'lon' in itemData:
            itemData['latlon'] = Item.LatLon(itemData['lat'], itemData['lon'])
            
        # name, category and createdBy are required
        if not ('name' in itemData and 'category' in itemData and 'createdBy' in itemData):
            web.badrequest()
            return

        # One of address or lat/lon pair required
        if 'address' not in itemData and not ('lat' in itemData and 'lon' in itemData):
            web.badrequest()
            return

        otherArgs = {}
        for attr, val in itemData.iteritems():
            if attr == 'name' or attr == 'category' or attr == 'createdBy':
                # remove from the dict so that what remains is what setAttrs expects for keyword args
                continue
            if attr == 'lat' or attr == 'lon': continue
            otherArgs[attr] = val
        
        try: 
            item.setAttrs(itemData['name'], itemData['category'], itemData['createdBy'], **otherArgs)
        except:
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
            print 'Unexpected error in checking for existing record -', ex
            web.badrequest()
            return
        if rtn != None:
            print 'item already exists'
            web.conflict()
            return
        
        # now that we have an item that doesn't exist, write it to the dbconn
        try:
            dbConn.write(item._serialized)
        except Exception as ex:
            print 'problem in PUT writing item - ', ex
            web.badrequest()
            return
        
        return json.JSONEncoder().encode(item._serialized)
            

    
    ## def POST(self, jsonitem=None, dbconn=None):
    ##     '''
    ##     dejsonize the supplied item, get a dbconnection, find the corresponding record (POST = Update)
    ##     and do the necessary updates.
    ##     '''
    ##     # the input here can't come on the URL; has to come via the post packaging mechanism
    ##     if not jsonitem: jsonitem = web.input()
    ##     if not dbconn: self._DAL = DataAccessLayer.DataAccessLayer()
        
    ##     assert True==False, "not yet implemented"



class t2dList():
    """
    handles resources that are lists of t2d items
    """
    def GET(self):
        search = web.input()
        # Search criteria must contain the key category
        if 'category' not in search:
            web.badrequest()
            return
        # OK, have a category - is it a valid category?
        if search['category'] not in Item.CATEGORIES:
            web.notfound()
            return
        # OK, have a valid category, did we get either lat/lon or address?
        if 'address' not in search:
            if 'lat' not in search and 'lon' not in search:
                web.badrequest()
                return
            else:
                # no address, but we do have the lat/lon
                try:
                    rtn = getByKeys(None, {'lat':search['lat'], 'lon':search['lon']})
                except:
                    web.internalerror()
                    return
                web.header('Content-Type', 'text/plain')
                return json.JSONEncoder().encode(rtn)
        else:
            # did get address, look for that
            try:
                rtn = getByKeys(None, {'category':search['category'], 'address':search['address']})
            except:
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

if __name__ == "__main__": t2dApp.run()

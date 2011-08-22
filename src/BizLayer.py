'''
Created on Jul 18, 2011

@author: papabear
'''
import DataAccessLayer
import Item
import sys
import web
import json

urls = ('/', 'BizLayer')
app = web.application(urls, globals())

class BizLayer():
    '''
    The top level API layer. Implements the REST interface. Creates Items,
    reads/writes from/to the DataAccessLayer. receives json, converts to
    Item, does some operation with the item (like uses it in a read or write
    call to the DAL), gets some item(s) back, puts this into a json and
    ships it back.

    URIs: (1) item, (2) collection of items
    Format: JSON - value is string, unless otherwise noted
     item = {"pk":value , "name":value , "category":value , "createdBy":value ,
             "address":value , "lat":float_value, "lon":float_value, "phone":value ,
             "email":value , "url":value , "description":value , "rating":value
             "reviews": [{"review":value} , {"review":value} , ...]}
     itemList = [item , item, item ...]

     item GET item format, status codes 200, 400, 404, 500
     item POST item format status codes 200, 400, 403, 500
       -> Semantically, POST = Update
     item PUT item format status codes 200, 400, 403, 500
       -> Semantically, PUT = Create
     item DELETE item format status codes 200, 400, 403, 500
     itemList GET itemList format status codes 200, 400, 403, 500
     itemList POST/PUT/DELETE: status codes 403
     -> Only allowed to create/update/delete individual items, not collections
     
    
    '''

    def GET(self, criteria=None, dbconn=None):
        '''
        dejsonize the critieria, get a db connection, search for the criteria, get a list of
        matching items back, json-ize them, send them back to the client
        '''
        if not criteria: criteria = web.input()
        if not dbconn: self._DAL = DataAccessLayer.DataAccessLayer()
        
        # turn the criteria into an Item.searchFor, then into a where clause
        # using dbconn, read using the where clause
        searchFor = Item.SearchFor()
        lookfor = json.JSONDecoder().decode(criteria)
        
        for attr, val in lookfor.iteritems():
            searchFor.setAttr(attr, val)
        where = searchFor.makeWhereClause()
        
        try:
            rtn = dbconn.read(where)
        except:
            print "Unexpected error in read - %s" % sys.exc_info()[0]
            
        # how are status codes set?
        return json.JSONEncoder().encode(rtn)
              

    def POST(self, jsonitem=None, dbconn=None):
        '''
        dejsonize the supplied item, get a dbconnection, find the corresponding record (POST = Update)
        and do the necessary updates.
        '''
        # the input here can't come on the URL; has to come via the post packaging mechanism
        if not jsonitem: jsonitem = web.input()
        if not dbconn: self._DAL = DataAccessLayer.DataAccessLayer()
        
        assert True==False, "not yet implemented"

    def PUT(self, jsonitem=None, dbconn=None):
        '''
        PUT == Create
        djsonize the supplied item, get a dbConnection, see if the item already exists. If it does, fail
        if it doesnt, insert it.
        '''
        # the input here can't come on the URL; has to come via the post packaging mechanism
        if not jsonitem: jsonitem = web.input()
        if not dbconn: self._DAL = DataAccessLayer.DataAccessLayer()
        # make an item and populate the attributes from the passed data
        item = Item.ThingToDo()
        itemData = json.JSONDecoder().decode(jsonitem)
        
        if 'lat' in itemData and 'lon' in itemData:
            itemData['latlon'] = Item.LatLon(itemData['lat'], itemData['lon'])
            
        # name, category and createdBy are required
        if not ('name' in itemData and 'category' in itemData and 'createdBy' in itemData):
            raise AttributeError
        
        otherArgs = {}
        for attr, val in itemData.iteritems():
            if attr == 'name' or attr == 'category' or attr == 'createdBy':
                # remove from the dict so that what remains is what setAttrs expects for keyword args
                continue
            if attr == 'lat' or attr == 'lon': continue
            otherArgs[attr] = val
        item.setAttrs(itemData['name'], itemData['category'], itemData['createdBy'], **otherArgs)
        
        # If the item already exists, that's an error - caller should be using POST, not PUT
        # Make the PK and see if it exists. AttributeError if it does
        PK = Item.genPK(itemData['name'], itemData['category'])
        searchFor = Item.SearchFor()
        searchFor.setAttr('pk', PK)
        where = searchFor.makeWhereClause()
        
        try:
            rtn = dbconn.read(where)
        except:
            print "Unexpected error in checking for existing record - %s" % sys.exc_info()[0]
            return
        if rtn != None:
            raise AttributeError
            return
        
        # now that we have an item that doesn't exist, write it to the dbconn
        try:
            dbconn.write(item._pk, item._serialized)
        except:
            print "problem in PUT writing item - %s" % sys.exc_info()[0]
        
        return json.JSONEncoder().encode(item._serialized)
            
        
        
        
    def DELETE(self, criteria):
        '''
        dejsonize the criteria, get a dbconn, search for the criteria. If the search matches more than
        one record - error... can only delete a single record. If the search matches a single record,
        delete it
        '''
        pass

        
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


if __name__ == "__main__": app.run()

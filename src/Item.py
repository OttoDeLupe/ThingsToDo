'''
Created on Jun 28, 2011

@author: papabear
'''

CATEGORIES = ["Recreational", "Cultural", "Historical"]

def genPK(name, category):
    '''
    Make a primary key from the name and category
    '''
    return "||" + name + "||" + category + "||"
    
class ThingToDo(): 
    '''
    Biz logic representation of the thing that gets passed between client & server
    gets serialized to persist it. Since serialization happens during construction, 
    means that an instance is immutable.
    '''
    
    def __init__(self):
        self._serialized = {}

    def setAttrs (self, *reqd_args, **keywords): 
        self._serialized['name']      = reqd_args[0]
        self._serialized['category']  = reqd_args[1]
        self._serialized['createdBy'] = reqd_args[2]
        if 'address' in keywords: self._serialized['address'] = keywords['address'] 
        if 'phone'   in keywords: self._serialized['phone']   = keywords['phone'] 
        if 'email'   in keywords: self._serialized['email']   = keywords['email']   
        if 'url'     in keywords: self._serialized['url']     = keywords['url']    
        if 'descr'   in keywords: self._serialized['descr']   = keywords['descr'] 
        if 'rating'  in keywords: self._serialized['rating']  = keywords['rating']   
        if 'review'  in keywords: self._serialized['review']  = keywords['review']
        if 'latlon'  in keywords:
            self._serialized['lat'] = keywords['latlon']._lat
            self._serialized['lon'] = keywords['latlon']._lon
          
        # Either address or lat/lon is required
        if ('address' not in self._serialized) and ('lat' not in self._serialized) and ('lon' not in self._serialized):
            raise AttributeError, "One of address or latlon required"
        
        if self._serialized['category'] not in CATEGORIES:
            raise AttributeError,"Invalid category"
        
        # Uniqueness is defined by concatenating the name&category 
        # strings and using this as the "primary key"
        self._serialized['pk'] = genPK(self._serialized['name'], self._serialized['category'])

    def getName(self):
        return self._serialized['name']
    def getCategory(self):
        return self._serialized['category']
    def getCreatedBy(self):
        return self._serialized['createdBy']
    def getAddress(self):
        return self._serialized['address']
    def getPhone(self):
        return self._serialized['phone']
    def getEmail(self):
        return self._serialized['email']
    def getDescr(self):
        return self._serialized['descr']
    def getUrl(self):
        return self._serialized['url']
    def getRating(self):
        return self._serialized['rating']
    def getReview(self):
        return self._serialized['review']
    def getLatLon(self):
        return LatLon(self._serialized['lat'], self._serialized['lon'])
    
class LatLon():
    def __init__(self,lat,lon):
        self._lat = lat
        self._lon = lon
        
    def boundingBox(self, offset):
        '''
        set a list of lat/lon pairs, [[LATmax, LONmin],[LATmin, LONmin],[LATmax,LONmax],[LATmin, LONmax]]
        based on the offset (in miles) passed, with self._lat and self._lon as the center to the box.
        Use a simple xMiles = yDecimalDegrees to do the arithmetic
        ''' 
        # simple conversion formula: 0.0145 degrees per mile
        # LATmax = _lat + 0.0145 * offset, LONmax = _lon + 0.0145 * offset 
        # use minus to get LAT, LON min
        conversionFactor = 0.0145
        offsetFactor = conversionFactor * offset
        self._box = []
        self._box.append([(self._lat + offsetFactor), (self._lon - offsetFactor)]) # LATmax, LONmin
        self._box.append([(self._lat - offsetFactor), (self._lon - offsetFactor)]) # LATmin, LONmin
        self._box.append([(self._lat + offsetFactor), (self._lon + offsetFactor)]) # LATmax, LONmax
        self._box.append([(self._lat - offsetFactor), (self._lon + offsetFactor)]) # LATmin, LONmax
        
    def getLATmax(self):
        assert(self._box)
        return self._box[0][0]
    def getLATmin(self):
        assert(self._box)
        return self._box[1][0]
    def getLONmax(self):
        assert(self._box)
        return self._box[2][1]
    def getLONmin(self):
        assert(self._box)
        return self._box[0][1]
        
class SearchFor():
    '''
    encapsulate the dict that serves as the search criteria
    '''
    def __init__(self):
        self._criteria = {}
    
    def setAttr(self, attr, val):
        self._criteria[attr] = val
        
    def getAttr(self, attr):
        return self._criteria[attr]
    
    def makeWhereClause(self):
        selectStr = ""
        # check to see if theres a latlon attr. 
        # If so, there must be a offset attr; otherwise throw exception
        if 'latlon' in self._criteria:
            assert('offset' in self._criteria)
            ll = self._criteria['latlon']
            ll.boundingBox(self._criteria['offset'])

            selectStr += 'lat between \"%f\" and \"%f\" and lon between \"%f\" and \"%f\"' % \
                (ll.getLATmax(), ll.getLATmin(), ll.getLONmax(), ll.getLONmin())
         
        for attr, val in self._criteria.iteritems():
            if attr == 'latlon' or attr == 'offset':
                continue # handled these above
            if selectStr == '':
                selectStr += '%s = \"%s\"' % (attr, val)
            else:
                selectStr += ' and %s = \"%s\"' % (attr, val)
        return selectStr

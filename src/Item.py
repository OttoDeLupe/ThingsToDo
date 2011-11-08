'''
Created on Jun 28, 2011

@author: papabear
'''
import uuid
import binascii
import logging

CATEGORIES = ["Recreational", "Cultural", "Historical"]

def genPK(name, category):
    '''
    Make a primary key from the name and category
    '''
    # pad out name to min of 15 characters so we get a key long enough
    # to create the UUID
    while len(name) < 15:
        name = name + name
        
    key = binascii.hexlify("%d%s" % (CATEGORIES.index(category), name[0:15]))
    return str(uuid.UUID(key))
    
class ThingToDo(): 
    '''
    Biz logic representation of the thing that gets passed between client & server
    gets serialized to persist it. Since serialization happens during construction, 
    means that an instance is immutable.
    '''
    
    def __init__(self):
        logging.info('Item - new item')
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
        if 'lat'     in keywords: self._serialized['lat']     = keywords['lat']
        if 'lon'     in keywords: self._serialized['lon']     = keywords['lon']
          
        # Either address or lat/lon is required
        if ('address' not in self._serialized) and ('lat' not in self._serialized) and ('lon' not in self._serialized):
            logging.error('Item-setAttrs - one of address or lat/lon required')
            raise AttributeError, "One of address or latlon required"
        
        if self._serialized['category'] not in CATEGORIES:
            logging.error('Item-setAttrs - category (%s) not in CATEGORIES', self._serialized['category'])
            raise AttributeError,"Invalid category"
        
        # Uniqueness is defined by concatenating the name&category 
        # strings and using this as the "primary key"
        self._serialized['pk'] = genPK(self._serialized['name'], self._serialized['category'])

    def setAttribute(self, attr, val):
        if attr not in self._serialized:
            logging.error('Item-setAttribute - %s not a valid attribute', attr)
            raise KeyError 
        else:
            if attr in ('name', 'category','createdBy'):
                logging.error('Item-setAttribute - trying to reset name, category or createdBy')
                raise AttributeError
            else:
                self._serialized[attr] = val
        
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
    def getLat(self):
        return self._serialized['lat'] 
    def getLon(self):
        return self._serialized['lon']
    
class LatLon():
    def __init__(self,lat,lon):
        # yeah yeah... this is poor polymorphism, but this can be called with
        # strings or floats. And conversions have to happen based on the
        # data type passed.
        if type(lat) == str and type(lon) == str:
            self._latFloat = float(lat)
            self._lonFloat = float(lon)
        elif type(lat) == float and type(lon) == float:
            self._latFloat = lat
            self._lonFloat = lon
        else:
            raise AttributeError
                    
        self._lat = self.toComparableString(self._latFloat)
        self._lon = self.toComparableString(self._lonFloat)
        self._box = []
        
    def toComparableString(self, number):
        return str(int(number*1000000))
        
    def boundingBox(self, offset):
        '''
        set a list of lat/lon pairs, [[LATmax, LONmin],[LATmin, LONmin],[LATmax,LONmax],[LATmin, LONmax]]
        based on the offset (in miles) passed, with self._lat and self._lon as the center to the box.
        Use a simple xMiles = yDecimalDegrees to do the arithmetic
        Need to have these stored as strings (that can be lexicographically compared) so that SimpleDB
        comparisons can be done.
        ''' 
        # simple conversion formula: 0.0145 degrees per mile
        # LATmax = _lat + 0.0145 * offset, LONmax = _lon + 0.0145 * offset 
        # use minus to get LAT, LON min
        conversionFactor = 0.0145
        offsetFactor = conversionFactor * offset

        self._box.append([self.toComparableString(self._latFloat + offsetFactor), 
                          self.toComparableString(self._lonFloat - offsetFactor)]) # LATmax, LONmin
        self._box.append([self.toComparableString(self._latFloat - offsetFactor), 
                          self.toComparableString(self._lonFloat - offsetFactor)]) # LATmin, LONmin
        self._box.append([self.toComparableString(self._latFloat + offsetFactor), 
                          self.toComparableString(self._lonFloat + offsetFactor)]) # LATmax, LONmax
        self._box.append([self.toComparableString(self._latFloat - offsetFactor), 
                          self.toComparableString(self._lonFloat + offsetFactor)]) # LATmin, LONmax
        
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
        selectStr = ''
        # check to see if theres a latlon attr. 
        # If so, there must be a offset attr; otherwise throw exception
        if 'lat' in self._criteria or 'lon' in self._criteria:
            if 'offset' not in self._criteria:
                raise AttributeError
            
            lat = self._criteria['lat']
            lon = self._criteria['lon']
            ll = LatLon(lat, lon)
            ll.boundingBox(self._criteria['offset'])

            selectStr += 'lat between %s and %s and lon between %s and %s' % \
                (ll.getLATmax(), ll.getLATmin(), ll.getLONmax(), ll.getLONmin())
           # logging.debug('makeWhereClause(1): %s', selectStr)
            
        for attr, val in self._criteria.iteritems():
            if attr == 'lat' or attr == 'lon' or attr == 'offset':
                continue # handled these above
            if selectStr == '':
                selectStr += '%s = \"%s\"' % (attr, val)
            else:
                selectStr += ' and %s = \"%s\"' % (attr, val)
            # logging.debug('makeWhereClause(2): %s', selectStr)
            
        #logging.debug('makeWhereClause(3): %s', selectStr)
        return selectStr

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
        self._serialized = None
        self._pk = None
        self._name = None
        self._category = None
        self._createdBy = None
        self._address = None
        self._latlon = None
        self._phone = None
        self._email = None
        self._url = None
        self._descr = None
        self._rating = None
        self._reviews = None

    def serialize(self):
        self._serialized = {}
        if self._name:      self._serialized['name'] = self._name
        if self._category:  self._serialized['category'] = self._category
        if self._createdBy: self._serialized['createdBy'] = self._createdBy
        if self._address:   self._serialized['address'] = self._address
        if self._latlon:
            self._serialized['lat'] = self._latlon._lat
            self._serialized['lon'] = self._latlon._lon
        if self._phone:     self._serialized['phone'] = self._phone
        if self._email:     self._serialized['email'] = self._email
        if self._url:       self._serialized['url'] = self._url
        if self._descr:     self._serialized['descr'] = self._descr
        if self._rating:    self._serialized['rating'] = self._rating
        if self._reviews:   self._serialized['reviews'] = self._reviews


             
      
    def setAttrs (self, *reqd_args, **keywords): 
        self._name = reqd_args[0]
        self._category = reqd_args[1]
        self._createdBy = reqd_args[2]
        if keywords.has_key('address'): self._address = keywords['address']
        if keywords.has_key('latlon'):  self._latlon = keywords['latlon']
        if keywords.has_key('phone'):   self._phone = keywords['phone']
        if keywords.has_key('email'):   self._email = keywords['email']
        if keywords.has_key('url'):     self._url = keywords['url']
        if keywords.has_key('descr'):   self._descr = keywords['descr']
        if keywords.has_key('rating'):  self._rating = keywords['rating']
        if keywords.has_key('reviews'): self._reviews = keywords['reviews']
        
        if self._address == None and self._latlon == None:
            raise AttributeError, "One of address or latlon required"
        
        if self._category not in CATEGORIES:
            raise AttributeError,"Invalid category"
        
        # Uniqueness is defined by concatenating the name&category 
        # strings and using this as the "primary key"
        self._pk = genPK(self._name, self._category)
        self.serialize()


   
  
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
        if self._criteria.has_key('latlon'):
            assert(self._criteria.has_key('offset'))
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

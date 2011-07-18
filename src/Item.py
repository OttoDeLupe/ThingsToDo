'''
Created on Jun 28, 2011

@author: papabear
'''

CATEGORIES = ["Recreational", "Cultural", "Historical"]

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
        
    def setAttrs (self, name, category, createdBy, address=None, latlon=None, phone=None, email=None, url=None, descr=None, rating=None, reviews=None):
        self._name = name
        self._category = category
        self._createdBy = createdBy
        self._address = address
        self._latlon = latlon
        self._phone = phone
        self._email = email
        self._url = url
        self._descr = descr
        self._rating = rating
        self._reviews = reviews
        
        if address == None and latlon == None:
            raise AttributeError, "One of address or latlon required"
        
        if category not in CATEGORIES:
            raise AttributeError,"Invalid category"
        
        # Uniqueness is defined by concatenating the name&category 
        # strings and using this as the "primary key"
        self._pk = "||" + self._name + "||" + self._category + "||"
        self._serialized = dict(name=self._name,
                                category=self._category,
                                createdBy=self._createdBy,
                                address=self._address,
                                lat = (self._latlon._lat if self._latlon else None),
                                lon = (self._latlon._lon if self._latlon else None),
                                phone=self._phone,
                                email=self._email,
                                url=self._url,
                                descr=self._descr,
                                rating=self._rating,
                                reviews=self._reviews)    
        
        def serialize(self):
            self._serialized = dict(name=self._name,
                                    category=self._category,
                                    createdBy=self._createdBy,
                                    address=self._address,
                                    lat = (self._latlon._lat if self._latlon else None),
                                    lon = (self._latlon._lon if self._latlon else None),
                                    phone=self._phone,
                                    email=self._email,
                                    url=self._url,
                                    descr=self._descr,
                                    rating=self._rating,
                                    reviews=self._reviews)  

        
   
  
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
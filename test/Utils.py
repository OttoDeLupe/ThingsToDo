'''
Created on Aug 23, 2011

@author: papabear
'''

import csv
import Item

def listify(data):
    ''' take a string and turn it into a single item list'''
    if data == '': 
        return []
    else:
        return [data]

class Utils():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._testData = []

        for newRec in csv.DictReader(open("TestData.csv", 'rb'), delimiter=','):
            newRec['pk'] = Item.genPK(newRec['name'], newRec['category'])
            newRec['review'] = listify(newRec['review'])
            # convert lat / lon to floats : float('str')
            # If already have the PK, append to the existing review entry
            if not self._testData:
                self._testData.append(newRec)
            else:
                existingUpdated = False
                for existingRec in self._testData:
                    if (existingRec['pk'] == newRec['pk']) and newRec['review']:
                        existingRec['review'].append(newRec['review'][0])
                        existingUpdated = True
                if not existingUpdated:
                    self._testData.append(newRec)

        
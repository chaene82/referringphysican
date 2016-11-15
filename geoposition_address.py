#!/usr/bin/python3

# *********************************************** #
# Geocoding Adresses                              #
# -------------------------                       #
#                                                 #
# Author:   christoph.haene@gmail.com             #
# Date:     10.11.2016                            #
# Version:  0.4                                   #
# *********************************************** #

# Import Modules
import geocoder
import time
import logging
import pandas as pd


# initial Logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


# function get_geocode 
# connect to google maps and get geo position for an address


def get_geocode(address):
    logger.debug('Searching Geoposition for %s' , address)
    g = geocoder.osm(address)
    logger.info('Geoposition %s', g.geojson)
    time.sleep(0.5)
    return g 
    


addresses = pd.read_csv("data/addresses_geo_1000.csv")


address = ''


for idx in addresses.index:
    
    if idx > 1000:
        
        logger.info('New address number  %s', idx)
        
        
        
        if idx % 50 == 0:
            print('\n ' + str(idx) + ' records generated')
    
        street  = addresses['Strasse'][idx]
        plz     = addresses['PLZ'][idx]
        ort     = addresses['Ort'][idx]
        add_new = street + ', ' + str(plz) + ', ' + str(ort)
        if(address.upper() == add_new.upper()):
           logger.info('address drop, dublicate  %s', address)
           addresses = addresses.drop(idx) 
           address = ''
    
        else:
           address = add_new
           logger.debug('address read  %s', address) 
           
           g = get_geocode(address)
     
        
           if( g.ok == False):
                logger.warning('drop row  %s', idx)      
                addresses = addresses.drop(idx) 
           else:
                logger.debug('write dataset  %s', g.lat)
                addresses.set_value(idx, 'lat', g.lat)
                addresses.set_value(idx, 'lng', g.lng)
        
        
        if idx > 1001 and idx % 1000 == 0:       
             addresses.to_csv("data/addresses_geo_" + str(idx) + ".csv")
             logger.warning('wrote file')      

   
addresses.to_csv("data/addresses_geo.csv")
logger.warning('wrote file and finish  %s', addresses)      
         
         
#g = get_geocode('Julie-Bikle-Strasse 33, 8406 Winterhur')    
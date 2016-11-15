#!/usr/bin/python3

# *********************************************** #
# SIMULATION OF A Kampagne                        #
# -------------------------                       #
#                                                 #
# Author:   christoph.haene@gmail.com             #
# Date:     11.11.2016                            #
# Version:  0.1                                   #
# *********************************************** #

# import Modules

from datetime import timedelta
import pandas as pd


# initial Logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Methode




# Prgramm

# Create pandas




def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
        

# Select Date for Kampagne

for single_date in daterange(start_date, end_date):
    date_id = np.random.randint(0,80)
    if date_id % 80 == 59:
        # Day of a Kampagne
        
        


# Define the Kampagne

# Select doctors for the Kampagne



        

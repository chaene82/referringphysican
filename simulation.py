#!/usr/bin/python3

# *********************************************** #
# SIMULATION OF A TREATMENT                       #
# -------------------------                       #
#                                                 #
# Author:   christoph.haene@gmail.com             #
# Date:     25.10.2016                            #
# Version:  0.1                                   #
# *********************************************** #

# Import Modules
import numpy as np
import csv
from datetime import timedelta, date


# Define Classes

class Treatment(object):
   id = 0
   patientId = 0
   doctorId = 0
   treatmentDate = 0
   referalDate = 0
   referaliClinic = 0
   emergency = 0
   insured = 0 
   hospitalStartDate = 0
   hospitalEndDate = 0
   medicalReportDate = 0
   structuredDataTrasfer = 0
   drg = 0
   cost = 0
   revenue = 0


   def __init__(self):
      self.id = get_treatment_number()
      self.patientId = get_patient_number()
      self.doctorId = get_doctor_number()

   def add_treatment_date(self, date):
      self.treatmentDate = date

   def add_referal(self, date, emercency_flag):
      if emercency_flag == 0:
         delta = np.random.randint(0,5 + 1)
         self.referalDate = date + timedelta(days=delta)
      elif emercency_flag == 1:
         delta = np.random.randint(0,2 + 1)
         self.referalDate = date + timedelta(days=delta)
      elif emercency_flag == 2:
         self.referalDate = date
      self.clinic = get_clinic()

   def add_emercency(self, date):
      self.emercency = get_emercency(date)
      
   def add_insured(self):
      self.insured = get_insured()


class Clinic(object):
   id = 0
   name = ''
   beds = 0

   def __init__(self, id, name, beds):
       self.id = id
       self.name = name
       self.beds = beds

class Hospital(object):
   name = ''

   def __init__(self):
       self.name = 'hospital'

   def get_next_free_date(self, treatment):
       if treatment.emercency != 0:
          return treatment.referalDate
       else:
          return treatment.referalDate + timedelta(np.random.randint(5,20 + 1))

   def add_hospital_stay(self, treatment):
       treatment.duration = np.random.randint(5,20 + 1)
       treatment.hospitalEndDate = treatment.hospitalStartDate + timedelta(treatment.duration)
       treatment.medicalReportDate = treatment.hospitalEndDate +  + timedelta(np.random.randint(5,20 + 1))
       return treatment

class DRG(object):
    name = ''

    def __init__(self):
       self.name = 'DRG 2016'

    def get_drg(self, treatment):
       treatment.drg = np.random.randint(0,1000 + 1)
       treatment.cost = np.random.randint(5000,15000 + 1)
       treatment.revenue = np.random.randint(5100,15800 + 1)

       return treatment

# Define Functions
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def initial():
   global treatmentNumber
   treatmentNumber = 0

def get_treatment_number():
   global treatmentNumber
   treatmentNumber += 1
   return treatmentNumber

def get_patient_number():
   return np.random.randint(1, 20000)

def get_doctor_number():
   return np.random.randint(1, 200)

def get_clinic():
   clinic = [1,2,3,4,5,6,7,8,9,10]
   weights = [0.4, 0.3, 0.1, 0.05, 0.05, 0.05, 0.02, 0.02, 0.005, 0.005]
   return np.random.choice(clinic, p=weights)

def get_emercency(date):
   emercency = [0,1,2]
   weights = [0.8, 0.1, 0.1]
   return np.random.choice(emercency, p=weights)
   
def get_insured():
   insured = [0,1,2]
   weights = [0.8, 0.1, 0.1]
   return np.random.choice(insured, p=weights)


# Initial variables
initial()
start_date = date(2013, 1, 1)
end_date = date(2016, 10, 31)
dataArray = []

ofile  = open('data/treatment.csv', 'w')
writer = csv.writer(ofile, delimiter=',' )
csvData = [['id', 'patientId', 'doctorId', 'emergencyId', 'insuredId', 'treatmentDate', \
            'referaldate', 'clinicId', 'hospitalStartDate', 'hospitalEndDate', \
            'duration','medicalReportDate','drgId','cost', 'revenue']]
writer.writerows(csvData)

hospital = Hospital()
drg = DRG()

# Simulate a Treatment

for single_date in daterange(start_date, end_date):

   # define number of treatment a day
   treatment_a_day = np.random.randint(15, 30)
   for i in range(0, treatment_a_day ):
     treatment = Treatment()
     treatment.add_treatment_date(single_date)
     treatment.add_emercency(single_date)
     treatment.add_insured()
     treatment.add_referal(treatment.treatmentDate, treatment.emercency)


     treatment.hospitalStartDate = hospital.get_next_free_date(treatment)
     treatment = drg.get_drg(treatment)
     treatment = hospital.add_hospital_stay(treatment)


     #print('\n --> New treatment for date ' +  single_date.strftime("%Y-%m-%d"))
     #print('ID         ' + str(treatment.id))
     #print('Patient    ' + str(treatment.patientId))
     #print('Doctor     ' + str(treatment.doctorId))
     #print('T-Date     ' + str(treatment.treatmentDate))
     #print('Emercency  ' + str(treatment.emercency))
     #print('R-Date     ' + str(treatment.referalDate))
     #print('Clinic     ' + str(treatment.clinic))
     #print('S-Date     ' + str(treatment.hospitalStartDate))
     #print('E-Date     ' + str(treatment.hospitalEndDate))
     #print('Duration   ' + str(treatment.duration))
     #print('Rep-Date   ' + str(treatment.medicalReportDate))
     #print('DRG        ' + str(treatment.drg))
     #print('Costs      ' + str(treatment.cost))

     if treatment.id % 1000 == 0:
        print('\n ' + str(treatment.id) + ' records generated')

     csvData = [treatment.id, treatment.patientId, treatment.doctorId, treatment.emercency, treatment.insured, \
                treatment.treatmentDate, treatment.referalDate, treatment.clinic, treatment.hospitalStartDate, \
                treatment.hospitalEndDate, treatment.duration, treatment.medicalReportDate, \
                treatment.drg, treatment.cost, treatment.revenue]
     writer.writerow(csvData)

ofile.close

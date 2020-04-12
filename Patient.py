#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:45:41 2020

@author: simonugor
"""

import uuid
from random import randrange
class Patient:
    def __init__(self, name, dob):
        self.ID = uuid.uuid1()
        self.name = name
        self.dob = dob 
        self.diagnosis = "Not tested"
        self.inQ = None
        self.inH = None
        self.discharged = None
    
    def serialize(self):
        return {
            'id': self.ID, 
            'name': self.name, 
            'dob': self.dob,
            'diagnosis': self.diagnosis,
            'in quarantine': self.inQ,
            'in hospital': self.inH,
        }

    def serialize_diagnosis(self):
        return {
            'diagnosis': ("Patient was tested " + str(self.diagnosis) + ".")
        }
    
    
    def diagnosis_(self):
        #using varieble x to randomly select number between 0 and 9
        x = randrange(10)
        print(x)
        #if x == 0 (10%), our patient is diagnosed positive
        if x == 0:
            self.diagnosis = "positive"
        #if it is any other number (90%), patient is diagnosed negative
        else:
            self.diagnosis = "negative"
        return self.diagnosis
            
            
    def cure(self):
        #using variable c to randomly select number betweet 0 and 99
        c = randrange(100)
        print(c)
        if c == 0 or c == 1 or c == 2:
            self.diagnosis = "dead"
            return "died"
        else:
            self.diagnosis = "negative"
            self.discharged = "discharged"
            return "cured"
            
    def addInQ(self, quarantine):
        self.inQ = quarantine
        #print(self.inQ)
    
    def addInH(self, hospital):
        self.inH = hospital
        
    def dischargeFromQ(self, quarantine):
        self.inQ = None
        
    def dischargeFromH(self, hospital):
        self.inH = None
    
    
    
    
    
            
            
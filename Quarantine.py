#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 19:32:41 2020

@author: simonugor
"""

import uuid

class Quarantine:
    def __init__(self, name, capacity):
        self.ID = uuid.uuid1()
        self.name = name
        self.capacity = int(capacity)
        self.patients = []
        
    def occupancy (self):         
        return 100* len(self.patients) / self.capacity 
    
    def addPatient (self, patient):
        self.patients.append(patient)
        print(self.patients)
        
    def dischargePatient(self, patient):
        self.patients.remove(patient)
        print(self.patients)
    
    
    def serialize(self):
        return {
            'id': self.ID, 
            'name': self.name, 
            'capacity': self.capacity,
            'occupancy': self.occupancy(),
        }
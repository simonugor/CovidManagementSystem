#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:44:50 2020

@author: simonugor
"""

from Patient import Patient
import uuid
class Hospital:
    def __init__(self, name, capacity):
        self.ID= uuid.uuid1()
        self.name = name
        self.capacity = int (capacity) 
        self.patients = [] # List of patients admitted to the hospital 
        self.staff = [] # List of doctors and nurses working in the hospital
        self.number_of_staff = None
    
    # return the percentage of occupancy of this hospital 
    def occupancy (self):         
        return 100* len(self.patients) / self.capacity
    
    # admit a patient to the hospital of given name and date of birth 
    def admission (self, name, dob):         
        p = Patient (name, dob)
        self.patients.append(p)
        message = "New Patient added."
        
    def add_staff(self, staff_to_add):
        print("add_staff responding")
        self.staff.append(staff_to_add)
        print(len(self.staff))
        
    def addPatient (self, patient):
        self.patients.append(patient)
        print(self.patients)
        
    def dischargePatient(self, patient):
        self.patients.remove(patient)
        print(self.patients)
        
    
    def serialize(self):
        self.number_of_staff = len(self.staff)
        return {
            'id': self.ID, 
            'name': self.name, 
            'capacity': self.capacity,
            'occupancy': self.occupancy(),
            'staff members': self.number_of_staff
        }
    

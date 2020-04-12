#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 01:06:30 2020

@author: simonugor
"""

import uuid
class Staff:
    def __init__(self, name, dob, type_):
        self.ID = uuid.uuid1()
        self.name = name
        self.dob = dob 
        self.type_ = type_
        self.works_in = None
        
    def assign_staff(self, hospital):
        print("assign_staff responding")
        self.works_in = hospital
        print(self.works_in)
    
    
    def serialize(self):
        return {
            'id': self.ID, 
            'name': self.name, 
            'dob': self.dob,
            'type': self.type_,
            'works in': self.works_in
        }
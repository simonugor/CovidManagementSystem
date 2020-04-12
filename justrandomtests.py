#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 01:15:13 2020

@author: simonugor
"""
from random import randrange

class patient:
    def __init__(self, name):
        self.name = name
        self.diagnosis = ""
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
        
    def print_diagnosis(self):
        print(self.diagnosis)
        
    def return_test(self):
        return "Hey im returning a string!"
        
        
#pat1 = patient("janko")
#pat1.diagnosis_()
#pat1.print_diagnosis()
#pat1.return_test()

x = "hospital"

def checkifPorQ(x):
    if x == "hospital":
        return "hospital"
    else:
        return "quarantine"
        
def addinHospital():
    test = checkifPorQ(x)
    if test == "hospital":
        print("HOSPITAL!")
    else:
        print("Quaranitne!")
        
#addinHospital()
        
test = []
print(len(test))   
     
        
q = ["q2", "q2", "q3"]
for i in range(len(q)):
    if q[i] == "q2":
        print("got it")
        break
    





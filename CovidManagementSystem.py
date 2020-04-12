#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:43:32 2020

@author: simonugor
"""

from Hospital import *
from Patient import *
from Quarantine import *
from Staff import *

class CovidManagementSystem:    
    def __init__(self):
        self.hospitals = [] #list of hospitals known to the system
        self.quarantines = [] #list of quarantines known to the system
        self.patients = [] #list of patients known to the system
        self.staff = [] #list of all staff know to the system
    
    def get_stats_hospital(self):
        try:
            patients_in_hospitals = 0
            capacity_of_hospitals = 0
            for h in self.hospitals:
                patients_in_hospitals = patients_in_hospitals + len(h.patients)
            for h in self.hospitals:
                capacity_of_hospitals = capacity_of_hospitals + h.capacity
            occupancy = (patients_in_hospitals/capacity_of_hospitals)*100
            return occupancy
        except ZeroDivisionError:
            return 0
        
    def get_stats_quarantine(self):
        try:
            patients_in_quarantines = 0
            capacity_of_quarantines = 0
            for q in self.quarantines:
                patients_in_quarantines = patients_in_quarantines + len(q.patients)
            for q in self.quarantines:
                capacity_of_quarantines = capacity_of_quarantines + q.capacity
            occupancy = (patients_in_quarantines/capacity_of_quarantines)*100
            return occupancy
        except ZeroDivisionError:
            return 0
        
    
    def get_stats_patients(self):
        try:
            patients_positive = 0
            patients_negative = 0
            patients_not_tested = 0
            positive_negative_nottested = []
            for p in self.patients:
                if p.diagnosis == "positive":
                    patients_positive = patients_positive + 1
                elif p.diagnosis == "negative":
                    patients_negative = patients_negative + 1
                elif p.diagnosis == "Not tested":
                    patients_not_tested = patients_not_tested + 1
                
                total = patients_positive + patients_negative + patients_not_tested
                positive_perc = (patients_positive/total)*100
                negative_perc = (patients_negative/total)*100
                not_tested_perc = (patients_not_tested/total )*100               
                
                positive_negative_nottested.append(patients_positive)
                positive_negative_nottested.append(patients_negative)
                positive_negative_nottested.append(patients_not_tested)
                
                positive_negative_nottested.append(positive_perc)
                positive_negative_nottested.append(negative_perc)
                positive_negative_nottested.append(not_tested_perc)
 
                print(positive_negative_nottested)
                return(positive_negative_nottested)
                #returning a list with all values i need for stats
        except:
            return 0
        
    def patient_status(self):
        try:
            in_quarantine = 0
            in_hospital = 0
            dead_patients = 0
            discharged_patients = 0
            inQ_inH_dead_discharged = []
            for p in self.patients:
                if p.inQ != None:
                    in_quarantine = in_quarantine + 1
                elif p.inH != None:
                    in_hospital = in_hospital + 1
            for p in self.patients:
                if p.diagnosis == "dead":
                    dead_patients = dead_patients + 1
            for p in self.patients:
                if p.discharged == "discharged":
                    discharged_patients = discharged_patients + 1
                    
            #returnn a list with all data i need for stats
            inQ_inH_dead_discharged.append(in_quarantine)   
            inQ_inH_dead_discharged.append(in_hospital)
            inQ_inH_dead_discharged.append(dead_patients)
            inQ_inH_dead_discharged.append(discharged_patients)
            print(inQ_inH_dead_discharged)
            return inQ_inH_dead_discharged
        except:
            return 0
        
        
        
    #picking quarantine for positive patients to be placed in
    def pick_q(self):
        print("Picking quarantine")
        if len(self.quarantines) != 0:
            for q in self.quarantines:
                if len(q.patients) < q.capacity:
                    return q.ID
        return None
    
    #picking hospital for positive patients to be placed in
    def pick_h(self):
        print("Picking hospital")
        if len(self.hospitals) != 0:
            for h in self.hospitals:
                if len(h.patients) < h.capacity:
                    return h.ID
        return None
    
    #checking if facility is hospital or quarantine
    def checkIfPorQ(self, facility_id):
        print("checking if hospital or quarantine")
        for q in self.quarantines:
            if(str(q.ID)==facility_id):
                return "quarantine"
        for h in self.hospitals:
            if(str(h.ID)==facility_id):
                return "hospital"
            
            
    #adding patient into hospital        
    def addPinH(self, _idh, _idp):
        #print("Added patient in hospital")
        ptrue = None
        htrue = None
        for h in self.hospitals:
            if(str(h.ID)==str(_idh)):
                htrue = h
        for p in self.patients:
            if(str(p.ID)==str(_idp)):
                ptrue = p
        if htrue!=None and ptrue!= None:
            h.addPatient(ptrue)
            p.addInH(htrue.ID)
            return htrue, ptrue
        return None   
    
    #adding patient into quarantine
    def addPinQ(self, _idq, _idp):
        print(_idq, _idp)
        ptrue = None
        qtrue = None
        for q in self.quarantines:
            if(str(q.ID)==str(_idq)):
                qtrue = q
        for p in self.patients:
            if(str(p.ID)==str(_idp)):
                ptrue = p
        if qtrue!=None and ptrue!= None:
            print("I got here")
            q.addPatient(ptrue)
            p.addInQ(qtrue.ID)
            return qtrue, ptrue
        return None
    
    #discharging patient form quarantine
    def dischargePfromQ(self, _idq, _idp):
        print("discharging patient from quarantine")   
        ptrue = None
        qtrue = None
        for q in self.quarantines:
            if(str(q.ID)==str(_idq)):
                qtrue = q
        for p in self.patients:
            if(str(p.ID)==str(_idp)):
                ptrue = p
        if qtrue!=None and ptrue!= None:
            q.dischargePatient(ptrue)
            p.dischargeFromQ(qtrue.ID) 
            return qtrue, ptrue
        return None  

    #discharging patient from hospital              
    def dischargePfromH(self, _idh, _idp):
        print("discharging patient from hospital")   
        ptrue = None
        htrue = None
        for h in self.hospitals:
            if(str(h.ID)==str(_idh)):
                htrue = h
        for p in self.patients:
            if(str(p.ID)==str(_idp)):
                ptrue = p
        if htrue!=None and ptrue!= None:
            h.dischargePatient(ptrue)
            p.dischargeFromH(htrue.ID) 
            return htrue, ptrue
        return None                 
                
                
    
    #adding staff in hospital
    def addStaffinH(self, staff_id, workplace):
        print("addStaff called")
        
        found_staff = None
        found_hospital = None
        
        for h in self.hospitals: 
            if(str(h.ID)==workplace):
                found_hospital = h
                print(found_hospital)
            
        for s in self.staff:
            if(str(s.ID)==staff_id):
                found_staff = s
                print(found_staff)
        
        if found_staff != None and found_hospital != None:
            found_hospital.add_staff(found_staff)
            found_staff.assign_staff(found_hospital.ID)
            return found_hospital, found_staff
        else:
            return None
        
  
    def getHospitals (self): 
        return self.hospitals
    
    def getQuarantines(self):
        return self.quarantines
    
    def getPatients(self):
        return self.patients
    
    def getStaff(self):
        return self.staff
        
    def addHospital (self, name, capacity): 
        h = Hospital (name, capacity)
        self.hospitals.append(h)
        
    def addQuarantine(self, name, capacity):
        q = Quarantine(name, capacity)
        self.quarantines.append(q)
        
    def addPatient(self, name, dob):
        p = Patient(name, dob)
        self.patients.append(p)
        
    def addStaff(self, name, dob, type_):
        s = Staff(name, dob, type_)
        self.staff.append(s)
    
    def getHospitalById(self, id_): 
        for h in self.hospitals: 
            if(str(h.ID)==id_):
                return h
        return None
    
    def getQuarantineById(self, _id):
        for q in self.quarantines:
            if(str(q.ID)==_id):
                return q
        return None
    
    def getStaffById(self, _id):
        for s in self.staff:
            if(str(s.ID)==_id):
                return s
        return None
    
    def getPatientById(self, _id):
        print("getPatientById called")
        for p in self.patients:
            if(str(p.ID)==_id):
                return p
        return None
            
    
    def diagnosePatient(self, _id):
        for p in self.patients:
            if(str(p.ID)==_id):
                diagnosis = p.diagnosis_()
                return diagnosis
        return None
    
    def curePatient(self, _id):
        for p in self.patients:
            if(str(p.ID)==_id):
                if p.diagnosis == "positive":
                    try_cure = p.cure()
                    if try_cure == "cured":
                        return "Patient was cured"
                    elif try_cure == "died":
                        return "Unfrotunatelly, patient died"
        return None
    
    
    def deleteHospital (self, id_):
        h = self.getHospitalById(id_)
        if(h!=None): 
            self.hospitals.remove (h)
        return h!=None                
    
    def deleteQuarantine (self, _id):
        q = self.getQuarantineById(_id)
        if(q!=None): 
            self.quarantines.remove (q)
        return q!=None   
    
    def deleteStaff (self, _id):
        s = self.getStaffById(_id)
        if(s!=None): 
            self.staff.remove (s)
        return s!=None 
    
    
    
    
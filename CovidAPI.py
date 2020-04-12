#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:41:35 2020

@author: simonugor
"""

from flask import Flask, request, jsonify
from CovidManagementSystem import *
from Hospital import * 
from Quarantine import *
from Patient import *

app = Flask(__name__)

# Root object for the management system
ms = CovidManagementSystem ()

#HOSPITAL

#Add a new hospital (parameters: name, capacity). 
@app.route("/hospital", methods=["POST"])
def addHospital():
    ms.addHospital(request.args.get('name'), request.args.get('capacity'))   
    return jsonify(f"Added a new hospital called {request.args.get('name')} with capacity {request.args.get('capacity')}")

#Return the details of a hospital of the given hospital_id. 
@app.route("/hospital/<hospital_id>", methods=["GET"])
def hospitalInfo(hospital_id):       
    h = ms.getHospitalById(hospital_id)
    if(h!=None): 
        return jsonify(h.serialize())
    return jsonify(
            success = False, 
            message = "Hospital not found")

# Admission of a patient to a given hospital 
@app.route("/hospital/<hospital_id>/patient", methods=["POST"])
def admitpatient(hospital_id):       
    h = ms.getHospitalById(hospital_id)
    if(h!=None): 
        h.admission (request.args.get('name'), request.args.get('dob'))
        message = "New patient added"
        success = "true"
    else:
        message = "Hospital not found"
        success = "false"
    return jsonify(
            success = success, 
            message = message)     

    
@app.route("/hospital/<hospital_id>", methods=["DELETE"])
def deleteHospital(hospital_id):
    
    result = ms.deleteHospital(hospital_id)   
    if(result): 
        message = f"Hospital with id{hospital_id} was deleted" 
    else: 
        message = "Hospital not found" 
    return jsonify(
            success = result, 
            message = message)

@app.route("/hospitals", methods=["GET"])
def allHospitals():   
    return jsonify(hospitals=[h.serialize() for h in ms.getHospitals()])


#QUARANTINE
    
#add new quarantine
@app.route("/quarantine", methods = ["POST"])
def addQuarantine():
    ms.addQuarantine(request.args.get("name"), request.args.get("capacity"))
    return jsonify(f"Added a new quarantine called {request.args.get('name')} with capacity {request.args.get('capacity')}")

#return all quarantines
@app.route("/quarantines", methods = ["GET"])
def allQuarantines():
    return jsonify(quarantines=[q.serialize() for q in ms.getQuarantines()])

#return quarantine by ID
@app.route("/quarantine/<quarantine_id>", methods=["GET"])
def quarantineInfo(quarantine_id):       
    q = ms.getQuarantineById(quarantine_id)
    if(q!=None): 
        return jsonify(q.serialize())
    return jsonify(
            success = False, 
            message = "Quarantine not found")

#deleting quarantine by ID
@app.route("/quarantine/<quarantine_id>", methods=["DELETE"])
def deleteQuarantine(quarantine_id):
    
    result = ms.deleteQuarantine(quarantine_id)   
    if(result): 
        message = f"Quarantine with id{quarantine_id} was deleted" 
    else: 
        message = "Quarantine not found" 
    return jsonify(
            success = result, 
            message = message)

#adding patient into quarantine
@app.route("/quarantine/<quarantine_id>/<patient_id>", methods=["POST"])
def addPatientinQuarantine(quarantine_id, patient_id):
    pq = ms.addPinQ(quarantine_id, patient_id)
    if pq!=None:
        return jsonify(
                success = True, 
                message = "Patient with id " + str(patient_id) + " added into Quarantine with id " + str(quarantine_id))
    else:
        return jsonify(
                success = False, 
                message = "Patient or Quarantine not found")        

        
#PATIENT 

#adding new Patient
@app.route("/patient", methods = ["POST"])
def addPatient():
    ms.addPatient(request.args.get("name"), request.args.get("dob"))
    return jsonify(f"Added new patient called {request.args.get('name')} with dob {request.args.get('dob')}")

#getting all patients THIS IS JUST FOR TESTING
@app.route("/patients", methods = ["GET"])
def allPatients():
    return jsonify(patients=[p.serialize() for p in ms.getPatients()])

#admit patient to given facility
@app.route("/patient/<pat_id>/admit/<facility_id>", methods=["PUT"])
def admitPtoF(pat_id, facility_id):
    hospitalOrQuarantine = ms.checkIfPorQ(facility_id)
    p = ms.getPatientById(pat_id)
    if p!=None and hospitalOrQuarantine == "quarantine":
        added_in_q = ms.addPinQ(facility_id, pat_id)
        if added_in_q != None:
            return jsonify("Added patient " + str(pat_id) + " into quarantine " + str(facility_id))
    elif p!=None and hospitalOrQuarantine == "hospital":
        added_in_h = ms.addPinH(facility_id, pat_id)
        if added_in_h != None:
            return jsonify("Added patient " + str(pat_id) + " into hospital " + str(facility_id))
    elif p == None:
        return jsonify("Patient was not found")
    elif hospitalOrQuarantine == None:
        return jsonify("Hospital or Quarantine was not found")
    else: 
        return jsonify("You really messed up")
   

#discharge patient from given facility
@app.route("/patient/<pat_id>/discharge/<facility_id>", methods=["PUT"])     
def dischargePfromF(pat_id, facility_id):
    hospitalOrQuarantine = ms.checkIfPorQ(facility_id)
    p = ms.getPatientById(pat_id)
    if p != None and hospitalOrQuarantine == "quarantine":
        discharged_from_q = ms.dischargePfromQ(facility_id, pat_id)
        if discharged_from_q != None:
            return jsonify("Discharged patient " + str(pat_id) + " from quarantine " + str(facility_id))
    elif p != None and hospitalOrQuarantine == "hospital":
        discharged_from_h = ms.dischargePfromH(facility_id, pat_id)
        if discharged_from_h != None:
            return jsonify("Discharged patient " + str(pat_id) + " from hospital " + str(facility_id))
    elif p == None:
        return jsonify("Patient was not found")
    elif hospitalOrQuarantine == None:
        return jsonify("Hospital or Quarantine was not found")
    else: 
        return jsonify("You really messed up")
    


#diagnosing patient
@app.route("/patient/<patient_id>/diagnosis", methods = ["POST"])
def diagnosePatient(patient_id):      
    p = ms.diagnosePatient(patient_id)
    addedInQ = None
    if(p!=None): 
        if p == "negative":
            return jsonify("Patient was diagnosed negative")
        elif p == "positive":
            quarantine_id = ms.pick_q()
            if quarantine_id != None:
                addedInQ = ms.addPinQ(quarantine_id, patient_id)
            if addedInQ != None: 
                return jsonify("Patient with id " + str(patient_id) + " was diagnosed positive and added in quarantine " + str(quarantine_id))
            else:
                return jsonify("No quarantine for patient was found.")
    return jsonify(
            success = False, 
            message = "Patient not found")

#cure patient
@app.route("/patient/<patient_id>/cure", methods = ["POST"])

def curePatient(patient_id):
    pick_hos = ms.pick_h()
    p = ms.getPatientById(patient_id)    
    if pick_hos != None:
        in_quarantine = p.inQ
        discharge_from_q = ms.dischargePfromQ(in_quarantine, patient_id)
        h = ms.addPinH(pick_hos, patient_id)
        p_cured = ms.curePatient(patient_id)
        discharge_from_h = ms.dischargePfromH(pick_hos, patient_id)
        if p != None and p_cured != None and h != None and discharge_from_q != None and discharge_from_h != None:
            message1 = ("Patiend was moved from quarantine " + str(in_quarantine) + " into hospital " + str(pick_hos))
            message2 = (str(p_cured))
            message3 = ("Patient was discharged from hospital " + str(pick_hos))
            return jsonify(
                    message1 = message1,
                    message2 = message2,
                    message3 = message3)
        elif p_cured == None:
            return jsonify("You cannot cure patient with negative diagnosis!")
        else:
            return jsonify("You reaaally messed up")
    elif p == None:
        return jsonify("Patient was not found")
    elif pick_hos == None:
        return jsonify("There is no hospital available.")
    else:
        return jsonify("Dont even try to fix this")
    

#STAFF

#adding new Staff
@app.route("/staff", methods = ["POST"])
def addStaff():
    #checking if only "doctor" or "nurse" is entered
    doctor_or_nurse = request.args.get("type")
    if doctor_or_nurse == "doctor" or doctor_or_nurse == "nurse":
        ms.addStaff(request.args.get("name"), request.args.get("dob"), doctor_or_nurse)
        return jsonify(f"Added new {request.args.get('type')} called {request.args.get('name')} with dob {request.args.get('dob')}")
    else:
        return jsonify("Please only enter type = doctor or nurse")
    
#getting all staff
@app.route("/staff", methods = ["GET"])
def allStaff():
    return jsonify(staff=[s.serialize() for s in ms.getStaff()])

#deleting a staff member from system
@app.route("/staff/<staff_id>", methods=["DELETE"])
def deleteStaff(staff_id):
    
    result = ms.deleteStaff(staff_id)   
    if(result): 
        message = f"Staff with id{staff_id} was deleted" 
    else: 
        message = "Staff not found" 
    return jsonify(
            success = result, 
            message = message)

#adding staff to given hospital or quarantine
@app.route("/staff/<staff_id>", methods=["PUT"])
def addStaffinH(staff_id):
    workplace_id = request.args.get("workplace")
    add = ms.addStaffinH(staff_id, request.args.get("workplace"))
    if add != None:
        return jsonify(f"Staff with id {staff_id} was was added into hospital with id {workplace_id}")
    else:
        return jsonify("Staff or Hospital wasn't found")
    
    
#STATS
@app.route("/stats", methods=["GET"])
def stats():
    hospitals_occupancy = ms.get_stats_hospital()
    quarantines_occupancy = ms.get_stats_quarantine()
    patients_infected = ms.get_stats_patients()
    patients_status = ms.patient_status()
    hospitals_total = len(ms.hospitals)
    quarantines_total = len(ms.quarantines)
    patients_total = len(ms.patients)
    if patients_infected != None:
        message1 = ("There are " + str(hospitals_total) + " hospitals with total occupancy " +  str(hospitals_occupancy) + "%")
        message2 = ("There are " + str(quarantines_total) + " quarantines with total occupancy " +  str(quarantines_occupancy) + "%")
        message3 = ("There are in total " + str(patients_total) + " patients:")
        message4 = (str(patients_infected[0]) + " of them tested positive -> " + str(patients_infected[3]) + "%")
        message5 = (str(patients_infected[1]) + " of them tested negative -> " + str(patients_infected[4]) + "%")
        message6 = (str(patients_infected[2]) + " of them not tested -> " + str(patients_infected[5]) + "%")
        message7 = "----------------------------------------"
        message8 = (str(patients_status[0]) + " patients are in quarantine.")
        message9 = (str(patients_status[1]) + " patients are in hospital.")
        message10 = (str(patients_status[2]) + " patients unfortunatelly died.")
        message11 = (str(patients_status[3]) + " patients were cured and discharged.")
        return jsonify(message1, message2, message3, message4, message5, message6, message7, message8, message9, message10, message11)
    elif patients_total == 0:
        return jsonify("There are no patients in system")
    else:
        return jsonify("Something went wrong")




@app.route("/")
def index():
    return jsonify(
            success = True, 
            message = "Your server is running! Welcome to the Covid API.")

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE"
    return response

if __name__ == "__main__":
    app.run(debug=False, port=8888)
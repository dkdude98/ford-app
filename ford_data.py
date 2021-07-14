import sys, os, logging, time
import requests
from fordpass import Vehicle
import json

def getDetails():         
    r = Vehicle("dkohli1@jh.edu", "Dkdude123?", "2FMPK3J98KBC63468") # Username, Password, VIN
    return r.status()
    # time.sleep(10) # Wait 10 seconds

def nhsta(vin):         
    r = requests.get("https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/"+ vin +"?format=json").json()
    results = r.get("Results")
    return [(results[0].get("Make")).title(),(results[0].get("Model")).title(),(results[0].get("ModelYear")).title(),(results[0].get("DriveType")),(results[0].get("FuelTypePrimary")),(results[0].get("VIN"))]
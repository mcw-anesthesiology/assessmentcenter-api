#!/usr/bin/env python3

from os import path, makedirs
import json
import requests

REGISTRATION_ID = '7C56CE15-00CD-4EE4-A64C-EA8DFDCF4ED9'
TOKEN = '2B45743A-1BAF-43CA-95A6-ED646BC296AF'
API_BASE_URL = 'https://www.assessmentcenter.net/ac_api/2014-01/'
API_FORMS = 'Forms/'
API_CALIBRATIONS = 'Calibrations/'
FORMAT = '.json'
FORMS_URL = API_BASE_URL + API_FORMS + FORMAT
AUTH = (REGISTRATION_ID, TOKEN)

FORMS_DIR = 'forms'
CALIBRATIONS_DIR = 'calibrations'

makedirs(FORMS_DIR, exist_ok=True)
try:
	forms = requests.get(API_BASE_URL + API_FORMS + FORMAT, auth=AUTH).json()
	with open('forms' + FORMAT, 'w') as forms_file:
		json.dump(forms, forms_file, indent='\t')
	for form in forms['Form']:
		with open(path.join(FORMS_DIR, form['OID']) + FORMAT, 'w') as form_file:
			json.dump(requests.get(API_BASE_URL + API_FORMS + form['OID'] + FORMAT, auth=AUTH).json(), form_file, indent='\t')
except:
	print('Unable to fetch forms')

makedirs(CALIBRATIONS_DIR, exist_ok=True)
try:
	calibrations = requests.get(API_BASE_URL + API_CALIBRATIONS + FORMAT, auth=AUTH).json()
	with open('calibrations' + FORMAT, 'w') as calibrations_file:
		json.dump(calibrations, calibrations_file, indent='\t')
	for calibration in calibrations['Calibration']:
		with open(path.join(CALIBRATIONS_DIR, calibration['OID']) + FORMAT, 'w') as calibration_file:
			json.dump(requests.get(API_BASE_URL + API_CALIBRATIONS + calibration['OID'] + FORMAT, auth=AUTH).json(), calibration_file, indent='\t')
except:
	print('Unable to fetch calibrations')

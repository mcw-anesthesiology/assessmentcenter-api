from os import path, makedirs
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
forms = requests.get(API_BASE_URL + API_FORMS + FORMAT, auth=AUTH).json()
for form in forms['Form']:
	with open(path.join(FORMS_DIR, form['OID']), 'w') as form_file:
		form_file.write(requests.get(API_BASE_URL + API_FORMS + form['OID'] + FORMAT, auth=AUTH).text)

makedirs(CALIBRATIONS_DIR, exist_ok=True)
calibrations = requests.get(API_BASE_URL + API_CALIBRATIONS + FORMAT, auth=AUTH).json()
for calibration in calibrations['Calibration']:
	with open(path.join(CALIBRATIONS_DIR, calibration['OID']), 'w') as calibration_file:
		calibration_file.write(requests.get(API_BASE_URL + API_CALIBRATIONS + calibration['OID'] + FORMAT, auth=AUTH).text)

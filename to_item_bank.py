import json
from os import path
from argparse import ArgumentParser
import sys


FORMS_DIR = './forms'
CALIBRATIONS_DIR = './calibrations'
EXTENSION = '.json'

SEPARATOR = '  '

def get_item_bank(oid):
	try:
		with open(path.join(FORMS_DIR, oid + EXTENSION)) as form_file:
			form = json.load(form_file)
	except:
		print('Error loading form')
		sys.exit()

	try:
		with open(path.join(CALIBRATIONS_DIR, oid + EXTENSION)) as calibration_file:
			calibration = json.load(calibration_file)
	except:
		print('Error loading calibration')
		sys.exit()

	properties = {}
	for prop in calibration['Properties']:
		for (key, val) in prop.items():
			properties[key] = val

	calibration_items_by_id = {}
	for item in calibration['Items']:
		calibration_items_by_id[item['ID']] = item


	bank = 'private static final ItemBank bank = itemBank(0.0, 0.0, {}, {}, {},\n'.format(
		properties['MinNumItems'],
		properties['MaxNumItems'],
		float(properties['MaxStdErr']) * 10
	)
	for item in form['Items']:
		try:
			bank += get_item(item, calibration_items_by_id[item['ID']])
		except Exception as e:
			print(e)
	bank = bank[:-2] + '\n'
	bank += ');'

	bank += '\n\n'
	bank += 'public static ItemBank bank() {\n'
	bank += SEPARATOR + 'return bank;\n'
	bank += '}'

	print(str(bank))


def get_item(item, calibration):
	elements = item['Elements']
	if len(elements) == 2:
		context = ''
		prompt = elements[0]['Description']
		responses = elements[1]['Map']
	elif len(elements) == 3:
		context = elements[0]['Description']
		prompt = elements[1]['Description']
		responses = elements[2]['Map']
	else:
		raise LookupError('Wrong number of elements: {}'.format(len(elements)))

	brief = ''
	alpha = calibration['A_GRM']

	betas = [item['Threshold'] for item in calibration['Map']]
	strata = -1
	category = ''

	item = SEPARATOR + 'item("{}", "{}", "{}", "{}", {}, new double[] {{ {} }}, {}, "{}",\n'.format(
		item['ID'],
		context,
		prompt,
		brief,
		alpha,
		', '.join(betas),
		strata,
		category
	)

	for response in responses:
		item += get_response(response)

	item = item[:-2] + '\n'
	item += SEPARATOR + '),\n'
	return item

def get_response(response):
	return SEPARATOR + SEPARATOR + 'response("{}", {}),\n'.format(
		response['Description'],
		response['Value']
	)

def main():
	parser = ArgumentParser(description='Convert PROMIS measure JSON files to CHOIR ItemBank')
	parser.add_argument('oid', action='store', help='OID of the PROMIS measure')

	args = parser.parse_args()

	get_item_bank(args.oid)

if __name__ == '__main__':
	main()

#!/usr/bin/env python3

import json
from os import path
from argparse import ArgumentParser
import sys


FORMS_DIR = './forms'
CALIBRATIONS_DIR = './calibrations'
EXTENSION = '.json'

SEPARATOR = '  '

def get_bank_file(class_name, oid):
	with open('./forms' + EXTENSION, 'r') as forms_file:
		forms = json.load(forms_file)

	forms_by_oid = {form['OID']: form for form in forms['Form']}

	form_name = forms_by_oid[oid]['Name']

	bank_file = '''package edu.mcw.survey.server.promis;

import edu.stanford.survey.server.CatAlgorithm.ItemBank;
import static edu.stanford.survey.server.ItemBanks.*;

/**
 * Item bank for PROMIS generated from:
 *
 * Name: {}
 * OID: {}
 */

public class {} {{
  private static final ItemBank bank = {}

  public static ItemBank bank() {{
    return bank;
  }}
}}'''.format(
		form_name,
		oid,
		class_name,
		get_item_bank(oid)
	)

	return bank_file

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


	bank = 'itemBank(0.0, 0.0, {}, {}, {},\n'.format(
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
	bank += SEPARATOR + ');'

	return bank


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

	item = SEPARATOR + SEPARATOR + 'item("{}", "{}", "{}", "{}", {}, new double[] {{ {} }}, {}, "{}",\n'.format(
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
	item += SEPARATOR + SEPARATOR + '),\n'
	return item

def get_response(response):
	return SEPARATOR + SEPARATOR + SEPARATOR + 'response("{}", {}),\n'.format(
		response['Description'],
		response['Value']
	)

def main():
	parser = ArgumentParser(description='Convert PROMIS measure JSON files to CHOIR ItemBank')
	parser.add_argument('class_name', action='store', help='Class name of Java file')
	parser.add_argument('oid', action='store', help='OID of the PROMIS measure')

	args = parser.parse_args()

	print(get_bank_file(args.class_name, args.oid))

if __name__ == '__main__':
	main()

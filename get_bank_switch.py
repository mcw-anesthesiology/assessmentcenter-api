#!/usr/bin/env python3

from os import scandir, path
from argparse import ArgumentParser
import sys

def get_switch(item_bank_path):
	bank_dir = path.realpath(item_bank_path)

	switch = ''

	with scandir(bank_dir) as bank_files:
		for bank_file in bank_files:
			try:
				bank_class_name = bank_file.name.replace('.java', '')
				with open(bank_file, 'r') as bank_file_contents:
					for line in bank_file_contents:
						if '* Name: ' in line:
							measure_name = line.replace('* Name: ', '').strip()
							break
				if not measure_name:
					raise LookupError('Error finding measure name for {}'.format(bank_class_name))

				switch += 'case "{}": return {}.bank();\n'.format(
					measure_name.replace('"', '\\"'),
					bank_class_name
				)
			except Exception as e:
				print(e, file=sys.stderr)

	return switch

def main():
	parser = ArgumentParser(description='Create Java switch statement for PROMIS measures in given directory')
	parser.add_argument('directory', action='store', help='Directory in which to look for Java PROMIS item banks')

	args = parser.parse_args()

	print(get_switch(args.directory))

if __name__ == '__main__':
	main()

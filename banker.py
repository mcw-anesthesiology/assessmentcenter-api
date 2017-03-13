#!/usr/bin/env python3

from os import scandir, path
from argparse import ArgumentParser
import sys

def get_measures(command, item_bank_path):
	bank_dir = path.realpath(item_bank_path)

	measures = ''

	with scandir(bank_dir) as bank_files:
		for bank_file in bank_files:
			try:
				bank_class_name = path.splitext(path.basename(bank_file))[0]
				with open(bank_file, 'r') as bank_file_contents:
					for line in bank_file_contents:
						if '* Name: ' in line:
							measure_name = line.replace('* Name: ', '').strip().replace('"', '\\"')
							break
				if not measure_name:
					raise LookupError('Error finding measure name for {}'.format(bank_class_name))

				if command == 'switch':
					measures += 'case "{}": return {}.bank();\n'.format(
						measure_name,
						bank_class_name
					)
				elif command == 'studies':
					measures += 'registry.addStudy(localPromisSystemId, "{}", "{}");\n'.format(
						measure_name,
						measure_name
					)
				elif command == 'sql':
					local_promis_system_id = 1003
					meta_version = 0
					measures += '''
						INSERT into study (
							survey_system_id,
							study_code,
							study_description,
							meta_version,
							dt_created,
							dt_changed,
							title
						) values (
							{},
							nextval('study_code_seq'),
							'{}',
							{},
							now(),
							NULL,
							'{}'
						);
					'''.format(
						local_promis_system_id,
						measure_name,
						meta_version,
						measure_name
					)
				else:
					raise ValueError('Invalid command {}'.format(command))
			except Exception as e:
				print(e, file=sys.stderr)

	return measures

def main():
	parser = ArgumentParser(description='Create Java studies for CreateRegistrySchema')
	parser.add_argument('command', action='store', help='Thing to export (switch, studies, sql)')
	parser.add_argument('directory', action='store', help='Directory in which to look for Java PROMIS item banks')

	args = parser.parse_args()

	print(get_measures(args.command, args.directory))

if __name__ == '__main__':
	main()

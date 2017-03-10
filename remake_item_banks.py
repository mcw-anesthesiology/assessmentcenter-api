#!/usr/bin/env python3

from argparse import ArgumentParser
from os import scandir, path
import sys

from to_item_bank import get_bank_file

def remake_banks(item_bank_path):
	bank_dir = path.realpath(item_bank_path)

	with scandir(bank_dir) as bank_files:
		for bank_file in bank_files:
			try:
				bank_class_name = path.splitext(path.basename(bank_file))[0]
				with open(bank_file, 'r') as bank_file_contents:
					for line in bank_file_contents:
						if '* OID: ' in line:
							oid = line.replace('* OID: ', '').strip()
							break
				if not oid:
					raise LookupError('Error finding measure name for {}'.format(bank_class_name))

				item_bank = get_bank_file(oid, bank_class_name) + '\n'
				with open(bank_file, 'w') as bank_fp:
					bank_fp.write(item_bank)
			except Exception as e:
				print('Error rewriting bank: {}'.format(e), file=sys.stderr)

def main():
	parser = ArgumentParser(description='Mass recreate item banks')
	parser.add_argument('directory', action='store', help='Directory in which to look for Java PROMIS item banks')

	args = parser.parse_args()

	remake_banks(args.directory)


if __name__ == '__main__':
	main()

import json
import os
import pandas as pd
import subprocess
import sys

def revisions(repopath, filename):
	output = subprocess.check_output(['git', '-C', repopath, 'log', '--pretty=%H %ct %ci', filename])
	lines = output.decode('UTF-8').rstrip().split("\n")
	return [
		line.split(" ", 2) for line in lines
	]

def getrevision(repopath, filename, ref):
	output = subprocess.check_output(['git', '-C', repopath, 'show', f'{ref}:{filename}'])
	return output.decode('UTF-8').rstrip()

def recurse(data: dict, value, prefix = ''):
	if isinstance(value, dict):
		if prefix:
			prefix = prefix + "."

		for key, val in value.items():
			recurse(data, val, f"{prefix}{key}")

	elif isinstance(value, list):
		if prefix:
			prefix = prefix + "."

		for idx, val in enumerate(value):
			recurse(data, val, f"{prefix}{idx}")

	else:
		data[prefix] = value

def parse(data: dict):
	result = {}
	recurse(result, data)
	return result

repopath = sys.argv[1]
jsonpath = sys.argv[2]
csvpath = sys.argv[3]

jsonfile = os.path.basename(jsonpath)
jsonname = os.path.splitext(jsonfile)[0]

revs = reversed(revisions(repopath, jsonpath))
files = {}

for rev in revs:
	ref, timestamp, rfcdate = rev

	txt = getrevision(repopath, jsonpath, ref)
	js = json.loads(txt)

	firstval = list(js.values())[0]

	if isinstance(firstval, dict):
		for key, value in js.items():
			fname = f'{jsonname}-{key}'
			files[fname] = files.get(fname, [])
			files[fname].append({
				'captureTimestamp': timestamp,
				'captureDateTime': rfcdate,
				'captureRevision': ref,
				**parse(value),
			})
	else:
		files[jsonname] = files.get(jsonname, [])
		files[jsonname].append({
			'captureTimestamp': timestamp,
			'captureDateTime': rfcdate,
			'captureRevision': ref,
			**parse(js),
		})

for filename, rows in files.items():
	filename = os.path.join(csvpath, f'{filename}.csv')
	df = pd.DataFrame.from_records(rows)
	df.to_csv(filename, index=False)

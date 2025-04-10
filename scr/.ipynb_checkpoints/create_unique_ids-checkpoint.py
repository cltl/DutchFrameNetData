import csv
import os
from collections import defaultdict
import uuid
import os

def find_most_annotated(article_data):
	times = defaultdict(list)
	for n, d in enumerate(article_data):
		time = d['most_recent_annotation']
        # mode = d['annotation_mode']
        # release = d['release']
		times[time].append(d)
        
	sorted_times = sorted(times, reverse = True)
	most_recent = sorted_times[0]
	d_most_recent = times[most_recent]
	if len(d_most_recent) == 1:
		selected_most_recent = d_most_recent[0]
	else:
		for d in d_most_recent:
			release = d['release']
			mode = d['annotation_mode']
			if release.startswith('dfn-data-cleaning-headlines') and mode == 'manual':
				selected_most_recent = d
				break
			elif release.startswith('dfn-data-cleaning-headlines') and mode == 'system':
				selected_most_recent = d
				break
			else:
				selected_most_recent = None
		if selected_most_recent is None:
			selected_most_recent = d_most_recent[0]
			
	target_release = selected_most_recent['release']
	# extend with other releases
	all_releases = [d['release'] for d in article_data]
	other_releases = [release for release in all_releases if release != target_release]
	if other_releases:
		selected_most_recent['other releases'] = ' '.join(other_releases)
	else:
		selected_most_recent['other releases'] = '-'
# 	print(other_releases)
# 	print(selected_most_recent['other releases'])
	
	# add unique id
	uid = uuid.uuid4()
	selected_most_recent['unique_id'] = str(uid)
	return selected_most_recent

with open('../data/overview.csv') as infile:
    data = list(csv.DictReader(infile, delimiter = ','))
	
article_data = defaultdict(list)

for d in data:
    title = (d['text_title'], d['lang'])
    article_data[title].append(d)
	

data_unique = []

for article_title, article_d in article_data.items():
    most_recent_d = find_most_annotated(article_d)
    data_unique.append(most_recent_d)

print('unique data')
print(len(data_unique))
	
for d in data_unique:
	release = d['release']
	title = d['text_title']
	lang = d['lang']
	uid = d['unique_id']
	path = f'../data/releases-and-repos-sorted/{release}/unstructured/{lang}/{title}'
	new_uuid_path = f'../data/data-unique-ids/unstructured/{lang}/{uid}.naf'
	with open(path) as infile:
		naf = infile.read()
	with open(new_uuid_path, 'w') as outfile:
		outfile.write(naf)
		
		
		
all_files = os.listdir('../data/data-unique-ids/unstructured')
print('all files')
print(len(all_files))
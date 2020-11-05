# Construct the filtered data_dicts with in/out links and id
from pathlib import Path
import json
from tqdm import tqdm

# Read and concatenate the data
data_dicts = []
out_Path = Path('output_json')
for i in tqdm(range(0, 17), desc='Reading'): # Q-16
    outPath = Path(out_Path, 'A'+chr(ord('A')+i)+'.json')
    with open(outPath, 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
        data_dicts += load_dict


title_to_id = {}
print("len=", len(data_dicts))  # 5719052

# Build the dicts
# Reid the data and record the links_id, for filtering
for i, data_dict in enumerate(data_dicts):
    data_dict['id'] = i
    title_to_id[data_dict['title']] = i

for data_dict in tqdm(data_dicts, desc='pre-Processing'):
    outlinks_id = []
    for out_title in data_dict['outlinks']:
        out_id = title_to_id.get(out_title, -1)
        if out_id != -1:
            outlinks_id.append(out_id)
            data_dicts[out_id]['inlinks_id'].append(data_dict['id'])
    data_dict['outlinks_id'] = outlinks_id

# Filter
threshold = 24
toSave = []
for i, data_dict in enumerate(data_dicts):
    if len(data_dict['inlinks_id'])+len(data_dict['outlinks_id']) >= threshold:
        toSave.append(i)

data_dicts_ = []
for i in toSave:
    data_dicts_.append(data_dicts[i])

data_dicts = data_dicts_
print("len=", len(data_dicts))  # 1052788

# Rebuild the complete dicts after filtering
title_to_id.clear()
for i, data_dict in enumerate(data_dicts):
    data_dict['id'] = i
    title_to_id[data_dict['title']] = i
    data_dict['inlinks'].clear()
    data_dict['inlinks_id'].clear()

for data_dict in tqdm(data_dicts_, desc='post-Processing'):
    outlinks_id = []
    outlinks = []
    for out_title in data_dict['outlinks']:
        out_id = title_to_id.get(out_title, -1)
        if out_id != -1:
            outlinks_id.append(out_id)
            outlinks.append(out_title)
            data_dicts[out_id]['inlinks'].append(data_dict['title'])
            data_dicts[out_id]['inlinks_id'].append(data_dict['id'])
    data_dict['outlinks_id'] = outlinks_id
    data_dict['outlinks'] = outlinks

# Dump the data
with open(Path(out_Path, 'data_dicts.json'), 'w', encoding='utf-8') as dump_f:
    json.dump(data_dicts, dump_f)
    print("Dump Done")

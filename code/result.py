# Rank the dicts and write down the results
from pathlib import Path
import json
from tqdm import tqdm

data_Path = Path('output_json')

print('loading')
with open(Path(data_Path, 'val_dict.json'), 'r', encoding='utf-8') as load_f:
    val_dict = json.load(load_f)
with open(Path(data_Path, 'data_dicts.json'), 'r', encoding='utf-8') as load_f:
    data_dicts = json.load(load_f)

# Rank the PageRank dicts
val_tuples = sorted(val_dict.items(), key=lambda dic: (
    dic[1], dic[0]), reverse=True)

# Write down the result
with open('result.txt', 'w', encoding='utf-8') as f:
    for item in tqdm(val_tuples, desc='Writing'):
        f.write("%s\t%f\n" % (data_dicts[int(item[0])]['title'], item[1]))

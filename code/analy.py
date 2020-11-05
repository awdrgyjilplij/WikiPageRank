# Do some analyses of the result
# This code just represents one analysis, of the 'Köppen climate classification'
from pathlib import Path
import json
import numpy as np
from tqdm import tqdm
from scipy.sparse import csr_matrix, save_npz

data_dicts = []
data_Path = Path('output_json')

print("loading")
with open(Path(data_Path, 'data_dicts.json'), 'r', encoding='utf-8') as load_f:
    data_dicts = json.load(load_f)

print("finding")
for data_dict in data_dicts:
    if data_dict['title'] == 'Köppen climate classification':
        print(len(data_dict['outlinks']), len(data_dict['inlinks']))

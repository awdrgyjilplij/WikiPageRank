# Build the sparse matrix and save it
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

data_len = len(data_dicts)

# From a null matrix, P[row[i]][col[i]]+=data[i] for i in len(row)
row = []
col = []
data = []

for i, data_dict in tqdm(list(enumerate(data_dicts)), desc='Building Matrix'):
    data_len = len(data_dict['outlinks_id'])
    if data_len == 0:
        continue
    val = 1/data_len
    outlinks_id = data_dict['outlinks_id']
    for j in outlinks_id:
        row.append(i)
        col.append(j)
        data.append(val)

# Save its transpose
P = csr_matrix((data, (row, col)), shape=(
    data_len, data_len), dtype=np.float).transpose()
save_npz('Matrix', P)
print("Save Done")

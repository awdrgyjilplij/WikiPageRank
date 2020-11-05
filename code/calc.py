# Calculate the pagerank values and save them
from pathlib import Path
import numpy as np
import json
from tqdm import tqdm
from scipy.sparse import csr_matrix, load_npz

# Load and initialize
out_Path = Path('output_json')
P = load_npz('Matrix.npz')
n = P.shape[0]
r = np.ones(n, dtype=float)
e = np.ones(n, dtype=float)

alpha = 0.9
epochs = 1000
r_ = r

# Calculate
for i in range(epochs):
    r_ = alpha*P.__mul__(r)+(1-alpha)*e
    var = np.linalg.norm(r_-r, ord=2)
    r = r_
    if var < 1e-9:
        break
    if i % 10 == 0:
        print("epoch %d with var %.10f" % (i, var))

# Dump the result
key = list(range(n))
val_dict = dict(zip(key, r))
with open(Path(out_Path, 'val_dict.json'), 'w', encoding='utf-8') as dump_f:
    json.dump(val_dict, dump_f)
    print("Dump Done")

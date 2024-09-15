from chroma import Chroma
from chroma import api
import numpy as np
import os
from tqdm import tqdm
api.register_key("5d9b4b61795e4b0db2db832d332d19d6")
import argparse
parser = argparse.ArgumentParser()

# Define model arguments
parser.add_argument('--run_name', type=str, help='Root directory', default='')
parser.add_argument('--outdir', type=str, help='Output directory', required=True)
parser.add_argument('--num_samples', type=int, help='Number of samples per length', default=5)
parser.add_argument('--len', type=int, help='Number of samples per length', default=100)
parser.add_argument('--len_dist', type=str, help='Output directory', default=None)
parser.add_argument('--sorted', action='store_true', help='Run in decreasing order of length')

# Parse arguments
args = parser.parse_args()

if args.len_dist is not None:
    lens = np.load(args.len_dist)['lengths']
    sample_lens = []
    for i in range(args.num_samples):
        choice = 0
        while choice < 4 or choice > 500:
            choice = np.random.choice(lens)
        sample_lens.append(choice)
    if args.sorted:
        sample_lens = sorted(sample_lens)[::-1]
else:
    sample_lens = [args.len] * args.num_samples

chroma = Chroma()
os.makedirs(args.outdir, exist_ok=True)
for i, length in tqdm(enumerate(sample_lens)):
    print(f'{i} of {len(sample_lens)} with len {length}')
    protein = chroma.sample(chain_lengths=[length], samples=1)
    protein.to(f"{args.outdir}/{args.run_name}sample{i}.pdb")
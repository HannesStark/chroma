from chroma import Chroma
from chroma import api
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

lens = np.load(args.len_dist)['lengths']

if args.len_dist is not None:
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


for i, length in tqdm(enumerate(sample_lens)):
    print(f'{i} of {len(sample_lens)}')
    chroma = Chroma()
    protein = chroma.sample(chain_lengths=[length], samples=1)
    protein.to(f"{args.outdir}/{run_name}sample{i}.pdb")
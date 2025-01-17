import pandas as pd
import altair_saver
from utils import *

# Define the directories containing the input data
input_dir = 'L:/cluster_seed30'
t = np.load(input_dir + '/raw_data/taxis.npy')[:20000]
v = np.load(input_dir + '/raw_data/membrane_potential_data/v.npy')[1471, :20000]  # 1471 soma(0.5)
part_neg = pd.read_csv(input_dir + '/partitioned_data/total_currents/itotal_neg_0.csv')
part_pos = pd.read_csv(input_dir + '/partitioned_data/total_currents/itotal_pos_0.csv')

# Rename current type column
part_neg.rename(columns={part_neg.columns[0]: 'itype'}, inplace=True)
part_pos.rename(columns={part_pos.columns[0]: 'itype'}, inplace=True)

# Identify unique indices based on the time vector t
unique_indices = np.unique(t, return_index=True)[1]

# Keep only the unique indices in t, v, part_pos, and part_neg
t_unique = t[unique_indices]
v_unique = v[unique_indices]

part_pos_without_itype = part_pos.iloc[:, 1:]
part_pos_unique = part_pos_without_itype.iloc[:, unique_indices]
part_pos_unique.insert(0, 'itype', part_pos.iloc[:, 0])

part_neg_without_itype = part_neg.iloc[:, 1:]
part_neg_unique = part_neg_without_itype.iloc[:, unique_indices]
part_neg_unique.insert(0, 'itype', part_neg.iloc[:, 0])

# Create charts
totalpos = create_currsum_pos_chart(part_pos_unique, t_unique)
totalneg = create_currsum_neg_chart(part_neg_unique, t_unique)
currshares_pos, currshares_neg = create_currshares_chart(part_pos_unique, part_neg_unique, t_unique)
vm_chart = create_vm_chart(v_unique, t_unique)

# Create currentscape
currentscape = combine_charts(vm_chart, totalpos, currshares_pos, currshares_neg, totalneg)
currentscape.save('currentscape.html')


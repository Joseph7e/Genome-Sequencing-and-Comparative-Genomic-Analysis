#! /usr/bin/env python3

import argparse
from upsetplot import UpSet
from upsetplot import from_contents
import matplotlib.pyplot as plt
import matplotlib
from csv import DictReader
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

"""
Orthogroup	Kurthia_huakuii	Solibacillus_kalamii	Kurthia_zopfii	Kurthia_sibirica	PROKKA_10142021	Total
OG0000000	1	0	5	9	19	34
OG0000001	22	0	1	2	2	27
OG0000002	5	5	4	7	6	27
OG0000003	3	20	1	1	1	26

BIN	ALHT-Deer-02	ALHT-Deer-10	ALHT-Deer-103	ALHT-Deer-103-2	ALHT-Deer-12	ALHT-Deer-126	ALHT-Deer-139	ALHT-Deer-14	ALHT-Deer-142	ALHT-Deer-15	ALHT-Deer-20	ALHT-Deer-27	ALHT-Deer-32	ALHT-Deer-34	ALHT-Deer-37	ALHT-Deer-40	ALHT-Deer-41	ALHT-Deer-44	ALHT-Deer-46	ALHT-Deer-47	ALHT-Deer-48	ALHT-Deer-50	ALHT-Deer-53	ALHT-Deer-58	ALHT-Deer-62	ALHT-Deer-65	ALHT-Deer-70	ALHT-Deer-79	ALHT-Deer-80	ALHT-Deer-89-1	ALHT-Deer-89-2	ALHT-Deer-89-3	ALHT-Deer-91	ALHT-Deer-91-1	ALHT-Deer-91-2	ALHT-Deer-91-3	EQ02441275	EQ02441277	EQ02441278	EQ02441281	EQ02441285	EQ02441297	EQ02441299	EQ02441300	EQ02441302	EQ02441303	EQ02441305	EQ02441308	EQ02441309	EQ02441312	EQ02441470	EQ02441473	EQ02441475	EQ02441477	EQ02441480	EQ02441481	EQ02441484	EQ02441485	EQ02441493	EQ02441494	EQ02441495	EQ02441496	EQ02441504	EQ02441509	EQ02442193	EQ02442194	EQ02442198	EQ02442200	EQ02442202	EQ02442203	EQ02442205	EQ02442209	EQ02442211	EQ02442219	EQ02442220	EQ02442231	EQ02442233	EQ02442956	EQ02442957	EQ02442958	EQ02442962	EQ02442969	EQ02442972	EQ02442973	EQ02442974	EQ02442980	EQ02442990	EQ02442991	EQ02442992	EQ02442993	TB-90024065	TB-90024076	ALHT-Deer-77	EQ02442215	EQ02441314	4065-16s	ALHT-Deer-04-2-16s	ALHT-Deer-07-16s	ALHT-Deer-100-16s	ALHT-Deer-101-16s	ALHT-Deer-102-1-16s	ALHT-Deer-102-2-16s	ALHT-Deer-107-1-16s	ALHT-Deer-107-2-16s	ALHT-Deer-121-1-16s	ALHT-Deer-121-2-16s	ALHT-Deer-121-3-16s	ALHT-Deer-122-16s	ALHT-Deer-125-1-16s	ALHT-Deer-125-2-16s	ALHT-Deer-125-3-16s	ALHT-Deer-127-16s	ALHT-Deer-128-1-16s	ALHT-Deer-128-2-16s	ALHT-Deer-129-16s	ALHT-Deer-130-1-16s	ALHT-Deer-130-2-16s	ALHT-Deer-133-16s	ALHT-Deer-134-16s	ALHT-Deer-135-16s	ALHT-Deer-140-1-16s	ALHT-Deer-140-2-16s	ALHT-Deer-140-3-16s	ALHT-Deer-141-1-16s	ALHT-Deer-141-2-16s	ALHT-Deer-141-3-16s	ALHT-Deer-145-1-16s	ALHT-Deer-145-2-16s	ALHT-Deer-145-3-16s	ALHT-Deer-145-4-16s	ALHT-Deer-146-1-16s	ALHT-Deer-146-2-16s	ALHT-Deer-147-1-16s	ALHT-Deer-147-2-16s	ALHT-Deer-147-3-16s	ALHT-Deer-147-4-16s	ALHT-Deer-148-1-16s	ALHT-Deer-148-2-16s	ALHT-Deer-149-16s	ALHT-Deer-153-16s	ALHT-Deer-17-1-16s	ALHT-Deer-17-2-16s	ALHT-Deer-22-16s	ALHT-Deer-24-16s	ALHT-Deer-64-16s	ALHT-Deer-73-16s	ALHT-Deer-90-16s	ALHT-Deer-92-16s	ALHT-Deer-93-1-16s	ALHT-Deer-93-2-16s	ALHT-Deer-98-1-16s	ALHT-Deer-98-2-16s	ALHT-Deer-98-3-16s	ALHT-Deer-98-4-16s	ALHT-Deer-99-1-16s	ALHT-Deer-99-2-16s	EQ02440606-16s	eq02440612-16s	eq02440616-1-16s	eq02440616-2-16s	eq02440616-3-16s	eq02440616-4-16s	eq02440624-16s	eq02440626-16s	eq02440635-16s	eq02440649-16s	eq02440749-3-16s	eq02440749-4-16s	eq02440756-16s	eq02440768-16s	eq02440769-16s	eq02440774-16s	eq02440775-1-16s	eq02440775-2-16s	eq02440776-16s	eq02440781-16s	eq02441467-1-16s	eq02441467-2-16s	eq02441467-3-16s	eq02441467-4-16s	EQ02441506-16s	EQ02442977-16s	TB-90024100-16s	TB-90024117-1-16s	TB-90024117-2-16s	ALHT-Deer-04-1-16s	ALHT-Deer-42-16s
Ixodes scapularis - deer tick	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	0	0	1	1	1	0	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	0	0	0	1	1
Dermacentor albipictus - winter tick	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	1	0	0	0	1	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	1	1	1	0	0
Odocoileus virginianus - white-tailed deer	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	0	0	1	1	1	0	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	1	0	0	0	1	0	0	0	0	1	1	0	1	1	1	1	1	1	1	0	0	0	1	1	1	1	1	1	1	0	0	0	1	1
"""

# parses command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Creates an Upset plot from orthogroup data")
    parser.add_argument("--genes", "-g", help="Orthogroup gene count csv file")
    parser.add_argument("--out", default="orthogroup_upsetplot.png", help="Name of Upset plot file")
    return parser.parse_args()

args = parse_args()

contents_dict = {}
# import binning tsv into a contents dictionary
bin_dict = DictReader(open(args.genes), delimiter="\t")

for row in bin_dict:
    curr_bin = ""
    for sample, count in row.items():
        # if its the Total row, ignore as sample
        if sample == "Total":
            continue
        # if sample is orthogroup, count is actually the sequence of interest
        if sample == "Orthogroup":
            contents_dict.setdefault(count, [])
            curr_bin = count
            continue
        # otherwise, sample is valid and will have count to add to contents
        if float(count) > 0:
            contents_dict[curr_bin].append(sample)
            
# transpose dictionary contents
transpose_contents = {}
for og, sample_list in contents_dict.items():
    for sample in sample_list:
        transpose_contents.setdefault(sample, [])
        transpose_contents[sample].append(og)

orthogroups = from_contents(transpose_contents)
matplotlib.rcParams["font.size"] = 7.25
ax_dict = UpSet(orthogroups, subset_size="count", show_counts="%d", show_percentages=True, sort_categories_by="-input", sort_by="-degree").plot()

# Save the plot to a file
plt.savefig(args.out)

# Show the plot
#plt.show()

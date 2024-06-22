import os
import pickle
import logging
import numpy as np
from tqdm import tqdm
from collections import defaultdict
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


#%% 参数
# GeneLocation_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.GeneLocation.pickle'
# CoordinateMatrix_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.CoordinateMatrix.pickle'
# save_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.GeneColocation.pickle'

import argparse
parse = argparse.ArgumentParser()
parse.add_argument('-ic',type=str,required=True,help='CoordinateMatrix.pickle file which generate by CoordinateMatrix.py')
parse.add_argument('-ig',type=str,required=True,help='GeneLocation.pickle file which generate by GeneLocation.py')
parse.add_argument('-s',type=str,required=True,help='save path')
args = parse.parse_args()
# GeneLocation_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.GeneLocation.pickle'
# save_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.CoordinateMatrix.pickle'
CoordinateMatrix_path = args.ic
GeneLocation_path = args.ig
save_path  = args.s

#%%
logger.info('Data Loading')
with open(GeneLocation_path, 'rb') as file:
    gene_location = pickle.load(file)
with open(CoordinateMatrix_path, 'rb') as file:
    coordinate_matrix = pickle.load(file)
#%%
logger.info('Data Processing')
gene_convert = defaultdict(list)
for cell in gene_location:
    for gene in gene_location[cell].keys():
        gene_convert[gene].extend(gene_location[cell][gene])

#%%
gene_region = {}
radius = 1
for reference_gene in tqdm(gene_convert.keys()):
    gene_region[reference_gene] = defaultdict(int)
    reference_coordinate_list = gene_convert[reference_gene]
    for num, coordinate in enumerate(reference_coordinate_list):
        x = coordinate[0]
        y = coordinate[1]
        region = []
        for i in range(-radius,radius+1):
            x_index = int(x - i)
            for j in range(-radius,radius+1):
                y_index = int(y - j)
                try:
                    for gene in coordinate_matrix[x_index][y_index].keys():
                        region.append(gene)
                except:
                    pass
        region = list(set(region))
        for gene in region:
            gene_region[reference_gene][gene] += 1
#%%
with open(save_path, 'wb') as file:
    pickle.dump(gene_region, file)

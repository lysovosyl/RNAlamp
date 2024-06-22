import os
import pickle
import logging
import numpy as np
from tqdm import tqdm
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# 创建控制台处理器（StreamHandler）
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
# 创建格式化器（Formatter）
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

#%% 参数
# CellCenter_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin_with_background.CellCenter.pickle'
# GeneLocation_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin_with_background.GeneLocation.pickle'
# save_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin_with_background.GeneDistance.pickle'


import argparse
parse = argparse.ArgumentParser()
parse.add_argument('-ic',type=str,required=True,help='CellCenter.pickle file which generate by CellCenter.py')
parse.add_argument('-ig',type=str,required=True,help='GeneLocation.pickle file which generate by GeneLocation.py')
parse.add_argument('-s',type=str,required=True,help='save path')
args = parse.parse_args()
CellCenter_path = args.ic
GeneLocation_path = args.ig
save_path  = args.s
#%%
logger.info('Data Loading')
with open(CellCenter_path, 'rb') as file:
    cell_center = pickle.load(file)

with open(GeneLocation_path, 'rb') as file:
    gene_location = pickle.load(file)
#%%
gene_list = []
for cell in gene_location:
    gene_list.extend(list(gene_location[cell].keys()))
gene_list = set(gene_list)
#%%
logger.info('Data Processing')
gene_distance = {}
for gene in tqdm(gene_list):
    cell_array = []
    gene_array = []
    for cell in gene_location:
        if gene in gene_location[cell].keys():
            for xy in gene_location[cell][gene]:
                cell_array.append(cell_center[cell])
                gene_array.append(xy)
    cell_array = np.array(cell_array)
    gene_array = np.array(gene_array)
    distances = np.linalg.norm(cell_array - gene_array, axis=1)
    gene_distance[gene] = distances

#%%
with open(save_path, 'wb') as file:
    pickle.dump(gene_distance, file)






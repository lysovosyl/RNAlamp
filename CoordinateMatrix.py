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

import argparse
parse = argparse.ArgumentParser()
parse.add_argument('-i',type=str,required=True,help='GeneLocation.pickle file which generate by GeneLocation.py')
parse.add_argument('-s',type=str,required=True,help='save path')
args = parse.parse_args()
# GeneLocation_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.GeneLocation.pickle'
# save_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.CoordinateMatrix.pickle'
GeneLocation_path = args.i
save_path  = args.s

#%%
logger.info('Data Loading')
with open(GeneLocation_path, 'rb') as file:
    gene_location = pickle.load(file)
#%%
logger.info('Data Processing')
matrix = {}
for cell in tqdm(gene_location):
    for gene in gene_location[cell]:
        for coordinate in gene_location[cell][gene]:
            x = coordinate[0]
            y = coordinate[1]
            if x not in matrix:
                matrix[x] = {}
                if y not in matrix[x].keys():
                    matrix[x][y] = {}
            else:
                if y not in matrix[x].keys():
                    matrix[x][y] = {}
            if gene not in matrix[x][y].keys():
                matrix[x][y][gene] = 1
            else:
                matrix[x][y][gene] += 1
#%%
with open(save_path, 'wb') as file:
    pickle.dump(matrix, file)

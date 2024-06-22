import os
import pickle
import logging
import numpy as np
import math
from tqdm import tqdm
import csv
# 创建logger对象
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# 创建控制台处理器（StreamHandler）
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
# 创建格式化器（Formatter）
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

#%%

import argparse
parse = argparse.ArgumentParser()
parse.add_argument('-i',type=str,required=True,help='GeneDistanceToCenter file which generate by GeneDistanceToCenter.py')
parse.add_argument('-s',type=str,required=True,help='save path this will save as a tsv file')
args = parse.parse_args()
input_path = args.i
save_path  = args.s

# input_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin_with_background.GeneDistanceToCenter.pickle'
# save_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin_with_background.Lscore.tsv'

#%%
logger.info('Data Loading')
with open(input_path, 'rb') as file:
    gene_distance = pickle.load(file)

#%%
logger.info('Data Processing')
def gen_loac(data,a,b,c,d):
    avg = np.average(data)
    var = np.var(data)
    p = 1/(1+math.exp(-(c*(a*avg+b)+d*var)))
    return p

f = open(save_path,'w')
writer = csv.writer(f,delimiter='\t')
writer.writerow(['Gene','L-score'])
for gene in tqdm(gene_distance):
    if len(gene_distance[gene]) > 10:
        p = gen_loac(gene_distance[gene],-0.3937,4.2381,4.0053, 0.0551)
        writer.writerow([gene,p])
f.close()
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


#%%
# input_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin_with_background.GeneLocation.pickle'
# save_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin_with_background.CellCenter.pickle'

import argparse
parse = argparse.ArgumentParser()
parse.add_argument('-i',type=str,required=True,help='GeneLocation.pickle file which generate by GeneLocation.py')
parse.add_argument('-s',type=str,required=True,help='save path')
args = parse.parse_args()
input_path = args.i
save_path  = args.s




# 从pickle文件加载字典
logger.info('Data Loading')
with open(input_path, 'rb') as file:
    gene_location = pickle.load(file)

#%%
# 创建logger对象

logger.info('Data Processing')
data = {}
for cell in tqdm(gene_location.keys()):
    if cell == '0.0':
        print(cell)
    temp = []
    for gene in gene_location[cell]:
        temp.extend(gene_location[cell][gene])
    temp = np.array(temp)
    x = np.mean(temp[:,0])
    y = np.mean(temp[:,1])
    data[cell] = [x,y]
#%%
with open(save_path, 'wb') as file:
    pickle.dump(data, file)

import os
import pickle
import logging
from tqdm import tqdm
import argparse
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


#%% 参数
parse = argparse.ArgumentParser()
parse.add_argument('-i',type=str,required=True,help='input tsv file include gene cell and it coordinate, see example.file')
parse.add_argument('-s',type=str,required=True,help='save path')
args = parse.parse_args()
# input_path = '/mnt/dfc_data2/project/linyusen/database/11_stereo_seq/Mouse_brain_Adult_GEM_CellBin.tsv'
# save_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.GeneLocation.pickle'
input_path = args.i
save_path  = args.s
#%%
logger.info('Data Loading')
f = open(input_path)
lines = f.readlines()
f.close()


logger.info('Data Processing')
data = {}
for line in tqdm(lines[1:]):
    line = line[:-1]
    line = line.split('\t')
    gene,x,y,_,cell = line
    x = int(x)
    y = int(y)
    if cell not in data:
        data[cell] = {}
    if gene not in data[cell].keys():
        data[cell][gene] = []
    data[cell][gene].append([x,y])
#%%
with open(save_path, 'wb') as file:
    pickle.dump(data, file)
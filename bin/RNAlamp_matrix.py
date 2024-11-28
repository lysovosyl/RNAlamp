import os
import pickle
import logging
from tqdm import tqdm
import argparse
import numpy as np
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
save_dir  = args.s

if os.path.exists(save_dir) == False:
    os.makedirs(save_dir)
#%%
logger.info('Data Loading')
f = open(input_path)
lines = f.readlines()
f.close()


logger.info('GeneLocation Processing')
GeneLocation = {}
GeneLocation_savepath = os.path.join(save_dir,'GeneLocation.pickle')
for line in tqdm(lines[1:]):
    line = line[:-1]
    line = line.split('\t')
    gene,x,y,_,cell = line
    x = int(x)
    y = int(y)
    if cell not in GeneLocation:
        GeneLocation[cell] = {}
    if gene not in GeneLocation[cell].keys():
        GeneLocation[cell][gene] = []
    GeneLocation[cell][gene].append([x,y])
with open(GeneLocation_savepath, 'wb') as file:
    pickle.dump(GeneLocation, file)
#%%
logger.info('CellCenter Processing')
CellCenter = {}
CellCenter_savepath = os.path.join(save_dir,'CellCenter.pickle')
for cell in tqdm(GeneLocation.keys()):
    if cell == '0.0':
        print(cell)
    temp = []
    for gene in GeneLocation[cell]:
        temp.extend(GeneLocation[cell][gene])
    temp = np.array(temp)
    x = np.mean(temp[:,0])
    y = np.mean(temp[:,1])
    CellCenter[cell] = [x,y]
with open(CellCenter_savepath, 'wb') as file:
    pickle.dump(CellCenter, file)
#%%
logger.info('GeneDistance Processing')
gene_list = []
for cell in GeneLocation:
    gene_list.extend(list(GeneLocation[cell].keys()))
gene_list = set(gene_list)
GeneDistance = {}
GeneDistance_savepath = os.path.join(save_dir,'GeneDistance.pickle')
for gene in tqdm(gene_list):
    cell_array = []
    gene_array = []
    for cell in GeneLocation:
        if gene in GeneLocation[cell].keys():
            for xy in GeneLocation[cell][gene]:
                cell_array.append(CellCenter[cell])
                gene_array.append(xy)
    cell_array = np.array(cell_array)
    gene_array = np.array(gene_array)
    distances = np.linalg.norm(cell_array - gene_array, axis=1)
    GeneDistance[gene] = distances
with open(GeneDistance_savepath, 'wb') as file:
    pickle.dump(GeneDistance, file)
#%%
logger.info('CoordinateMatrix Processing')
CoordinateMatrix = {}
CoordinateMatrix_savepath = os.path.join(save_dir,'CoordinateMatrix.pickle')
for cell in tqdm(GeneLocation):
    for gene in GeneLocation[cell]:
        for coordinate in GeneLocation[cell][gene]:
            x = coordinate[0]
            y = coordinate[1]
            if x not in CoordinateMatrix:
                CoordinateMatrix[x] = {}
                if y not in CoordinateMatrix[x].keys():
                    CoordinateMatrix[x][y] = {}
            else:
                if y not in CoordinateMatrix[x].keys():
                    CoordinateMatrix[x][y] = {}
            if gene not in CoordinateMatrix[x][y].keys():
                CoordinateMatrix[x][y][gene] = 1
            else:
                CoordinateMatrix[x][y][gene] += 1
with open(CoordinateMatrix_savepath, 'wb') as file:
    pickle.dump(CoordinateMatrix, file)

#%%
from collections import defaultdict
logger.info('GeneColocation Processing')
gene_convert = defaultdict(list)
for cell in GeneLocation:
    for gene in GeneLocation[cell].keys():
        gene_convert[gene].extend(GeneLocation[cell][gene])
GeneColocation = {}
GeneColocation_savepath = os.path.join(save_dir,'GeneColocation.pickle')
radius = 1
for reference_gene in tqdm(gene_convert.keys()):
    GeneColocation[reference_gene] = defaultdict(int)
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
                    for gene in CoordinateMatrix[x_index][y_index].keys():
                        region.append(gene)
                except:
                    pass
        region = list(set(region))
        for gene in region:
            GeneColocation[reference_gene][gene] += 1
with open(GeneColocation_savepath, 'wb') as file:
    pickle.dump(GeneColocation, file)

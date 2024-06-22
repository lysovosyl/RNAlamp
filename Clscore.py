import os
import pickle
import logging
import numpy as np
from tqdm import tqdm
import csv
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
# GeneCoLocation_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.GeneColocation.pickle'
# save_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.CLscore.tsv'


import argparse
parse = argparse.ArgumentParser()
parse.add_argument('-igl',type=str,required=True,help='GeneLocation file which generate by GeneLocation.py')
parse.add_argument('-icm',type=str,required=True,help='CoordinateMatrix file which generate by CoordinateMatrix.py')
parse.add_argument('-igc',type=str,required=True,help='GeneCoLocation file which generate by GeneColocation.py')
parse.add_argument('-s',type=str,required=True,help='save path')
args = parse.parse_args()
# input_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.GeneDistance1.pickle'
# save_path = '/mnt/dfc_data2/project/linyusen/database/53_stero_seq_github_test/Mouse_brain_Adult_GEM_CellBin.Lscore.tsv'
GeneLocation_path = args.igl
CoordinateMatrix_path  = args.icm
GeneCoLocation_path = args.igc
save_path  = args.s
#%%
logger.info('Data Loading')
with open(GeneLocation_path, 'rb') as file:
    GeneLocation = pickle.load(file)

with open(CoordinateMatrix_path, 'rb') as file:
    CoordinateMatrix = pickle.load(file)

with open(GeneCoLocation_path, 'rb') as file:
    GeneCoLocation = pickle.load(file)
#%%
logger.info('Data Processing')
gene_convert = defaultdict(list)
for cell in GeneLocation:
    for gene in GeneLocation[cell].keys():
        gene_convert[gene].extend(GeneLocation[cell][gene])
#%%
gene_count = {}
for gene in gene_convert:
    gene_count[gene] = len(gene_convert[gene])

#%%
f = open(save_path,'w')
writer = csv.writer(f,delimiter='\t')
writer.writerow(['reference_gene','observe_gene','reference_num','observe_num','observe|reference','reference|observe','clscore'])
for reference_name in tqdm(GeneCoLocation):
    for observe_name in GeneCoLocation[reference_name]:
        if reference_name in gene_count.keys() and observe_name in gene_count.keys():
            reference_num = gene_count[reference_name]
            observe_num = gene_count[observe_name]
            if reference_num > observe_num:
                rna1_count = reference_num
                rna2_count = observe_num
                rna1_name  = reference_name
                rna2_name  = observe_name
            else:
                rna2_count = reference_num
                rna1_count = observe_num
                rna2_name = reference_name
                rna1_name = observe_name
            clscore = GeneCoLocation[rna1_name][rna2_name]/rna2_count/np.log10(rna1_count/rna2_count+10)
            writer.writerow([reference_name,observe_name,reference_num,observe_num,GeneCoLocation[reference_name][observe_name],GeneCoLocation[observe_name][reference_name],clscore])
f.close()


RNAlamp
=======================================

Introduction
------------
**RNAlamp** is a software use to explore RNA localization in subcellar using spatial transcriptome data.

Require：

numpy

pickle

tqdm

Install
------------
```
git clone https://github.com/lysovosyl/RNAlamp.git
cd RNAlamp
conda create -n RNAlamp python==3.8
conda activate RNAlamp
pip install numpy pickle tqdm
```

Usage
------------
Before to use this software, make sure you have prepered a suitable data file(tsv format), an example data can be downloaded from https://xxxx
L-score
-----------------
Introduction
-----------------
L-score is a score be used to explore whether a gene locate in nucleus or cytoplasm, to calculate this score, you should use Mouse_brain_Adult_GEM_CellBin.tsv as input

Step by step
-----------------

```
python ./RNAlamp_matrix.py -i ./data/Mouse_brain_Adult_GEM_CellBin.tsv -s ./result/Mouse_brain_Adult_GEM_CellBin
```

```
python ./Lscore.py -i ./result/Mouse_brain_Adult_GEM_CellBin/GeneDistance.pickle -s ./result/Mouse_brain_Adult_GEM_CellBin/Lscore.tsv
```



CL-score
-----------------
Introduction
-----------------
CL-score is a score be used to explore whether a pair gene has colocalization relation, to calculate this score, you should use Mouse_brain_Adult_GEM_CellBin_with_background.tsv as input

Step by step
-----------------

```
python ./RNAlamp_matrix.py -i ./data/Mouse_brain_Adult_GEM_CellBin_with_background.tsv -s ./result/Mouse_brain_Adult_GEM_CellBin_with_background
```

```
python ./CLscore.py -igl ./result/Mouse_brain_Adult_GEM_CellBin_with_background/GeneLocation.pickle -icm ./result/Mouse_brain_Adult_GEM_CellBin_with_background/CoordinateMatrix.pickle -igc ./result/Mouse_brain_Adult_GEM_CellBin_with_background/GeneColocation.pickle -s ./result/Mouse_brain_Adult_GEM_CellBin_with_background/CLscore.tsv
```




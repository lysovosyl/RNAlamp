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
git clone https://github.com/lysovosyl/RNAloc.git
cd RNAloc
conda create -n RNAloc python==3.8
pip install numpy pickle tqdm
```

Usage
------------
Before to use this software, make sure you have prepered a suitable data file(tsv format), an example data can be downloaded from https://xxxx
L-score
-----------------
Introduction
-----------------
L-score is a score be used to explore whether a gene locate in nucleus or cytoplasm

Step by step
-----------------

```
python ./GeneLocation.py -i ./data/Mouse_brain_Adult_GEM_CellBin.tsv -s ./result/Mouse_brain_Adult_GEM_CellBin.GeneLocation.pickle
```
```
python ./CellCenter.py -i ./result/Mouse_brain_Adult_GEM_CellBin.GeneLocation.pickle -s ./result/Mouse_brain_Adult_GEM_CellBin.CellCenter.pickle
```
```
python ./GeneDistanceToCenter.py -ic ./result/Mouse_brain_Adult_GEM_CellBin.CellCenter.pickle -ig ./result/Mouse_brain_Adult_GEM_CellBin.GeneLocation.pickle -s ./result/Mouse_brain_Adult_GEM_CellBin.GeneDistanceToCenter.pickle
```
```
python ./Lscore.py -i ./result/Mouse_brain_Adult_GEM_CellBin.GeneDistanceToCenter.pickle -s ./result/Mouse_brain_Adult_GEM_CellBin.Lscore.tsv
```



CL-score
-----------------
Introduction
-----------------
CL-score is a score be used to explore whether a pair gene has colocalization relation.

Step by step
-----------------

```
python ./GeneLocation.py -i ./data/Mouse_brain_Adult_GEM_CellBin_with_background.tsv -s ./result/Mouse_brain_Adult_GEM_CellBin_with_background.GeneLocation.pickle
```
```
python ./CoordinateMatrix.py -i ./result/Mouse_brain_Adult_GEM_CellBin_with_background.GeneLocation.pickle -s ./result/Mouse_brain_Adult_GEM_CellBin_with_background.CoordinateMatrix.pickle
```
```
python ./GeneColocation.py -ic ./result/Mouse_brain_Adult_GEM_CellBin_with_background.CoordinateMatrix.pickle -ig ./result/Mouse_brain_Adult_GEM_CellBin_with_background.GeneLocation.pickle -s ./result/Mouse_brain_Adult_GEM_CellBin_with_background.GeneColocation.pickle
```
```
python ./Lscore.py -igl ./result/Mouse_brain_Adult_GEM_CellBin_with_background.GeneLocation.pickle -icm ./result/Mouse_brain_Adult_GEM_CellBin_with_background.CoordinateMatrix.pickle -igc ./result/Mouse_brain_Adult_GEM_CellBin_with_background.GeneColocation.pickle -s ./result/Mouse_brain_Adult_GEM_CellBin_with_background.Clscore.tsv
```




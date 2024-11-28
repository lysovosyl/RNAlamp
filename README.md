RNAlamp
=======================================

Analyzing RNAs with a lamp in cells.

## Table of Contents

- [Introduction](#Introduction)
- [Install](#Install)
- [Input](#Input)
- [Preprocessing](#Preprocessing)
- [L-score](#L-score)
- [CL-score](#CL-score)
- [Contributors](#Contributors)
- [Citation](#Citation)
- [License](#License)


Introduction
------------
**RNAlamp** is a flexible computational framework for dissecting the subcellular localization of lncRNA and its interacting RNAs in a high resolution.It maps the spatial localization of thousands of endogenous RNAs in subcellular resolution and its adherent interactions using spatial RNA-seq datasets. RNAlamp calculates the L-score and CL-score to provide these capabilities in RNA subcellular localization analyses.

RNAlamp requires the following python packages including: python3.8, numpy, pickle, tqdm etc.


Install
------------

```
# clone RNAlamp
git clone https://github.com/lysovosyl/RNAlamp.git
cd RNAlamp

# create the environment by conda and install the requried packages
conda create -n RNAlamp python==3.8
conda activate RNAlamp

pip install numpy pickle tqdm
```

Input
------------

The input date is formated as follows (TSV format):
```
geneID         x      y      UMICount  label
Gm26825        13476  11944  1         27298.0
Gm42418        13476  11944  1         27298.0
Pja1           8758   13656  1         37442.0
Cx3cl1         8758   13656  1         37442.0
Mgat3          11661  11611  1         25246.0
Gng3           5630   14950  1         44380.0
Sgce           10844  16087  1         49884.0
Ptgds          5722   8775   1         9239.0
Cpsf6          9361   18009  2         56356.0
B4galt6        11234  11946  2         27296.0
...
```
The "geneID", "x", "y" and "label" is required for the input dataset. "label" represents the cell label; "x" and "y" represent the coordinates of each observed gene.

The MOSTA data used in our study can download from CNGB (https://ftp.cngb.org/pub/SciRAID/stomics/STDS0000058/Cell_bin_matrix/Mouse_brain_Adult_GEM_CellBin.tsv.gz ).

```
mkdir ./test
cd ./test
wget https://ftp.cngb.org/pub/SciRAID/stomics/STDS0000058/Cell_bin_matrix/Mouse_brain_Adult_GEM_CellBin.tsv.gz
gunzip Mouse_brain_Adult_GEM_CellBin.tsv.gz
```


Preprocessing
-----------------

```
mkdir ./result
python ../bin/RNAlamp_matrix.py -i ./Mouse_brain_Adult_GEM_CellBin.tsv -s ./result/Mouse_brain_Adult_GEM_CellBin
```

This step results the dataset for L-score and CL-score calcualtion including CellCenter.pickle, CoordinateMatrix.pickle, GeneColocation.pickle, GeneDistance.pickle and GeneLocation.pickle.

L-score
-----------------

L-score defined as the distance of an RNA molecule relative to the centroid of each cell in terms of the mean distance of all RNAs within an experiment; a sigmoid function was applied to obtain the final L-score range from 0 to 1; thus, a higher L-score means more likely to localize in cytoplasm, vice versa.

```
python ../bin/Lscore.py -i ./result/Mouse_brain_Adult_GEM_CellBin/GeneDistance.pickle -s ./result/Mouse_brain_Adult_GEM_CellBin/Lscore.tsv
```

The output file is Lscore.tsv.

```
Gene            L-score
Gm49144         0.9353881054211588
Nsun3           0.496691475553424
Ten1            0.1683513817488177
Strip1          0.18299108720649007
Magee1          0.16542023517317442
Gm47728         0.7895910952083053
Cldn23          0.25790137977161215
Wdr27           0.32098171648355134
Lrmda           0.9360376081525656
Stat3           0.35275055231835245
```

CL-score
-----------------

CL-score is the degree of the co-occurrence of rna1 and rna2 reciprocally. The larger CL-score means the more probability of co-localization of rna1 and rna2.

```
python ../bin/CLscore.py -igl ./result/Mouse_brain_Adult_GEM_CellBin_with_background/GeneLocation.pickle -icm ./result/Mouse_brain_Adult_GEM_CellBin_with_background/CoordinateMatrix.pickle -igc ./result/Mouse_brain_Adult_GEM_CellBin_with_background/GeneColocation.pickle -s ./result/Mouse_brain_Adult_GEM_CellBin_with_background/CLscore.tsv
```

The output file is CLscore.tsv.

```
reference_gene  observe_gene   reference_num  observe_num  observe|reference  reference|observe  clscore
Cr2             Cdh20          73             2442         1                  2                  0.016725938758823885
Cr2             Gigyf2         73             4718         2                  2                  0.014628144581652834
Cr2             Adcy2          73             7638         1                  1                  0.006652084710161676
Cr2             Mxi1           73             5678         1                  1                  0.007048797290171357
Cr2             Gm28043        73             4828         1                  1                  0.00728032609008191
Cr2             Bex2           73             85874        1                  1                  0.004455976478707606
Cr2             Cr2            73             73           73                 73                 0.9602525677891274
Cr2             Ank2           73             39755        3                  4                  0.019969057576367348
Cr2             Mtr            73             1014         1                  1                  0.009939337806628402
Cr2             Rnf19a         73             2649         1                  1                  0.008225106747420765
```

### Contributors

[Jiajian Zhou](https://github.com/zhoujj2013) and [Yusen Lin](https://github.com/lysovosyl) designed this project. Yusen Lin implemented the L-score and CL-score calculation.


### Citation

J.L., Y.L. et al. Profiling RNA subcellular localization and RNA-RNA colocalization network using spatial single-cell RNA sequencing.

### License

[MIT](LICENSE) © Yusen Lin

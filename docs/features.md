---
icon: octicons/milestone-24
description: Features
---

# Features

[![PyPI](https://img.shields.io/pypi/v/careamics.svg?color=green)](https://pypi.org/project/careamics)

CAREamics is an on-going project and the API is not yet stable.

## Officially supported features (v0.0.15)

- Installation from conda and mamba
- Data formats
    - in-memory arrays
    - tiff files
- Training
    - training in memory or from multiple files
    - choose number of epochs and steps per epochs
- Prediction
    - Tiled prediction
- Algorithms
    - Content-aware image restoration (CARE) [[ref](https://www.nature.com/articles/s41592-018-0216-7)]
    - Noise2Noise [[ref](https://arxiv.org/abs/1803.04189)]
    - Noise2Void [[ref1](https://openaccess.thecvf.com/content_CVPR_2019/html/Krull_Noise2Void_-_Learning_Denoising_From_Single_Noisy_Images_CVPR_2019_paper.html), [ref2](https://proceedings.mlr.press/v97/batson19a.html)]
    - N2V2 [[ref](https://link.springer.com/chapter/10.1007/978-3-031-25069-9_33)]
- napari UI



## Current work

- Next-generation dataset
    - data formats: 
        - Zarr
        - CZI
    - flexible, modular
    - arbitrary data organization
    - on-line statistics estimation
    - data masking
    - background patch rejection
- Prediction
    - direct tile writing (e.g. Zarr)
- Algorithms
    - P(P)N2V [[ref1](), [ref2]()]
    - Hierarchical DivNoising [[ref1](), [ref2]()]
    - MicroSplit [[ref]()]
- Stand-alone UI


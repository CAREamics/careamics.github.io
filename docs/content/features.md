---
icon: lucide/signpost
description: Features.
---

This pages lists the progress of CAREamics towards `v1.0.0`. We list future development,
in particular regarding the inclusion of new algorithms, or interoperatibility bridges. 
Future version will be indexed based on new algorithm additions.

## APIs

- [x] CAREamist API: user-friendly API for training and prediction.
- [x] Lightning API: using CAREamics modules in PyTorch Lightning for more control and flexibility.

## Algorithms

Only algorithms fully integrated into the CAREamics API are checkmarked.

- [x] Noise2Void, N2V2, structN2V
- [x] CARE, Noise2Noise
- [ ] UNet semantic segmentation
- [ ] HDN
- [ ] MicroSplit
- [ ] COSDD
- [ ] cryoCARE

To request algorithms to be added, please contribute to the [discussion on Github](https://github.com/CAREamics/careamics/issues/611).

## File formats

We do not expect to maintain more file formats, but we provide dependency injection
mechanisms to allow you to easily consume your own file formats.

- [x] numpy arrays in memory
- [x] TIFF format
- [x] Zarr format (without OME-NGFF metadata)
- [x] CZI format
- [x] Custom format via a simple read function
- [x] Custom format via a more complex `ImageStack` implementation
- [ ] OME-NGFF (Zarr with OME-NGFF metadata support)
- [ ] Memory-mapped MRC (cryoCARE)

## Features

### Training

- [x] Patch exclusion using a mask
- [x] Background patch filtering
- [x] Training from list of files without loading them all in memory
- [x] Training from NGFF format (Zarr only) 
- [x] Splitting validation from training data
- [x] Skipping validation (Noise2Void only)

### Logging

- [x] WandB and Tensorboard logging (thanks to PyTorch Lightning)
- [ ] Metrics and validation image saving during training

### Prediction

- [x] Tile-by-tile prediction to disk (for Zarr)


## Interoperability

- [ ] CLI
- [ ] napari plugin / stand-alone UI
- [ ] nextflow/nf-core modules
- [ ] HPC examples
# Frequently asked questions


## Prediction

### Sizes of tensors must match

If you get an error similar to:

```python
RuntimeError: Sizes of tensors must match except in dimension 1. Expected size 320 but got size 321 for tensor number 1 in the list.
```

This is likely because the input data size is not compatible with the model (e.g. the
model has layers that downsample the data, then upsample it, and this is only 
compatible with dimensions that are power of 2!).

!!! success "Solution"
    By [tiling](usage/prediction.md#tiling) the prediction, you can ensure that every
    input to the model has the correct shape. Then upon stitching back the tiles, you
    recover your whole image!
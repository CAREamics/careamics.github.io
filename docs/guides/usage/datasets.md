# Datasets

Datasets are the internal classes providing the individual patches for training, 
validation and prediction. In CAREamics, we provide a `CAREamicsTrainData` class that 
creates the datasets for training and validation (there is a class for prediction
as well, which is simpler and shares some parameters with the training one). In most cases,
it is created internally. In this section, we describe what it does and shed light on
some of its parameters that are passed to the [train methods](training).

## Overview

The `CAREamicsTrainData` receives both data configuration and data itself. The data
can be passed a path to a folder, to a file or as `numpy` array. 


```python title="Simplest way to instantiate CAREamicsTrainData"
from careamics.config import create_n2v_configuration
from careamics import CAREamicsTrainData
import numpy as np

train_array = np.random.rand(128, 128)

config = create_n2v_configuration(
    experiment_name="n2v_2D",
    data_type="array",
    axes="YX",
    patch_size=[64, 64],
    batch_size=1,
    num_epochs=1,
)

data_module = CAREamicsTrainData( # (1)!
    data_config=config.data_config,
    train_data=train_array
)
```

It has the following parameters:

- `data_config`: data configuration
- `train_data`: training data (array or path)
- `(optional) val_data`: validation data, if not provided, the validation data is taken from the training data
- `(optional) train_data_target`: target data for training (if applicable)
- `(optional) val_data_target`: target data for validation (if applicable)
- `(optional) read_source_func`: function to read custom data types 
    (see [custom data types](#advanced-custom-data-types))
- `(optional) extension_filter`: filter to select custom types
    (see [custom data types](#advanced-custom-data-types))
- `(optional) val_percentage`: percentage of validation data to extract from the training
    (see [splitting validation](../training/#splitting-validation-from-training-data))
- `(optional) val_minimum_split`: minimum validation split 
    (see [splitting validation](../training/#splitting-validation-from-training-data))
- `(optional) use_in_memory`: whether to use in-memory dataset if possible (Default is `True`), 
    not applicable to mnumpy arrays.

Depending on the type of the data, which is specified in the `data_config` and
is compared to the type of `train_data`, the `CAREamicsTrainData` will create the appropriate
dataset for both training and validation data.

In the absence of validation, validation data is extracted from training data
(see [splitting validation](../training/#splitting-validation-from-training-data)).


## Available datasets

CAREamics currently support two datasets:

- [InMemoryDataset](#in-memory-dataset): used when the data fits in memory.
- [IterableDataset](#iterable-dataset): used when the data is too large to fit in memory.

If the data is a `numpy` array, the `InMemoryDataset` is used automatically. Otherwise,
we list the files contained in the path, compute the size of the data and instantiate
an `InMemoryDataset` **if the data is less than 80% of the total RAM size**. If not,
CAREamics instantiate an `IterableDataset`.

Both datasets work differently, and the main differences can be summarized as follows:

| Feature          | `InMemoryDataset`    | `IterableDataset`   |
| ---------------- | -------------------- | ------------------- |
| Used with arrays | :material-check: Yes | :material-close: No |
| Patch extraction | Sequential           | Random              |
| Data loading     | All in memory        | One file at a time  |


In the next sections, we describe the different steps they perform.


### In-memory dataset

As the name implies, the in-memory dataset loads all the data in memory. It is used when
the data on the disk seems to fit in memory, or when the data is already in memory and 
passed as a numpy array. The advantage of the dataset is that is allows faster access
to the patches, and therefore faster training time.

It performs the following steps:

=== ":material-application-array-outline: On numpy arrays"

    1. Compute the `mean` and `std` of the dataset over all images.
    2. Reshape the array so that the axes are ordered following the convention `SC(Z)YX`.
    3. Extract patches sequentially so that they cover all images and keep them
        in memory.
    4. Update the `mean` and `std` in the configuration if they were not provided. This step
        also updates the `mean` and `std` of the normalization transform.
    5. Get the transforms from the configuration.
    6. Each time a patch is requested:
        1. A patch is extracted from the in-memory patches, it has dimensions `(1, C, (Z), Y, X)`, 
            where `C` is the number of channels, `Z` is present only if the data is 3D, and
            `Z, Y, X` are the patch sizes in each dimension.
        2. The transformations are applied to the patch (see [transforms](#intermediate-transforms)).
        3. The result of the transformation is returned.


=== ":octicons-rel-file-path-16: On Paths"

    1. For each file in the path, the corresponding image is loaded.
    2. The `mean` and `std` are computed for the loaded image.
    3. The image is reshaped so that the axes are ordered following the convention `SC(Z)YX`.
    4. Extract patches sequentially so that they cover the whole image and keept them
        in memory.
    5. Once all files have been processed, the average `mean` and `std` are computed.
    6. Update the `mean` and `std` in the configuration if they were not provided. This step
        also updates the `mean` and `std` of the normalization transform.
    7. All patches are concatenated together.
    8. Get the transforms from the configuration.
    9. Each time a patch is requested:
        1. A patch is extracted from the in-memory patches, it has dimensions `(1, C, (Z), Y, X)`, 
            where `C` is the number of channels, `Z` is present only if the data is 3D, and
            `Z, Y, X` are the patch sizes in each dimension.
        2. The transformations are applied to the patch (see [transforms](#intermediate-transforms)).
        3. The result of the transformation is returned.


!!! note "What about supervised training?"

    For supervised training, the steps are the same and are performed for the targets
    alongside the source.


!!! note "What if I have a time (`T`) axis?"

    `T` axes are accepted by the CAREamics configuration, but are treated as a sample
    dimension (`S`). If both `S` and `T` are present, the two axes are concatenated.


### Iterable dataset

The iterable dataset is used to load patches from a single file at a time, one file after
another. This allows training on datasets that are too large to fit in memory. This dataset
is exclusively used with files input (data passed as paths).

It performs the following steps:

1. The dataset does a first pass of all the data to compute the average `mean` and `std`,
    if these have not been specified in the configuration.
2. Update the configuration and the transforms with the computed `mean` and `std`.
3. Get the list of transforms from the configuration.
4. Each time a patch is requested:
    1. If there is no more patches (see point 6), the next image is loaded.
    2. The image is reshaped so that the axes are ordered following the convention `SC(Z)YX`.
    4. Random patches are extracted from the image, they have dimensions `(N, C, (Z), Y, X)`, 
        where `C` is the number of channels, `Z` is present only if the data is 3D,
        `Z, Y, X` are the patch sizes in each dimension, and `N` is the number of patches.
    5. The transformations are applied to the patches (see [transforms](#intermediate-transforms)).
    6. The next patch is yielded. The patches are yielded one at a time until there are no more patches
        in the image, at which point the next image is loaded when the next patch is requested (see point 1).


!!! note "What about supervised training?"

    For supervised training, the steps are the same and are performed for the targets
    alongside the source.


!!! note "What if I have a time (`T`) axis?"

    `T` axes are accepted by the CAREamics configuration, but are treated as a sample
    dimension (`S`). If both `S` and `T` are present, the two axes are concatenated.


## (Intermediate) Transforms

Transforms are augmentations and any operation applied to the patches before feeding them
into the network. CAREamics supports the following transforms (see 
[configuration full spec](../../configuration/full_spec) for an example on how to configure them):


| Transform               | Description                                  | Notes                                 |
| ----------------------- | -------------------------------------------- | ------------------------------------- |
| `Normalize`             | Normalize (zero mean, unit variance)         | Necessary                             |
| `NDFlip`                | Flip the image along one of the spatial axis | X, Y and Z (not by default), optional |
| `XYRandomRotate90Model` | Rotate by 90 degrees the XY axes             | Optional                              |
| `N2VManipulateModel`    | N2V pixel manipulation                       | Only for N2V, necessary               |


The `Normalize` transform is always applied, and the rest are optional. The exception is
`N2VManipulateModel`, which is only applied when training with N2V (see [Noise2Void](../../algorithms/n2v)).

!!! note "When to turn off transforms?"

    The configuration allows turning off transforms. In this case, only normalization
    (and potentially the `N2VManipulateModel` for N2V) is applied. This is useful when
    the structures in your sample are always in the same orientation, and flipping and
    rotation do not make sense.


## (Advanced) Custom data types

To read custom data types, you can set `data_type` to `custom` in `data_config`
and provide a function that returns a numpy array from a path as
`read_source_func` parameter. The function will receive a Path object and
an axies string as arguments, the axes being derived from the `data_config`.

You should also provide a `fnmatch` and `Path.rglob` compatible expression (e.g.
"*.npy") to filter the files extension using `extension_filter`.


```python title="Read custom data types"
from pathlib import Path
from typing import Any

import numpy as np
from careamics import CAREamicsTrainData
from careamics.config import create_n2v_configuration

def read_npy( # (1)!
        path: Path, # (2)!
        *args: Any,
        **kwargs: Any, # (3)!
    ) -> np.ndarray:
    return np.load(path) # (4)! 

# example data
train_array = np.random.rand(128, 128)
np.save("train_array.npy", train_array)

# configuration
config = create_n2v_configuration(
    experiment_name="n2v_2D",
    data_type="custom", # (5)!
    axes="YX",
    patch_size=[32, 32],
    batch_size=1,
    num_epochs=1,
)

data_module = CAREamicsTrainData(
    data_config=config.data_config, 
    train_data="train_array.npy", # (6)!
    read_source_func=read_npy, # (7)!
    extension_filter="*.npy", # (8)!
)
data_module.prepare_data()
data_module.setup() # (9)!

# check dataset output
dataloader = data_module.train_dataloader()
print(dataloader.dataset[0][0].shape) # (10)!
```

1. We define a function that reads the custom data type.

2. It takes a path as argument!

3. But it also need to receive `*args` and `**kwargs` to be compatible with the `read_source_func` signature.

4. It simply returns a `numpy` array.

5. The data type must be `custom`!

6. And we pass a `Path | str`.

7. Simply pass the method by name.

8. We also need to provide an extension filter that is compatible with `fnmatch` and `Path.rglob`.

9. These two lines are necessary to instantiate the training dataset that we call at the end. They are
    called automatically by PyTorch Lightning during training.

10. The dataloader gives access to the dataset, we choose the first element, and since
    we configured CAREamics to use N2V, the output is a tuple whose first element is our
    first patch!


## Prediction datasets

The prediction data module, `CAREamicsPredictData` works similarly to `CAREamicsTrainData`, albeit
with fewer parameters:


- `pred_config`: data configuration
- `pred_data`: prediction data (array or path)
- `(optional) read_source_func`: function to read custom data types 
    (see [custom data types](#advanced-custom-data-types))
- `(optional) extension_filter`: filter to select custom types
    (see [custom data types](#advanced-custom-data-types))

It uses `InMemoryPredictionDataset` for arrays and `IterablePredictionDataset` for paths. These
are similar to their training counterparts, but they have simpler transforms and offer the possibility
to run test-time augmentation. For more details, refer to the [prediction section](../prediction).

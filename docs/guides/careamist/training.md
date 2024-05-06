# Training

You can provide data in various way to train your model: as a `numpy` array, using a
path to a folder or files, or by using CAREamics data module class for more control
(advanced).

The details of how CAREamics deals with the loading and patching is detailed in the
[dataset section](datasets).


!!! warning "Data type"
    The data type of the source and targets must be the same as the one specified in the configuration.
    That is to say `array` in the case of `np.ndarray`, and `tiff` in the case of paths.


## Training by passing an array

CAREamics can be trained by simply passing numpy arrays.

```python title="Training by passing an array"
import numpy as np

train_array = np.random.rand(128, 128)
val_array = np.random.rand(128, 128)

careamist.train(
    train_source=train_array, # (1)!
    val_source=val_array, # (2)!
)
```

1. All parameters to the `train` method must be specified by keyword.
2. If you don't provide a validation source, CAREamics will use a fraction of the training data
   to validate the model.


!!! info "Supervised training"
    If you are training a supervised model, you must provide the target data as well.

    ```python
    careamist.train(
        train_source=train_array,
        train_target=target_array,
        val_source=val_array,
        val_target=val_target_array,
    )
    ```

## Training by passing a path

The same thing can be done by passing a path to a folder or files.

```python title="Training by passing a path"
careamist.train(
    train_source="path/to/my/train_data.tiff", # (1)!
    val_source="path/to/my/val_data.tiff",
)
```

1. The path can point to a single file, or contain multiple files.

## Splitting validation from training data

If you only provide training data, CAREamics will extract the validation data directly
from the training set. There are two parameters controlling that behaviour: `val_percentage`
and `val_minimum_split`.

`val_percentage` is the fraction of the training data that will be used for validation, and
`val_minimum_split` is the minimum number of iamges used. If the percentage leads to a 
number of patches smaller than `val_minimum_split`, CAREamics will use `val_minimum_split`.

```python title="Splitting validation from training data"
careamist.train(
    train_source=train_array,
    val_percentage=0.1, # (1)!
    val_minimum_split=5, # (2)!
)
```

1. 10% of the training data will be used for validation.
2. If the number of images is less than 5, CAREamics will use 5 images for validation.


!!! warning "Patches vs images"
    The behaviour of `val_percentage` and `val_minimum_split` is based different depending
    on whether the source data is an array or a path. If the source is an array, the
    split is done on the patches (`N` patches are used for validation). If the source is a
    path, the split is done on the files (`N` files are used for validation).


## Training by passing a CAREamicsTrainData object

CAREamics provides a class to handle the data loading of custom data type. We will dive 
in more details in the next section into what this class can be used for.

```python title="Training by passing a CAREamicsTrainData object"
from careamics import CAREamicsTrainData

data_module = CAREamicsTrainData( # (1)!
    data_config=config.data_config,
    train_source=train_array
)

careamist.train(
    datamodule=data_module
)
```

1. Here this does the same thing as passing the `train_source` directly into the `train` method.
    In the next section, we will see a more useful example.


## Callbacks

!!! warning "In construction"
    This section is still under construction.


## Logging the training

!!! warning "In construction"
    This section is still under construction.


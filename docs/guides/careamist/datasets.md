# Datasets

Datasets are the internal classes providing the individual patches for training, 
validation and prediction. In CAREamics, we provide a `CAREamicsTrainData` class that 
creates the datasets for training and validation (there is a class for prediction
as well, which is simpler and shares some parameters with the training one). In most cases,
it is created internally. In this section, we describe what it does and shed light on
some of its parameters that are passed to the [train methods](training).

## Overview

The `CAREamicsTrainData` receives both data configuration and data itself. The data
can be passed a path to a folder, to a file or as `numpy` array. It has the following 
parameters:

- `data_config`
- `train_data`
- `(optional) val_data`
- `(optional) train_data_target`
- `(optional) val_data_target`
- `(optional) read_source_func`
- `(optional) extension_filter`
- `(optional) val_percentage`
- `(optional) val_minimum_split`
- `(optional) use_in_memory`

Depending on the type of the data, which is specified in the `data_config` parameter and
is compared to the data received, the `CAREamicsTrainData` will create the appropriate
dataset.

CAREamics currently support two datasets:

- `InMemoryDataset`: This dataset is used when the data fits in memory.
- `IterableDataset`: This dataset is used when the data is too large to fit in memory.

If the data is a `numpy` array, the `InMemoryDataset` is used automatically. Otherwise,
we list the files contained in the path, compute the size of the data and instantiate
an `InMemoryDataset` if the data is less than 80% of the total RAM size. Otherwise,
we instantiate an `IterableDataset`.

Both datasets work differently.



mean and std calculation

## In-memory dataset

memory calculation
random patching

## Iterable dataset

sequential patching

## (Advanced) Custom data types


---
description: Convenience functions
---

# Convenience functions

As building a full CAREamics configuration requires a complete understanding of the 
various parameters and experience with Pydantic, we provide convenience functions
to create configurations with a only few parameters related to the algorithm users
want to train.

All convenience methods can be found in the `careamics.config` modules. CAREamics 
currently supports [Noise2Void]() and its variants, [CARE]() and [Noise2Noise](). 

``` python title="Import convenience functions"
from careamics.config import (
    create_n2v_configuration, # Noise2Void, N2V2, structN2V
    create_care_configuration, # CARE
    create_n2n_configuration, # Noise2Noise
)
```

Each method does all the heavy lifting to make the configuration coherent. They share
a certain numbers of mandatory parameters:

- `experiment_name`: The name of the experiment, used to differentiate trained models.
- `data_type`: One of the types supported by CAREamics (`array`, `tiff` or [`custom`]()).
- `axes`: Axes of the data (e.g. SYX), can only the following letters: `STCZYX`.
- `patch_size`: Size of the patches along the spatial dimensions (e.g. [64, 64]).
- `batch_size`: Batch size to use during training (e.g. 8). This parameter affects the
    memory footprint on the GPU.
- `num_epochs`: Number of epochs.


Additional optional parameters can be passed to tweak the configuration. 

## General optional parameters

### Training with channels

When training with multiple channels, the `axes` parameter should contain `C` (e.g. `YXC`).
An error will be then thrown if the optional parameter `n_channels` is not specified! 
Likewise if `n_channels` is specified but `C` is not in `axes`.

The correct way is to specify them both at the same time.

```python title="Configuration with multiple channels"
config = create_n2n_configuration(
    experiment_name='n2n_2D', 
    data_type="tiff", 
    axes="YXC", # (1)!
    patch_size=[64, 64],
    batch_size=8, 
    num_epochs=20,
    n_channels=3 # (2)!
)
```

1. The axes contain the letter `C`.
2. The number of channels is specified.


### Using augmentations

By default CAREamics configuration uses augmentations that are specific to the algorithm
(e.g. Noise2Void) and that are compatible with microscopy images (e.g. flip and 90 degrees
rotations).

However in certain cases, users might want to disable augmentations. For instance if you
have structures that are always oriented in the same direction. To do so there is a single
`use_agumentations` parameter:

```python title="Configuration without augmentations"
config = create_care_configuration(
    experiment_name='care_2D', 
    data_type="tiff", 
    axes="YX",
    patch_size=[64, 64],
    batch_size=8, 
    num_epochs=20,
    use_augmentations=False # (1)!
)
```

1. Augmentations are disabled (but normalization is still there!).


### Choosing a logger

By default, CAREamics simply log the training progress in the console. However, it is 
possible to use either [WandB](https://wandb.ai/site) or [TensorBoard](https://pytorch.org/tutorials/recipes/recipes/tensorboard_with_pytorch.html).

!!! note "Loggers installation"

    Using WandB or TensorBoard require the installation of `extra` dependencies. Check
    out the [installation section](/../../installation/#extra-dependencies) to know more about it.


```python title="Configuration with WandB"
config = create_n2n_configuration(
    experiment_name='n2n_2D', 
    data_type="tiff", 
    axes="YXC",
    patch_size=[64, 64],
    batch_size=8, 
    num_epochs=20,
    logger="wandb" # (1)!
)
```

1. `wandb` or `tensorboard`

### (Advanced) Passing model specific parameters

By default, the convenience functions use the default [UNet model parameters](). But if 
you are feeling brave, you can pass model specific parameters in the `model_kwargs` dictionary. 

```python title="Configuration with model specific parameters"
config = create_care_configuration(
    experiment_name='care_3D', 
    data_type="tiff", 
    axes="ZYX",
    patch_size=[16, 64, 64],
    batch_size=8, 
    num_epochs=20,
    model_kwargs={
        "depth": 3, # (1)!
        "num_channels_init": 64, # (2)!
        # (3)!
    }
)
```

1. The depth of the UNet.
2. The number of channels in the first layer.
3. Add any other parameter specific to the model!

!!! note "Model parameters overwriting"

    Some values of the model parameters are not compatible with certain algorithms. 
    Therefore, these are overwritten by the convenience functions. For instance,
    if you pass `in_channels` in the `model_kwargs` dictionary, it will be ignored and
    replaced by the `n_channels` parameter of the convenience function.



## CARE and Noise2Noise specific parameters

As opposed to Noise2Void, [CARE]() and [Noise2Noise]() can be trained with different loss
functions. This can be set using the `loss` parameter (surprise, surprise!).

```python title="Configuration with different loss"
config = create_care_configuration(
    experiment_name='care_3D', 
    data_type="tiff", 
    axes="ZYX",
    patch_size=[16, 64, 64],
    batch_size=8, 
    num_epochs=20,
    loss="mae" # (1)!
)
```

1. `mae` or `mse`

## Noise2Void specific parameters

[Noise2Void]() has a few additional parameters that can be set, including for using its 
variants [N2V2]() and [structN2V]().

!!! note "Understanding Noise2Void and its variants"

    Before deciding which variant to use, and how to modify the parameters, we recommend
    to die a little a bit on [how each algorithm works](/../../algorithms)!



### Noise2Void parameters

There are two Noise2Void parameters that influence how the patches are manipulated during
training:

- `roi_size`: This parameter specifies the size of the area used to replace the masked pixel value.
- `masked_pixel_percentage`: This parameter specifies how many pixels per patch will be manipulated.

While the default values are usually fine, they can be tweaked to improve the training
in certain cases.

```python title="Configuration with N2V parameters"
config = create_n2v_configuration(
    experiment_name='n2v_2D', 
    data_type="tiff", 
    axes="YX",
    patch_size=[64, 64],
    batch_size=8, 
    num_epochs=20,
    roi_size=7,
    masked_pixel_percentage=0.5
)
```

### N2V2

To use N2V2, the `use_n2v2` parameter should simply be set to `True`.

```python title="Configuration with N2V2"
config = create_n2v_configuration(
    experiment_name='n2v2_3D', 
    data_type="tiff", 
    axes="ZYX",
    patch_size=[16, 64, 64],
    batch_size=8, 
    num_epochs=20,
    use_n2v2=True # (1)!
)
```

1. What it does is modifying the architecture of the UNet model and the way the masked
    pixels are replaced.


### structN2V

StructN2V has two parameters that can be set:

 - `struct_n2v_axis`: The axis along which the structN2V mask will be applied. By default it
    is set to `none` (structN2V is disabled), you can set it to either `horizontal` or `vertical`.
 - `struct_n2v_span`: The size of the structN2V mask.

```python title="Configuration with structN2V"
config = create_n2v_configuration(
    experiment_name='structn2v_3D', 
    data_type="tiff", 
    axes="ZYX",
    patch_size=[16, 64, 64],
    batch_size=8, 
    num_epochs=20,
    struct_n2v_axis="horizontal",
    struct_n2v_span=5
)
```
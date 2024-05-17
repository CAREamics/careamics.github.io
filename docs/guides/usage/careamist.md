# CAREamist

The `CAREamist` is the central class in CAREamics, it provides the API to train, predict
and save models. There are three ways to create a `CAREamist` object: with a configuration, 
with a path to a configuration, or with a path to a trained model.


## Instantiating with a configuration

When passing a configuration to the `CAREamist` constructor, the model is initialized
with random weights and prediction will not be possible until the model is trained.


```python title="Instantiating CAREamist with a configuration"
from careamics import CAREamist
from careamics.config import create_n2v_configuration

config = create_n2v_configuration(
    experiment_name="n2v_2D",
    data_type="array",
    axes="YX",
    patch_size=[64, 64],
    batch_size=1,
    num_epochs=1,
) # (1)!

careamist = CAREamist(config)
```

1. Any valid configuration will do!


## Instantiating with a path to a configuration

This is similar to the previous section, except that the configuration is loaded from
a file on disk.

```python title="Instantiating CAREamist with a path to a configuration"
from careamics import CAREamist
from careamics.config import create_n2v_configuration, save_configuration

config = create_n2v_configuration(
    experiment_name="n2v_2D",
    data_type="array",
    axes="YX",
    patch_size=[64, 64],
    batch_size=1,
    num_epochs=1,
)

# save a configuration to disk
save_configuration(config, "configuration_example.yml")

# load it from within CAREamist
careamist = CAREamist("configuration_example.yml")
```

## Instantiating with a path to a model

There are two types of models exported from CAREamics. During training, the model is
saved as checkpoints (`.ckpt`). After training, users can export the model to the 
bioimage model zoo format (saved as a`.zip`). Both can be loaded into CAREamics to
either retrain or predict. Alternatively, a checkpoint can be loaded in order to 
export it as a bioimage model zoo model.

In any case, both types of pre-trained models can be loaded into CAREamics by passing
the path to the model file. The instantiated CAREamist is then ready to predict on new
images!


```python title="Instantiating CAREamist with a path to a model"
from careamics import CAREamist

path_to_model = "model.zip" # (1)!

careamist = CAREamist(path_to_model)
```

1. Any valid path to a model, as a string or a `Path.path` object, will work.

When loading a pre-trained model, the experiment name, used in the loggers (e.g. WandB),
or to name the checkpoints, is automatically set to `CAREamics`. But you can change that
by passing it to the `CAREamist` constructor.

```python title="Changing the experiment name"
careamist = CAREamist(path_to_model, experiment_name="a_new_experiment")
```


## Setting the working directory

By default, CAREamics will save the checkpoints in the current working directory. When
creating a new CAREamist, you can indicate a different working directory in which to
save the logs and checkpoints during training.

```python title="Changing the working directory"
careamist = CAREamist(config, work_dir="work_dir")
```

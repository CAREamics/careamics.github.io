# Build the configuration

!!! info "Beginner vs Advanced"

    This is an advanced level way to create CAREamics configuration. Do check the
    [convenience functions](convenience_functions.md) if you are looking for a simpler
    way to create CAREanics configurations!


CAREamics configuration is validated using [Pydantic](https://docs.pydantic.dev/latest/), 
a library that allows you to define schemas and automatically check the types of the 
input data you provide. 

In addition, it allows great flexibility in writing custom validators. In turns this
ensures that the configuration is always valid and coherent, protecting against errors
deep in the library.

As shown in the introduction, a CAREamics configuration is composed of four main elements:

1. Experiment name, a simple string
2. Algorithm configuration, also a Pydantic model
3. Data configuration, also a Pydantic model
4. Training configuration, also a Pydantic model

Each of the parameters and models are validated independently, and the configuration as a whole is validated at the end.

There are two ways to build Pydantic models: by passing a dictionary that reproduces the
model structure, or by calling all Pydantic models explicitly. While the second method is 
more concise, the first approach is less error prone and allow you to explore all
parameters available easily if you are using an IDE (e.g. VSCode, JupyterLab etc.).

Each algorithm has a specific configuration that may or may not be similar to the others.
For differences between algorithms, refer to the [algorithm requirements](algorithm_requirements.md) section.


!!! information "Complete list of parameters"
    A complete list of all parameters would be very long and difficult to showcase, as
    it also depends on the algorithm.

    The preferred way to check the parameters of the various configurations and subconfigurations is to read directly the [code reference](../../../reference/careamics/config) or the [source code](https://github.com/CAREamics/careamics/tree/main/src/careamics/config).


## Using Pydantic models

The preferred way to build the configuration is to call the Pydantic models directly. This
allows you to explore the parameters via your IDE, but also to get the validation errors
closer to the source of the error.

```python title="Building the configuration using Pydantic models"
--8<-- "careamics-examples/guides/careamist_api/configuration/build_configuration.py:pydantic"
```

1. The Pydantic models are imported from the `careamics.config` 
    submodules, and its various submodules.
2. Because the `architecture` parameter is used to discriminate between different models
    within CAREamics, there is no default value and it is therefore necessary to set it.
3. You can change here the model parameters.
4. There are more parameters available, but keep in mind that by creating the models
    directly, you are responsible for setting the correct parameters and you might get
    errors when assembling the final configuration. For instance, Noise2Void requires
    the same number of input and output channels, which is not checked here.
5. Noise2Void requires a specific algorithm configuration.
6. Other parameters are related to the optimizer and learning rate scheduler.
7. As opposed to CARE and Noise2Noise, Noise2Void requires a specific data configuration.
8. You can decide on the augmentations and their parameters.
9. Noise2Void requires the last augmentation to be `N2VManipulate`.
10. The dataloader parameters are the general parameters that can be passed to PyTorch's
    `DataLoader` class (see [documentation](https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader)).
11. The early stopping callback has many parameters, which are those available in the  
    PyTorch Lightning callback (see [documentation](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.EarlyStopping.html#lightning.pytorch.callbacks.EarlyStopping)).
12. Similarly, the `CheckpointModel` parameters are those of the corresponding PyTorch
    Lightning callback (see [documentation](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelCheckpoint.html)).
13. The training configuration is general and has many parameters, checkout the code
    reference or the code base for more information.
14. Finally the Noise2Void configuration can be instantiated.
15. Alternatively, CAREamics uses internally a factory to select and instantiate the 
    correct configuration based on the various parameters.

## Using nested dictionaries

An alternative to working with Pydantic models is to assemble the configuration using
a dictionary. While this is neat, because you are dealing with nested dictionaries, it is easy to add the parameters at the wrong level and you need to constantly refer to the [code documentation](../../reference) to know which parameters are available. Finally, because you are validating the configuration at once, you will get all the validation
errors in one go.

Here, we reproduce the same configuration as previously, but as a dictionary this time:

```python title="Building the configuration with a dictionary"
--8<-- "careamics-examples/guides/careamist_api/configuration/build_configuration.py:as_dict"
```

1. In order to correctly instantiate the N2V configuration via a dictionary, we have
    to explicitely specify certain paramaters that otherwise have a default value when
    using Pydantic. This is the case for the `algorithm` parameter.
2. As previously, we also specify the architecture.
3. Since many parameters have default values, we don't need to specify them but still
    need to pass an empty dictionary to make sure that there is an early stopping
    callback.
4. Here we are using the Pydantic class with the unpacked dictionary.
5. An alternative is to use the configuration factory, this function is used internally
    to select the correct algorithm based on the parameters.
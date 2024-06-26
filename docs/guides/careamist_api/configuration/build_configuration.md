# Build the configuration

!!! info "Beginner vs Intermediate"

    This is an intermediate level way to create CAREamics configuration. Do check the
    [convenience functions](convenience_functions.md) if you are looking for a simpler
    way to create CAREanics configurations!


CAREamics configuration is validated using [Pydantic](https://docs.pydantic.dev/latest/), 
a library that allows you to define schemas and automatically check the types of the 
input data you provide. 

In addition, it allows great flexibility in writing custom validators. In turns this
ensures that the configuration is always valid and coherent, protecting against errors
deep in the library.

As shown in the introduction, CAREamics configuration is composed of four main elements:

1. Experiment name, a simple string
2. Algorithm configuration, also a Pydantic model
3. Data configuration, also a Pydantic model
4. Training configuration, also a Pydantic model

Each of the parameters and models are validated independently, and the configuration as a whole is
validated at the end.

There are two ways to build Pydantic models: by passing a dictionary that reproduces the
model structure, or by calling all Pydantic models explicitly. While the first method is 
more concise, the second method is less error prone and allow you to explore all
parameters available easily if you are using an IDE (e.g. VSCode, JupyterLab etc.).

## Using nested dictionaries

In the introduction, we have seen a minimum example on how to build the configuration
with a dictionary, reproduced here:


```python title="Building the configuration with a dictionary"
--8<-- "careamics-examples/guides/careamist_api/configuration/build_configuration.py:as_dict"
```

1. The first parameter is just a string!
2. But this one is itself a Pydantic model, so we need to pass a dictionary that
    respects the structure of the model.
3. Don't be surprised, the deep neural network model is also a Pydantic model.
4. Same here, and so on...
5. The configuration is instantiated by passing keywords arguments rather than a dictionary, 
    and Pydantic knows how to interpret the sub-dictionaries to correctly instantiate the member 
    models.

While this is neat, because you are dealing with nested dictionaries, it is easy to add
the parameters at the wrong level and you need to constantly refer to the [code documentation](../../reference)
to know which parameters are available.

Finally, because you are validating the configuration at once, you will get all the validation
errors in one go.


## Using Pydantic models (preferred)

The preferred way to build the configuration is to call the Pydantic models directly. This
allows you to explore the parameters via your IDE, but also to get the validation errors
closer to the source of the error.

```python title="Building the configuration using Pydantic models"
--8<-- "careamics-examples/guides/careamist_api/configuration/build_configuration.py:pydantic"
```

1. The main Pydantic models are imported from the `careamics` and `careamics.config` 
    submodules, the others are organized in different submodules.
2. A Pydantic model is instantiated like any other class.
3. In CAREamics, we store constant values in `enum` classes in the `careamics.config.support` 
    submodule. This allows to have a single source of truth for the values. But you have
    to remember to use the `.value` attribute to get the string value.
4. You can instantiate the nested models directly in the parent model or outside (outside
    is better to track down the errors!).
5. The `transforms` parameter is a list, you can mix and match the different transformations,
    but also use dictionaries or the Pydantic model classes directly. Make sure to pass
    the `name` as it is used to identify the correct Pydantic model to instantiate for the
    transformation.
6. Here for instance, we use the Pydantic model directly.
7. The `dataloader_params` is a dictionary, you can pass any parameter that is accepted by
    the `torch.utils.data.DataLoader` class.
8. Finally, the configuration is instantiated by passing the Pydantic models directly.


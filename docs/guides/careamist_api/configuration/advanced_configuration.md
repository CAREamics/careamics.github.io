# Advanced configuration

We have implemented several mechanism to allow users to use CAREamics in contexts we 
do not explicitly support. In this section, we describe several of these mechanisms.

In the future, we hope to add more depending on user requests.

## Custom data type

The `data_type` parameter of the `DataConfig` class is a string that is used to choose
the data loader within CAREamics. We currently only support `array` and `tiff` explicitly.

However, users can set the `data_type` to `custom` and use their own read function.

```python title="Custom data type"
--8<-- "careamics-examples/guides/configuration/advanced_configuration.py:data"
```

1. As far as the configuration is concerned, you only set the `data_type` to `custom`. The
    rest happens in the `CAREamist` instance.

!!! info "Full example in other sections"

    A full example of the use of a custom data type is available in the [CAREamist]()
     and [Applications]() sections.


## Custom AI model

CAREamics currently only support UNet models, but users can create their own model
and use it in CAREamics. First, the model needs to be registered with the 
`register_model` decorator, then both the `algorithm` of `AlgorithmConfig` and the 
`architecture` of the `model` need to be set to custom.

```python title="Custom AI model"
--8<-- "careamics-examples/guides/configuration/advanced_configuration.py:model"
```

1. Register your model using the decorator and indicates its `name`.
2. Set the `algorithm` to `custom`.
3. In the `model`, set the `architecture` to `Custom`. Watch the capital letter!
4. Indicate the name of the model.

!!! info "Full example in other sections"

    A full example of the use of a custom data type is available in the 
    [Applications]() sections.

# Full specification

The full specification of the configuration is a detailed description of all the parameters 
that can be used to configure CAREamics. It is useful for advanced users who want to 
have full control over the training process.

You can also explore all the Pydantic models using the [reference documentation](../../reference/careamics).

```python title="Full specification"
--8<-- "careamics-examples/guides/configuration/full_spec.py:specs"
```

1. Currently, we only support the UNet architecture and custom models (see [advanced
    configuration](advanced_configuration.md#custom-ai-model)). But in the future, there will be more
    models to use here.
2. Here the parameters are those from Pytorch DataLoaders.
3. Normalization is also a transformation, but it is always applied before these 
    augmentations.
4. The `EarlyStoppingModel` has a lot of parameters not reproduced here.


However, not all algorithms are compatible with all parameters. The configuration does
some heavy lifting to correct the obvious incompatibilities, but some are left to the user.
In the next section, we will see the constraints on each algorithm.
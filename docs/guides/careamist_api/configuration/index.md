---
description: Configuration guide
---


The configuration summarizes all the parameters used internally by CAREamics. It is 
used to create a `CAREamist` instance and is saved together with the checkpoints and 
saved models.

It is composed of four members:

```python title="Anatomy of the configuration"
--8<-- "careamics-examples/guides/careamist_api/configuration/build_configuration.py:as_dict"
```

1. The name of the experiment, used to differentiate trained models.
2. Configuration specific to the model.
3. Configuration related to the data.
4. Training parameters.
5. The configuration is an object! :bomb:

If the number of parameters looks too limited, it is because the configuration is
hiding a lot of default values! But don't be afraid, we have designed convenience
functions to help you create a configuration for each of the algorithm CAREamics
offers.

In the next sections, you can dive deeper on how to use CAREamics 
configuration with different levels of expertise.

- (beginner) [Convenience functions](convenience_functions.md)
- (beginner) [Save and load configurations](save_load.md)
- (intermediate) [Build the configuration from scratch](build_configuration.md)
- (intermediate) [Full specification](full_spec.md)
- (intermediate) [Algorithm requirements](algorithm_requirements.md)
- (advanced) [Advanced configuration](advanced_configuration.md)
- (all) [Understanding the errors](understanding_errors.md)

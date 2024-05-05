---
description: Configuration guide
---


The configuration summarizes all the parameters used internally by CAREamics. It is 
used to create a `CAREamist` instance and is saved together with the checkpoints and 
saved models.

It is composed of four members:

```python title="Anatomy of the configuration"
from careamics import Configuration

config_as_dict = {
    "experiment_name": "my_experiment", # (1)!
    "algorithm_config": { # (2)!
        "algorithm": "n2v",
        "loss": "n2v",
        "model": {
            "architecture": "UNet",
        }
    },
    "data_config": { # (3)!
        "data_type": "array",
        "patch_size": [128, 128],
        "axes": "YX",
    },
    "training_config": { # (4)!
        "num_epochs": 1,
    }
}
config = Configuration(**config_as_dict) # (5)!
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

- Beginner: use convenience functions
- Intermediate: build the configuration with Pydantic
- Advanced: custom model
- Full specification
- Understanding the errors

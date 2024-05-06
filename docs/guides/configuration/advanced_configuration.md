# Advanced configuration

We have implemented several mechanism to allow users to use CAREamics in contexts we 
do not explicitely support. In this section, we describe several of these mechanisms.

In the future, we hope to add more depending on user requests.

## Custom data type

The `data_type` parameter of the `DataConfig` class is a string that is used to choose
the data loader within CAREamics. We currently only support `array` and `tiff` explicitely.

However, users can set the `data_type` to `custom` and use their own read function.

```python title="Custom data type"
from careamics.config import DataConfig

data_config = DataConfig(
    data_type="custom", # (1)!
    axes="YX",
    patch_size=[128, 128],
    batch_size=8,
    num_epochs=20,
)
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
from torch import nn, ones
from careamics.config import AlgorithmConfig, register_model

@register_model(name="linear_model")  # (1)!
class LinearModel(nn.Module):
    def __init__(self, in_features, out_features, *args, **kwargs):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = nn.Parameter(ones(in_features, out_features))
        self.bias = nn.Parameter(ones(out_features))
    
    def forward(self, input):
        return (input @ self.weight) + self.bias
    
config = AlgorithmConfig(
    algorithm="custom",  # (2)!
    loss="mse",
    model={
        "architecture": "Custom", # (3)!
        "name": "linear_model", # (4)!
        "in_features": 10,
        "out_features": 5,
    },
)
```

1. Register your model using the decorator and indicates its `name`.
2. Set the `algorithm` to `custom`.
3. In the `model`, set the `architecture` to `Custom`. Watch the capital letter!
4. Indicate the name of the model.

!!! info "Full example in other sections"

    A full example of the use of a custom data type is available in the [CAREamist]()
     and [Applications]() sections.

# Lightning API

The so-called "Lightning API" is how we refer to using the lightning modules 
from CAREamics in a [PyTorch Ligthning](https://lightning.ai/docs/pytorch/stable/) 
pipeline. In our [high-level API](../careamist_api/index.md), these modules are 
hidden from users and many checks, validations, error handling, and other 
features are provided. However, if you want to have increased flexibility, for instance
to use your own dataset, model or a different training loop, you can re-use many of 
CAREamics modules in your own PyTorch Lightning pipeline.


```python "Basic Usage"
--8<-- "examples/lightning_api/basic_usage.py"
```




- Lightning Module
- Data Module
- Trainer, callbacks
- Prediction
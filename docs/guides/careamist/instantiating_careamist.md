# Instantiating CAREamist

There are three ways to create a `CAREamist` object: with a configuration, with a path
to a configuration, or with a path to a model.


## Instantiating with a configuration


```python title="Instantiating CAREamist with a configuration"
from careamics import CAREamist
from careamics.config.configuration_example import full_configuration_example

config = full_configuration_example() # (1)!

careamist = CAREamist(config)
```

1. Any valid configuration will do!



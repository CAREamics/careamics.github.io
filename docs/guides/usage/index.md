# Using CAREamics

In this section, we will explore the many facets of the `CAREamist` class, which
allors training and predicting using the various algorithms in CAREamics.

The workflow in CAREamics has five steps: creating a configuration, instantiating a
`CAREamist` object, training, prediction, and model export.


```python title="Basic CAREamics usage"
import numpy as np
from careamics import CAREamist
from careamics.config import create_n2v_configuration

# create a configuration
config = create_n2v_configuration(
    experiment_name="n2v_2D",
    data_type="array",
    axes="YX",
    patch_size=[64, 64],
    batch_size=1,
    num_epochs=1, # (1)!
)

# instantiate a careamist
careamist = CAREamist(config)

# train the model
train_data = np.random.randint(0, 255, (256, 256)) # (2)!
careamist.train(train_source=train_data)

# once trained, predict
pred_data = np.random.randint(0, 255, (128, 128))
predction = careamist.predict(source=pred_data)

# export to BMZ format
careamist.export_to_bmz(
    path="my_model.bmz", name="N2V 2D", authors=[{"name": "CAREamics authors"}]
)
```

1. Obviously, one should choose a more reasonable number of epochs for training.

2. One should use real data for training!


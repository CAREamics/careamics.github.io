---
icon: octicons/repo-24
description: Guides
---

# Guides

The basic usage of CAREamics follows this pattern:

```python title="CAREamics workflow"
"""Example showcasing the basic usage of CAREamics."""
import numpy as np
from careamics import CAREamist
from careamics.config import create_n2v_configuration

# create a configuration
config = create_n2v_configuration( # (1)!
    experiment_name="n2v_2D",
    data_type="array",
    axes="YX",
    patch_size=[64, 64],
    batch_size=1,
    num_epochs=1, # (2)!
)

# instantiate a careamist
careamist = CAREamist(config) # (3)!

# train the model
train_data = np.random.randint(0, 255, (256, 256)) # (4)!
careamist.train(train_source=train_data)

# once trained, predict
pred_data = np.random.randint(0, 255, (128, 128))
predction = careamist.predict(source=pred_data)

# export to BMZ format
careamist.export_to_bmz( # (5)!
    path="my_model.bmz", name="N2V 2D", authors=[{"name": "CAREamics authors"}]
)
```

1. There are several convenience functions to create a configuration, but you can also
create it entirely manually. Head to the configuration section to know more!

2. Obviously, one should choose a more reasonable number of epochs for training.

3. The CAREamist allows training, predicting and exporting the model. Refer to the 
CAREamist section to learn more about it. There is also an alternative for more advance
users, which we call the Lightning API.

4. One should use real data for training!

5. Models can be exported to the [BioImage Model Zoo](https://bioimage.io/) format.


!!! warning "Work in progress"
    These pages are still under construction.
    

<div class="md-container secondary-section">
    <div class="g">
        <div class="section">
            <div class="component-wrapper" style="display: block;">
                <!-- New row -->
                <div class="responsive-grid">
                    <!-- Installation -->
                    <a class="card-wrapper" href="configuration">
                        <div class="card"> 
                            <div class="logo">
                                <span class="twemoji">
                                    --8<--  "desktop-download.svg"
                                </span>
                            </div>
                            <div class="card-content">
                                <h5>Configuration</h5>
                                <p>
                                    The configuration is at the heart of CAREamics, it 
                                    allow users to define how and which algorithm will be
                                    trained.
                                </p>
                            </div>
                        </div>
                    </a>
                    <!-- Installation -->
                    <a class="card-wrapper" href="usage">
                        <div class="card"> 
                            <div class="logo">
                                <span class="twemoji">
                                    --8<--  "desktop-download.svg"
                                </span>
                            </div>
                            <div class="card-content">
                                <h5>Using CAREAmics</h5>
                                <p>
                                    The CAREamist is the core element allowing training
                                    and prediction using the model defined in the configuration.
                                </p>
                            </div>
                        </div>
                    </a>
                </div>
                  <!-- New row -->
                <div class="responsive-grid">
                    <!-- Installation -->
                    <a class="card-wrapper" href="lightning_api">
                        <div class="card"> 
                            <div class="logo">
                                <span class="twemoji">
                                    --8<--  "desktop-download.svg"
                                </span>
                            </div>
                            <div class="card-content">
                                <h5>Lightning API</h5>
                                <p>
                                    Advanced users can re-use part of CAREamics in their
                                    Lightning pipeline, with more customization potential
                                    available.
                                </p>
                            </div>
                        </div>
                    </a>
                    <!-- Installation -->
                    <a class="card-wrapper" href="dev_resources">
                        <div class="card"> 
                            <div class="logo">
                                <span class="twemoji">
                                    --8<--  "desktop-download.svg"
                                </span>
                            </div>
                            <div class="card-content">
                                <h5>Developer resources</h5>
                                <p>
                                    More insights on how CAREamics is organized and how
                                    to tweak it to your needs.
                                </p>
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
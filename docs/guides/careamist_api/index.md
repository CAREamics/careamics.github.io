---
description: CAREamist API main page.
---

# CAREamist API

The CAREamist API is the recommended way to use CAREamics, it is a two stage process, in
which users first define a configuration and then use a the `CAREamist` to run their 
training and prediction. The [applications](../../applications/index.md) section provides
examples.

```python title="Basic CAREamics usage"
--8<-- "careamics-examples/guides/careamist_api/careamist_api.py:careamist_api"
```

1. Obviously, one should choose a more realistic number of epochs for training.

2. One should use real data for training!



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
                                    --8<--  "tasklist.svg"
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
                                    --8<--  "code.svg"
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
            </div>
        </div>
    </div>
</div>
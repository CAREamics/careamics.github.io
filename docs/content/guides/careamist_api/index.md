---
icon: octicons/code-24
description: CAREamist API main page.
---

# CAREamist API

The CAREamist API is the recommended way to use CAREamics, it is a two stage process, in
which users first define a configuration and then use a the `CAREamist` to run their 
training and prediction.

## Quick start

The simplest way to use CAREamics is to create a configuration using the [convenience functions](configuration/convenience_functions.md). Checkout the [applications](../../applications/index.md) section for real-world examples of the various algorithms.

=== "Noise2Void"
    
    ```python
    --8<-- "careamist_api.py:quick_start_n2v"
    ```

    1. Obviously, choose a more realistic number of epochs for training.

    2. Use real data for training!


=== "CARE"

    ```python
    --8<-- "careamist_api.py:quick_start_care"
    ```

    1. Obviously, choose a more realistic number of epochs for training.

    2. Use real data for training! Here, we added validation data as well.


=== "Noise2Noise"

    ```python
    --8<-- "careamist_api.py:quick_start_n2n"
    ```

    1. Obviously, choose a more realistic number of epochs for training.

    2. Use real data for training!


## Documentation

There are many features that can be useful for your application, explore the
documentation to learn all the various aspects of CAREamics.



<div class="grid cards" markdown>

-   :octicons-tasklist-24:{ .lg .middle } __Configuration__

    ---

    The configuration is at the heart of CAREamics, it allows users to define how and
    which algorithm will be trained.

    [:octicons-arrow-right-24: Configuration](./content/guides/careamist_api/configuration/)

-   :octicons-code-24:{ .lg .middle } __Usage__

    ---

    The CAREamist is the core element allowing training and prediction using the model
    defined in the configuration.

    [:octicons-arrow-right-24: Usage](./content/guides/careamist_api/usage/)

</div>

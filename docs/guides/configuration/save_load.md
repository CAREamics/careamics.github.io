# Save and load

CAREamics configurations can be saved to the disk as `.yml` file and loaded easily to
start similar experiments.

## Save a configuration

```python title="Save a configuration"
from careamics import save_configuration
from careamics.config import create_n2v_configuration

config =  create_n2v_configuration(
    experiment_name="Config_to_save",
    data_type="tiff",
    axes="ZYX",
    patch_size=(8, 64, 64),
    batch_size=8,
    num_epochs=20
)
save_configuration(config, "config.yml")
```

In the resulting file, you can see all the parameters that are defaults and hidden
from you.

??? Example "resulting config.yml file"

    ```yaml
    version: 0.1.0
    experiment_name: Config_to_save
    algorithm_config:
    algorithm: n2v
    loss: n2v
    model:
        architecture: UNet
        conv_dims: 3
        num_classes: 1
        in_channels: 1
        depth: 2
        num_channels_init: 32
        final_activation: None
        n2v2: false
    optimizer:
        name: Adam
        parameters:
        lr: 0.0001
    lr_scheduler:
        name: ReduceLROnPlateau
        parameters: {}
    data_config:
    data_type: tiff
    patch_size:
    - 8
    - 64
    - 64
    batch_size: 8
    axes: ZYX
    transforms:
    - name: Normalize
        mean: 0.485
        std: 0.229
    - name: NDFlip
        p: 0.5
        is_3D: true
        flip_z: true
    - name: XYRandomRotate90
        p: 0.5
        is_3D: true
    - name: N2VManipulate
        roi_size: 11
        masked_pixel_percentage: 0.2
        strategy: uniform
        struct_mask_axis: none
        struct_mask_span: 5
    training_config:
    num_epochs: 20
    checkpoint_callback:
        monitor: val_loss
        verbose: false
        save_weights_only: false
        mode: min
        auto_insert_metric_name: false
        save_last: true
        save_top_k: 3
    ```

## Load a configuration

```python title="Load a configuration"
from careamics import load_configuration

config = load_configuration("config.yml")
```

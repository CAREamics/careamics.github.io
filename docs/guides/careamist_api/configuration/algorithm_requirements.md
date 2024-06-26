# Algorithm requirements

In this section we detail the constraints of each algorithm on the configuration.

### Noise2Void family

This is valid for `Noise2Void`, `N2V2` and `structN2V`.

#### Algorithm configuration

- `algorithm="n2v"`
- `loss="n2v"`
- `model`: 
    - must be a UNet (`architecture="UNet"`)
    - `in_channels` and `num_classes` must be equal


#### Data configuration

- `transforms`: must contain `N2VManipulateModel` as the last transform


### CARE

#### Algorithm configuration

- `algorithm="care"`
- `loss`: any but `n2v`

#### Data configuration

- `transforms`: must not contain `N2VManipulateModel`


### Noise2Noise

#### Algorithm configuration

- `algorithm="care"`
- `loss`: any but `n2v`

#### Data configuration

- `transforms`: must not contain `N2VManipulateModel`




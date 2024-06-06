# Full specification

The full specification of the configuration is a detailed description of all the parameters 
that can be used to configure CAREamics. It is useful for advanced users who want to 
have full control over the training process.

You can also explore all the Pydantic models using the [reference documentation](../../reference/careamics).

```python title="Full specification"
from careamics import Configuration
from careamics.config import (
    AlgorithmConfig,
    DataConfig,
    TrainingConfig,
)
from careamics.config.architectures import UNetModel
from careamics.config.callback_model import EarlyStoppingModel
from careamics.config.optimizer_models import LrSchedulerModel, OptimizerModel
from careamics.config.support import (
    SupportedActivation,
    SupportedAlgorithm,
    SupportedArchitecture,
    SupportedData,
    SupportedLogger,
    SupportedLoss,
    SupportedOptimizer,
    SupportedPixelManipulation,
    SupportedScheduler,
    SupportedStructAxis,
)
from careamics.config.transformations import (
    N2VManipulateModel,
    XYFlipModel,
    NormalizeModel,
    XYRandomRotate90Model,
)

experiment_name = "Full example"

# Algorithm
model = UNetModel( # (1)!
    architecture=SupportedArchitecture.UNET.value,
    in_channels=1,
    num_classes=1,
    depth=2,
    num_channels_init=32,
    final_activation=SupportedActivation.NONE.value,
    n2v2=False,
)

optimizer = OptimizerModel(
    name=SupportedOptimizer.ADAM.value, parameters={"lr": 0.0001}
)

scheduler = LrSchedulerModel(
    name=SupportedScheduler.REDUCE_LR_ON_PLATEAU.value,
)

algorithm_model = AlgorithmConfig(
    algorithm=SupportedAlgorithm.N2V.value,
    loss=SupportedLoss.N2V.value,
    model=model,
    optimizer=optimizer,
    lr_scheduler=scheduler,
)

# Data
norm = NormalizeModel()
xyflip = XYFlipModel()
rotate = XYRandomRotate90Model()
n2vmanipulate = N2VManipulateModel(
    roi_size=11,
    masked_pixel_percentage=0.2,
    strategy=SupportedPixelManipulation.MEDIAN.value,
    struct_mask_axis=SupportedStructAxis.NONE.value,
    struct_mask_span=7,
)

data_model = DataConfig(
    data_type=SupportedData.ARRAY.value,
    patch_size=(256, 256),
    batch_size=8,
    axes="YX",
    transforms=[norm, xyflip, rotate, n2vmanipulate],
    dataloader_params={
        "num_workers": 4,
        # (2)!
    },
    # (3)!
)

# Traning
earlystopping = EarlyStoppingModel(
    # (4)!
)

training_model = TrainingConfig(
    num_epochs=30,
    logger=SupportedLogger.WANDB.value,
    early_stopping_callback=earlystopping,
)

config = Configuration(
    experiment_name=experiment_name,
    algorithm_config=algorithm_model,
    data_config=data_model,
    training_config=training_model,
)
```

1. Currently, we only support the UNet architecture and custom models (see [advanced
    configuration](advanced_configuration)). But in the future, there will be more
    models to use here.
2. Here the parameters are those from Pytorch DataLoaders.
3. There are also the `mean` and `std` parameters, used to normalize the data. But they are typically
    calculated from the data itself, and then later stored in the configuration.
4. The `EarlyStoppingModel` has a lot of parameters not reproduced here.


However, not all algorithms are compatible with all parameters. The configuration does
some heavy lifting to correct the obvious incompatibilities, but some are left to the user.
In the next section, we will see the constraints on each algorithm.
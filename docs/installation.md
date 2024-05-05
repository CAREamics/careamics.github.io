---
icon: octicons/desktop-download-24
description: Installation instructions
---

# Installation

CAREamics is a deep-learning library and we therefore recommend having GPU support as
training the algorithms on the CPU can be very slow. MacOS users can also benefit from
GPU-acceleration if they have the new chip generations (M1, M2, etc.).

Support is provided directly from PyTorch, and is still experimental for macOS.

## Step-by-step

We recommend using [mamba (miniforge)](https://github.com/conda-forge/miniforge#download) 
to install all packages in a virtual environment. As an alternative, you can use
[conda 
(miniconda)](https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html). 


=== "Linux and Windows"
    1. Open the terminal and type `mamba` to verify that mamba is available.
    2. Create a new environment:
        
        ``` bash
        mamba create -n careamics python=3.10
        mamba activate careamics
        ```

    3. Install PyTorch following the [official 
        instructions](https://pytorch.org/get-started/locally/)

        As an example, our test machine requires:

        ``` bash
        mamba install pytorch torchvision pytorch-cuda=11.8 -c pytorch -c nvidia
        ```
    
    4. Verify that the GPU is available:
        
        ``` bash
        python -c "import torch; print([torch.cuda.get_device_properties(i) for i in range(torch.cuda.device_count())])"
        ```

        This should show a list of available GPUs. If the list is empty, then you
        will need to change the `pytorch` and `pytorch-cuda` versions to match your
        hardware (linux and windows).
    
    5. Install CAREamics. We have several extra options (`dev`, `examples`, `wandb`
        and `tensorboard`). If you wish to run the [example notebooks](https://github.com/CAREamics/careamics-examples),
        we recommend the following:

        ``` bash
        pip install --pre "careamics[examples]"
        ```

    These instructions were tested on a linux virtual machine (RedHat 8.6) with a 
    NVIDIA A40-8Q GPU.

=== "macOS"
    1. Open the terminal and type `mamba` to verify that mamba is available.
    2. Create a new environment:
        
        ``` bash
        mamba create -n careamics python=3.10
        mamba activate careamics
        ```

    3. Install PyTorch following the [official 
        instructions](https://pytorch.org/get-started/locally/)

        As an example, our test machine requires:

        ``` bash
        mamba install pytorch::pytorch torchvision torchaudio -c pytorch
        ```

        :warning: Note that accelerated-training is only available on macOS silicon.
    
    4. Install CAREamics. We have several extra options (`dev`, `examples`, `wandb`
        and `tensorboard`). If you wish to run the [example notebooks](https://github.com/CAREamics/careamics-examples),
        we recommend the following:

        ``` bash
        pip install --pre "careamics[examples]"
        ```

### Extra dependencies

CAREamics extra dependencies can be installed by specifying them in brackets. In the previous
section we installed `careamics[examples]`. You can add other extra dependencies, for instance
`wandb` by doing:

``` bash
pip install --pre "careamics[examples, wandb]"
```

Here is a list of the extra dependencies:

- `examples`: Dependencies required to run the example notebooks.
- `wandb`: Dependencies to use [WandB](https://wandb.ai/site) as a logger.
- `tensorboard`: Dependencies to use [TensorBoard](https://pytorch.org/tutorials/recipes/recipes/tensorboard_with_pytorch.html) as a logger.
- `dev`: Dependencies required to run all the tooling necessary to develop with CAREamics.
        
## Quickstart

Once you have [installed CAREamics](installation.md), the easiest way to get started
is to look at the [applications](applications/index.md) for full examples and the 
[guides](guides/index.md) for in-depth tweaking.
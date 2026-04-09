---
icon: lucide/download
description: Installation instructions
---

# Installation

CAREamics is available as a PyPI and conda-forge package. We recommend using CAREamics with [uv](./install_with_uv), but we also provide
instructions for [mamba](./install_with_mamba).


!!!warning
    Having access to GPU is highly recommended for running any deep-learning, but note
    that PyTorch installation depends on the system and CUDA version.

    Therefore, should you encounter issues installing CAREamics, first make sure that
    you can install a compatible version of PyTorch with GPU support.

    - [PyTorch supported versions](https://github.com/CAREamics/careamics/blob/main/pyproject.toml):
    check `torch` in our `dependencies`.
    - [Installing PyTorch](https://pytorch.org/get-started/locally/)

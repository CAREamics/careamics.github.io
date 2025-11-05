---
description: uv
---

# Installing CAREamics with uv

Follow [uv installation guidelines](https://docs.astral.sh/uv/getting-started/installation/)
to use `uv`.


!!! important
    Please refer to the [installing PyTorch](https://docs.astral.sh/uv/guides/integration/pytorch/#installing-pytorch)
    section of `uv` documentation should you encounter issues running on GPU. In particular
    it may be necessary to install torch independently in the `venv` on Windows (see [this section](#installing-careamics-with-gpu-on-windows))


## Using notebooks

To run notebooks, install [juv](https://github.com/manzt/juv):

```bash title="Installing juv"
uv tool install juv
```

### Running CAREamics examples

[CAREamics-examples](https://github.com/CAREamics/careamics-examples/tree/main/applications) contains
multiple notebook examples that can be directly run with `uv`:


```python title="Run a notebook"
juv run notebook.ipynb
```


### Running your own notebook

To run your own notebook, we recommend adding [PEP723](https://peps.python.org/pep-0723/)
metadata:

```bash title="Add CAREamics dependency"
juv add my_notebook.ipynb "careamics[examples]"
juv run my_notebook.ipynb
```

You can also pin the CAREamics dependency in order to improve reproducibility:

```bash title="Pin CAREamics dependency"
juv add my_notebook.ipynb "careamics[examples]==0.0.16"
```


## CAREamics as a dependency

In this section, we will describe creating a project with CAREamics as a dependency,
using standard `uv`:

```bash
uv init careamics_project
cd careamics_project
uv add "careamics[examples]>=0.0.16"  # (1)!
```

1. Pin the dependency for reproducibility


## Installing CAREamics with GPU on Windows

This section walks you through creating a CAREamics-based projects using GPU on
Windows.

1. Create a `pyproject.toml` in your project folder:
    ``` title="pyproject.toml"
    [project]
    name = "myproject"
    version = "0.1.0"
    description = "Running CAREamics on Windows with GPU"
    readme = "README.md"
    requires-python = ">=3.11"
    dependencies = [
        "torch>=2.0,<=2.9.0", # (1)!
        "torchvision<=0.24.0",
        "careamics[examples]>=0.0.18",
    ]

    [tool.uv.sources]
    torch = [
        { index = "pytorch" },
    ]
    torchvision = [
        { index = "pytorch" },
    ]

    [[tool.uv.index]]
    name = "pytorch"
    url = "https://download.pytorch.org/whl/cu128" # (2)!
    explicit = true
    ```

    1. The constraints here will change with time, and are given as indications here.
    2. This will depend on your system (especially GPU driver), [check the PyTorch instructions](https://pytorch.org/get-started/locally/).

2. Test GPU accessibility by running the following script:
    ```
    uv run python -c "import torch; print([torch.cuda.get_device_properties(i) for i in range(torch.cuda.device_count())])"
    ```
3. Add your training script or notebook to the project and run it with `uv` (see previous sections).
 


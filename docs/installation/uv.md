---
description: uv
---

# Installing CAREamics with uv

Follow [uv installation guidelines](https://docs.astral.sh/uv/getting-started/installation/)
to use `uv`.


!!! important
    Please refer to the [installing PyTorch](https://docs.astral.sh/uv/guides/integration/pytorch/#installing-pytorch)
    section of `uv` documentation should you encounter issues running on GPU.


## Using notebooks

To run notebooks, install [juv](https://github.com/manzt/juv):

```bash title="Installing `juv`"
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
uv add "careamics[examples]>=0.0.16 # (1)
```

1. Pin the dependency for reproducibility




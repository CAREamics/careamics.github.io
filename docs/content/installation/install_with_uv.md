---
icon: lucide/sun
description: Install with uv
---

# Install with uv

[uv](https://docs.astral.sh/uv/getting-started/installation/) is a modern Python package
manager and virtual environment tool. We favor installing with `uv` thanks to its speed
and creation of lockfiles to ensure reproducible environments.

!!! warning
    Please refer to the [installing PyTorch](https://docs.astral.sh/uv/guides/integration/pytorch/#installing-pytorch)
    section of `uv` documentation should you encounter issues running on GPU. In particular
    it may be necessary to install torch independently in the `venv` on Windows (see [this section](#installing-careamics-with-gpu-on-windows))


### Using notebooks

1. Install [juv](https://github.com/manzt/juv) in `uv`:

    ```bash
    uv tool install juv
    ```

2. Add `CAREamics` to your notebook:

    ```bash
    juv add my_notebook.ipynb "careamics[examples]"
    ```

3. Run the notebook:

    ```bash
    juv run my_notebook.ipynb
    ```

!!! note
    You can start with one of our [example notebooks](https://github.com/CAREamics/careamics-examples/tree/main/applications). These already have the dependencies declared (`juv add`).

### Using a project

1. Start your project:

    ```bash
    uv init my_project
    cd my_project
    ```

2. Add `CAREamics` to your project:

    ```bash
    uv add "careamics[examples]"
    ```

!!! note
    You can start with one of our [example notebooks](https://github.com/CAREamics/careamics-examples/tree/main/applications) or the [getting started section]().

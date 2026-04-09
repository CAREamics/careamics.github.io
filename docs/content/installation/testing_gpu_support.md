---
icon: lucide/microchip
description: GPU support.
---

# Testing GPU support

To test if your system has GPU support (including MPS on Apple Silicon), you can call
specific Python commands, either directly in python or via the command linecommand line.


## Linux and Windows with CUDA


=== "Command line"
  
    ```bash
    python -c "import torch; print(torch.cuda.device_count() > 0)"
    ```

=== "Python" 

    ```python
    import torch
    
    print(torch.cuda.device_count() > 0)
    ```

!!! note "Running bash commands on Windows"

    If you are using Windows, try out [git for Windows](https://gitforwindows.org/) to
    run bash commands in a terminal.

## macOS with Apple Silicon (MPS)

=== "Command line"

    ```bash
    python -c "import torch; import platform; print((platform.processor() in ('arm', 'arm64') and torch.backends.mps.is_available()))"
    ```


=== "Python"

    ```python
    import torch
    import platform
    
    print((platform.processor() in ('arm', 'arm64') and torch.backends.mps.is_available()))
    ```
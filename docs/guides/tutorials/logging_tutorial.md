---
description: Using WandB and TensorBoard for experiment tracking
---

# Using WandB and TensorBoard

Training deep learning models for microscopy image restoration involves monitoring numerous metrics, hyperparameters, and model behaviors. CAREamics provides built-in support for two popular experiment tracking tools: [Weights & Biases (WandB)](https://wandb.ai/site) and [TensorBoard](https://pytorch.org/tutorials/recipes/recipes/tensorboard_with_pytorch.html). These tools enable you to visualize training progress, compare experiments, and maintain reproducible research workflows.

!!! note "Installation required"

    Both WandB and TensorBoard require additional dependencies. You can install them [as extras](https://careamics.github.io/0.1/installation/conda_mamba/#extra-dependencies):
    
    ```bash
    # For WandB
    pip install "careamics[wandb]"
    
    # For TensorBoard
    pip install "careamics[tensorboard]"
    ```

## Weights & Biases (WandB)

WandB offers cloud-based experiment tracking with collaborative features, making it ideal for teams and projects requiring centralized monitoring. It automatically logs metrics, hyperparameters, system information, and can store model artifacts.

### Basic usage

To enable WandB logging in your CAREamics workflow, simply specify `logger="wandb"` when creating your configuration:

```python title="Using WandB with Noise2Void"
from careamics import CAREamist
from careamics.config import create_n2v_configuration

# Create configuration with WandB logging
config = create_n2v_configuration(
    experiment_name="n2v_experiment",  # (1)!
    data_type="array",
    axes="YX",
    patch_size=(64, 64),
    batch_size=16,
    num_epochs=100,
    logger="wandb"  # (2)!
)

# Initialize and train
careamist = CAREamist(source=config)
careamist.train(train_source=train_data)
```
1. Name of the experiment run as it will appear in WandB
2. Enable WandB logging

### WandB authentication and configuration

On first use, WandB will prompt you to authenticate. You have several options:

```python
import wandb

# Option 1: Login interactively (will open browser)
wandb.login()

# Option 2: Login with API key
wandb.login(key="your_api_key_here")

# Option 3: Set environment variable (recommended for scripts)
import os
os.environ["WANDB_API_KEY"] = "your_api_key_here"
```

You can configure additional WandB settings through environment variables:

```python
import os

# Set project name
os.environ["WANDB_PROJECT"] = "microscopy-denoising"

# Set entity (team or username)
os.environ["WANDB_ENTITY"] = "your_username"

# Set specific run name
os.environ["WANDB_RUN_NAME"] = "n2v_experiment_001"

# Disable WandB (useful for debugging)
os.environ["WANDB_MODE"] = "disabled"
```
!!! tip "Finding your API key"
    
    Get your WandB API key from [https://wandb.ai/authorize](https://wandb.ai/authorize)

### What WandB logs

When using WandB with CAREamics, the following information is automatically tracked:

- **Training metrics**: Loss values for each epoch
- **Validation metrics**: Validation loss and PSNR when validation data is provided
- **Hyperparameters**: All configuration parameters (learning rate, batch size, model architecture, etc.)
- **Learning rate**: Learning rate schedule throughout training

## TensorBoard

TensorBoard provides local experiment tracking and visualization, making it excellent for individual workflows and offline environments. It's particularly useful when working on HPC systems with limited internet connectivity.

### Basic usage

Enable TensorBoard logging by specifying `logger="tensorboard"` in your configuration:

```python title="TensorBoard with Noise2Void"
from careamics import CAREamist
from careamics.config import create_n2v_configuration
from pathlib import Path

# Create configuration with TensorBoard logging
config = create_n2v_configuration(
    experiment_name="n2v_experiment",
    data_type="array",
    axes="YX",
    patch_size=(64, 64),
    batch_size=16,
    num_epochs=100,
    logger="tensorboard"  # (1)!
)

# Initialize with specific working directory
work_dir = Path("experiments/n2v_runs")
careamist = CAREamist(source=config, work_dir=work_dir)  
careamist.train(train_source=train_data)
```
1. Enable TensorBoard logging

### Viewing TensorBoard logs

After training, launch TensorBoard to visualize your results:

```bash
# Point to the logs directory
tensorboard --logdir experiments/n2v_runs/n2v_experiment/logs

# Or to view multiple experiments
tensorboard --logdir experiments/

# Specify custom port
tensorboard --logdir experiments/ --port 6007
```

Then open your browser to `http://localhost:6006` (or your specified port).

### What TensorBoard logs

TensorBoard captures:

- **Scalars**: Training and validation loss curves, PSNR metrics
- **Hyperparameters**: Complete configuration parameters
- **Learning rate**: Learning rate changes during training

!!! info "Log directory structure"

    CAREamics organizes TensorBoard logs as follows:
    ```
    work_dir/
    └── experiment_name/
        ├── logs/
        │   └── version_0/   # (1)!
        │       └── events.out.tfevents...
        └── checkpoints/
            ├── last.ckpt
            └── best.ckpt
    ```    
    1. Each training run creates a new version directory.

## Using WandB on HPC

High-Performance Computing (HPC) environments require special consideration for experiment tracking. WandB works well on HPC systems, but you need to handle authentication and potential connectivity limitations.

### Setting up WandB on HPC

First, authenticate WandB on your HPC system. This only needs to be done once:

```bash
# Login to compute node or interactive session
# Load Python module
# Activate your conda environment
conda activate careamics

# Login to WandB
wandb login
```

Enter your API key when prompted. This stores your credentials in `~/.netrc`.

!!! tip "Alternative: API key in environment"

    If you prefer not to store credentials in `~/.netrc`, you can use environment variables in your job scripts (see below).

### SLURM script template for WandB

Create a SLURM script to run your CAREamics training with WandB logging. Remember to set the configuration to logger="wandb" in your training script:

```bash
#!/bin/bash
#SBATCH --job-name=experiment_name
#SBATCH --output=logs/experiment_name_%j.out
#SBATCH --error=logs/experiment_name_%j.err
#SBATCH --time=4:00:00 # (1)!
#SBATCH --mem=32G # (1)!
#SBATCH --gres=gpu:1 # (1)!

# Load required modules
# WandB configuration
export WANDB_API_KEY="your_api_key_here"  # (2)!
export WANDB_PROJECT="careamics-experiment"
export WANDB_ENTITY="your_username"  # (3)!
export WANDB_RUN_NAME="n2v_${SLURM_JOB_ID}"  # (4)!

# Optional: Configure WandB cache directory
export WANDB_DIR="/scratch/${USER}/wandb"  # (5)!
export WANDB_CACHE_DIR="/scratch/${USER}/wandb_cache"
mkdir -p $WANDB_DIR $WANDB_CACHE_DIR

# Activate environment
# Run training script
```
1. Adjust according to your HPC parameters
2. Get your API key from https://wandb.ai/authorize
3. Replace with your WandB username or team name
4. Automatically name runs with the SLURM job ID for tracking
5. Use fast scratch storage for WandB cache to improve performance

### Handling connectivity issues

HPC compute nodes may have limited or no internet connectivity. Here are strategies to handle this:

```python
# Option 1: Use offline mode (logs locally, sync later)
os.environ["WANDB_MODE"] = "offline"

# After job completes, sync from login node:
# wandb sync /scratch/username/wandb/run_id
```

```bash 
#!/bin/bash
# Run this on login node after jobs complete

# Sync all offline runs
wandb sync /scratch/$USER/wandb/offline-run-*

# Or sync specific run
wandb sync /scratch/$USER/wandb/offline-run-20240315_143022-abc123
```

!!! warning "Storage considerations"

    WandB caches data locally. On HPC systems:
    
    - Use scratch space for `WANDB_DIR` and `WANDB_CACHE_DIR` if you have access to such space
    - Avoid using home directories (often have strict quotas)
    - Clean up old runs periodically: `wandb sync --clean`


## Using TensorBoard on HPC

TensorBoard is well-suited for HPC environments due to its offline nature and minimal external dependencies. However, viewing the dashboard requires some additional setup.

### SLURM script template for TensorBoard

```bash 
#!/bin/bash
#SBATCH --job-name=experiment_name
#SBATCH --output=logs/experiment_name_%j.out
#SBATCH --error=logs/experiment_name_%j.err
#SBATCH --time=4:00:00 # (1)!
#SBATCH --mem=32G # (1)!
#SBATCH --gres=gpu:1 # (1)!

# Load required modules
# Set working directories
export EXPERIMENT_NAME="n2v_${SLURM_JOB_ID}"
export WORK_DIR="/scratch/${USER}/tensorboard_runs/${EXPERIMENT_NAME}"
mkdir -p $WORK_DIR

# Activate environment
# Run training script
```
1. Adjust according to your HPC parameters

### Viewing TensorBoard on HPC

Since HPC compute nodes typically don't allow direct browser access, you have two options for viewing TensorBoard:

#### Option 1: Using SLURM job for TensorBoard server

```bash
#!/bin/bash
#SBATCH --job-name=experiment_name
#SBATCH --output=logs/experiment_name_%j.out
#SBATCH --time=2:00:00  # (1)! # (2)!
#SBATCH --mem=8G # (1)!
#SBATCH --gres=gpu:1 # (1)!

# Load required modules
# Activate environment

# Get hostname and print connection info
HOSTNAME=$(hostname)
PORT=6006

echo "========================================="
echo "TensorBoard Server Information"
echo "========================================="
echo "Node: ${HOSTNAME}"
echo "Port: ${PORT}"
echo "========================================="
echo "To connect, run on your LOCAL machine:"
echo "ssh -L ${PORT}:${HOSTNAME}:${PORT} ${USER}@hpc-login.university.edu"
echo "Then open: http://localhost:${PORT}"
echo "========================================="

# Start TensorBoard
tensorboard \
    --logdir /scratch/${USER}/tensorboard_runs \
    --port ${PORT} \
    --bind_all  # (3)!
```
1. Adjust according to your HPC parameters
2. Keep it running while you need to view results
3. Allow connections from any host (required for HPC networking)

Then on your local machine:
```bash
# Replace with actual hostname from job output
ssh -L 6006:compute-node-123:6006 username@hpc-login.university.edu
```

#### Option 2: Download logs and view locally 

```bash
# On your local machine, download TensorBoard logs
rsync -avz username@hpc-login.university.edu:/path_to_folders/tensorboard_runs ./local_tensorboard_runs

# View locally
tensorboard --logdir ./local_tensorboard_runs
```

### Comparing multiple experiments

TensorBoard excels at comparing runs. Structure your experiments for easy comparison:

```python 
from pathlib import Path
from careamics import CAREamist
from careamics.config import create_n2v_configuration

# Create parent directory for all experiments
base_dir = Path("/scratch/username/tensorboard_runs/n2v_comparison")
base_dir.mkdir(parents=True, exist_ok=True)

# Define experiments
experiments = [
    {"name": "baseline", "patch_size": 64, "batch_size": 16},
    {"name": "larger_patches", "patch_size": 128, "batch_size": 8},
    {"name": "smaller_batch", "patch_size": 64, "batch_size": 8},
]

for exp in experiments:
    config = create_n2v_configuration(
        experiment_name=exp["name"],
        data_type="array",
        axes="YX",
        patch_size=[exp["patch_size"]] * 2,
        batch_size=exp["batch_size"],
        num_epochs=100,
        logger="tensorboard"
    )
    
    work_dir = base_dir / exp["name"]
    careamist = CAREamist(source=config, work_dir=work_dir)
    careamist.train(train_source=train_data)

# View all experiments together
tensorboard --logdir="/path_to_folders/tensorboard_runs/n2v_comparison"
```
When you launch TensorBoard pointing to the parent directory, it will automatically display all experiments together for comparison.
Both WandB and TensorBoard offer powerful experiment tracking capabilities for CAREamics:

**Choose WandB when:**

- Working in teams requiring centralized tracking
- Need cloud storage and sharing
- Want comprehensive system monitoring
- Have reliable internet connectivity

**Choose TensorBoard when:**

- Working on HPC with limited connectivity
- Prefer local, offline tracking
- Need lightweight setup
- Want full control over data storage

**On HPC systems:**

- Use scratch space for logs and caches
- Set up SSH tunneling for TensorBoard viewing
- Configure WandB for offline mode when connectivity is unreliable
- Organize experiments in clear directory hierarchies

Both tools integrate seamlessly with CAREamics so choose the tool that best fits your workflow and infrastructure constraints.
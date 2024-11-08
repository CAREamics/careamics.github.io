---
icon: octicons/file-media-24
description: Applications
---

# Applications

Click on your algorithm of choice to explore various applications. We collected the 
algorithms based on the type of training data they require! 

## Keywords

- **no ground-truth**: The algorithm trains without clean images.
- **single image**: The algorithm can train on a single image.
- **pairs of noisy images**: The algorithm requires pairs of noisy images.
- **ground-truth**: The algorithm requires pairs of clean and noisy images.


## Denoising noisy images without clean data

You have noisy images and no clean images? No problem! These algorithms can help you, as
they do not require any ground-truth data. You can also train on a single image of
reasonable size.

<!-- The following links are pointing to non existing pages (pre-build) -->
<!-- Disable markdown link check to allow bulding the pages -->
<!-- markdown-link-check-disable -->
<div class="md-container secondary-section">
    <div class="g">
        <div class="section">
            <div class="component-wrapper" style="display: block;">
                <div class="responsive-grid">
                    <!-- N2V -->
                    <a class="card-wrapper" href="Noise2Void">
                        <div class="card"> 
                            <div class="card-body">
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<--  "cpu.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>Noise2Void</h5>
                                    <p>
                                        A self-supervised denoising algorithm based on a 
                                        pixel masking scheme.
                                    </p>
                                </div>
                            </div>
                            <div class="card-tags">
                                <span class=tag>no ground-truth</span>
                                <span class=tag>single image</span>
                            </div>
                        </div>
                    </a>
                    <!-- N2V2 -->
                    <a class="card-wrapper" href="N2V2">
                        <div class="card"> 
                            <div class="card-body">
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<--  "cpu.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>N2V2</h5>
                                    <p>
                                        A variant of Noise2Void capable of removing 
                                        checkboard artefacts.
                                    </p>
                                </div>
                            </div>
                            <div class="card-tags">
                                <span class=tag>no ground-truth</span>
                                <span class=tag>single image</span>
                            </div>
                        </div>
                    </a>
                </div>
                <div class="responsive-grid">
                    <!-- structN2V -->
                    <a class="card-wrapper" href="structN2V">
                        <div class="card"> 
                            <div class="card-body">
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<--  "cpu.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>StructN2V</h5>
                                    <p>
                                        A variant of Noise2Void that uses an enhanced mask
                                        to remove structured noise.
                                    </p>
                                </div>
                            </div>
                            <div class="card-tags">
                                <span class=tag>no ground-truth</span>
                                <span class=tag>single image</span>
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>


If you have multiple noisy instances of the same structure (e.g. a noisy time-lapse), 
then Noise2Noise might be the right choice for you.

<!-- The following links are pointing to non existing pages (pre-build) -->
<!-- Disable markdown link check to allow bulding the pages -->
<!-- markdown-link-check-disable -->
<div class="md-container secondary-section">
    <div class="g">
        <div class="section">
            <div class="component-wrapper" style="display: block;">
                <div class="responsive-grid">
                    <!-- Noise2Noise -->
                    <a class="card-wrapper" href="Noise2Noise">
                        <div class="card"> 
                            <div class="card-body">
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<--  "cpu.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>Noise2Noise</h5>
                                    <p>
                                        A supervised methods that can denoise images without
                                        corresponding clean data.
                                    </p>
                                </div>
                            </div>
                            <div class="card-tags">
                                <span class=tag>no ground-truth</span>
                                <span class=tag>pairs of noisy images</span>
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>


## Supervised restoration with clean images

If you have pairs of clean (e.g. high SNR, long exposure or high laser power) and noisy
images, then CARE might be the right choice for you.

Note that CARE can be used for a variety of tasks, such as denoising, deconvolution,
isotropic resolution restoration or projection.


<div class="md-container secondary-section">
    <div class="g">
        <div class="section">
            <div class="component-wrapper" style="display: block;">
                <div class="responsive-grid">
                    <!-- CARE -->
                    <a class="card-wrapper" href="CARE">
                        <div class="card"> 
                            <div class="card-body"> 
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<--  "cpu.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>CARE</h5>
                                    <p>
                                        The original supervised method to restore microscopy
                                        images.
                                    </p>
                                </div>
                            </div>
                            <div class="card-tags">
                                <span class=tag>ground-truth</span>
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>



## Using the Lightning API

If you need more control on the algorithm training, for instance to implement or replace
features, you can use the Lightning API. 

It uses [PyTorch Lightning](https://lightning.ai/docs/pytorch/stable/) and the 
CAREamics Lightning components.


<div class="md-container secondary-section">
    <div class="g">
        <div class="section">
            <div class="component-wrapper" style="display: block;">
                <div class="responsive-grid">
                    <!-- N2V -->
                    <a class="card-wrapper" href="Lightning_API">
                        <div class="card"> 
                            <div class="card-body"> 
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<--  "cpu.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>Lightning API</h5>
                                    <p>
                                        Get full control of the training and prediction
                                        pipelines by using CAREamics Lightning components.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
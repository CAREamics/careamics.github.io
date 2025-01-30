---
icon: octicons/cpu-24
description: Descriptions of the algorithms.
---

# Algorithms

!!! warning "Work in progress"
    These pages are still under construction and we expect a lot more details 
    descriptions of each algorithm in the near future.

In these pages, you will find explanations and illustrations of how the various
algorithms used in CAREamics work. These algorithms are divided into different 
sections and a few keywords help you to understand the main characteristics of
each algorithm. 

## Keywords

- **no ground-truth**: The algorithm trains without clean images.
- **single image**: The algorithm can train on a single image.
- **pairs of noisy images**: The algorithm requires pairs of noisy images.
- **ground-truth**: The algorithm requires pairs of clean and noisy images.


## Self-supervised restoration
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


## Noise Models


<div class="md-container secondary-section">
    <div class="g">
        <div class="section">
            <div class="component-wrapper" style="display: block;">
                <div class="responsive-grid">
                    <!-- Noise2Noise -->
                    <a class="card-wrapper" href="NoiseModels">
                        <div class="card"> 
                            <div class="card-body">
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<--  "cpu.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>Noise Models</h5>
                                    <p>
                                        Methods to estimate the noise models of
                                        microscopes.
                                    </p>
                                </div>
                            </div>
                            <div class="card-tags">
                                <span class=tag>no ground-truth</span>
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </div>


## Supervised restoration without ground-truth


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


## Supervised restoration

<div class="md-container secondary-section">
    <div class="g">
        <div class="section">
            <div class="component-wrapper" style="display: block;">
                <div class="responsive-grid">
                    <!-- N2V -->
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
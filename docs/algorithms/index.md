---
icon: octicons/cpu-24
description: Descriptions of the algorithms.
---

# Algorithms

!!! warning "Work in progress"
    These pages are still under construction and we expect a lot more details 
    descriptions of each algorithm in the near future.

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
                    <a class="card-wrapper" href="n2v/Noise2Void">
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
                        </div>
                    </a>
                    <!-- N2V2 -->
                    <a class="card-wrapper" href="n2v2">
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
                        </div>
                    </a>
                </div>
                <div class="responsive-grid">
                    <!-- structN2V -->
                    <a class="card-wrapper" href="structn2v">
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
                        </div>
                    </a>
                    <!-- Noise2Noise -->
                    <a class="card-wrapper" href="n2n">
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
                    <a class="card-wrapper" href="care">
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
                        </div>
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
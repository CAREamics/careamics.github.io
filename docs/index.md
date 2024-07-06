---
icon: octicons/home-24
description: Guide and documentation.
---

<img src="assets/banner_careamics_large.png" width="400">

[![License](https://img.shields.io/pypi/l/careamics.svg?color=green)](https://github.com/CAREamics/careamics/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/careamics.svg?color=green)](https://pypi.org/project/careamics)
[![Python Version](https://img.shields.io/pypi/pyversions/careamics.svg?color=green)](https://python.org)
[![CI](https://github.com/CAREamics/careamics/actions/workflows/ci.yml/badge.svg)](https://github.com/CAREamics/careamics/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/CAREamics/careamics/branch/main/graph/badge.svg)](https://codecov.io/gh/CAREamics/careamics)

# Documentation

CAREamics is a PyTorch library aimed at simplifying the use of Noise2Void and its many
variants and cousins (CARE, Noise2Noise, N2V2, P(P)N2V, HDN, muSplit etc.).

## Why CAREamics?

Noise2Void is a widely used denoising algorithm, and is readily available from the `n2v`
python package. However, n2v is based on TensorFlow and Keras and we found it 
increasingly hard to maintain. In addition, more recent methods (PPN2V, DivNoising,
HDN) are all implemented in PyTorch, but are lacking the extra features that would make
them usable by the community.

The aim of CAREamics is to provide a PyTorch library reuniting all the latest methods
in one package, while providing a simple and consistent API. The library relies on 
PyTorch Lightning as a back-end. In addition, we will provide extensive documentation and 
tutorials on how to best apply these methods in a scientific context.

!!! warning "Work in progress"
    These pages are still under construction.

## Getting Started
<div class="md-container secondary-section">
    <div class="g">
        <div class="section">
            <div class="component-wrapper" style="display: block;">
                <!-- New row -->
                <div class="responsive-grid">
                    <!-- Installation -->
                    <a class="card-wrapper" href="installation">
                        <div class="card">
                            <div class="card-body"> 
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<--  "desktop-download.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>Installation</h5>
                                    <p>
                                        Get started with CAREamics installation.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </a>
                    <!-- Current state -->
                    <a class="card-wrapper" href="current_state">
                        <div class="card">
                            <div class="card-body">
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<-- "milestone.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>Current State</h5>
                                    <p>
                                        Check out where we stand and where we want to go.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </a>
                </div>
                <!-- New row -->
                <div class="responsive-grid">
                    <!-- Guides -->
                    <a class="card-wrapper" href="guides">
                        <div class="card">
                            <div class="card-body">
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<-- "repo.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>Guides</h5>
                                    <p>
                                        In-depth guides on CAREamics usage and features.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </a>
                    <!-- Application -->
                    <a class="card-wrapper" href="applications">
                        <div class="card">
                            <div class="card-body">
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<-- "file-media.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>Applications</h5>
                                    <p>
                                        Examples of CAREamics in action on various datasets.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </a>
                </div>
                <!-- New row -->
                <div class="responsive-grid">
                    <!-- Algorithms -->
                    <a class="card-wrapper" href="algorithms">
                        <div class="card">
                            <div class="card-body">
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<-- "cpu.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>Algorithms</h5>
                                    <p>
                                        Dive into the various CAREamics algorithms.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </a>
                    <!-- Code reference -->
                    <a class="card-wrapper" href="reference">
                        <div class="card">
                            <div class="card-body">
                                <div class="logo">
                                    <span class="twemoji">
                                        --8<-- "code.svg"
                                    </span>
                                </div>
                                <div class="card-content">
                                    <h5>Code Reference</h5>
                                    <p>
                                        Code documentation for all CAREamics libraries.
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


## Feedback

We are always welcoming feedback on what to improve of what features could be useful,
therefore do not hesitate to open an issue on the
[Github repository](https://github.com/CAREamics/careamics)!

<!-- ## Cite us -->
# Summer 2026 Research Roadmap

Structured plan for the May–October 2026 window. The goal is to arrive at
the end of summer with a portfolio-grade GitHub repository demonstrating
the signal-processing and ML foundations for adaptive SiC grinding
control, with at least one piece of work substantive enough to form the
basis of a future conference submission.

## Guiding principle

Research quality over quantity. **One working module per month, well
documented, with reproducible results, beats five half-finished modules.**

## Month-by-month

### May 2026 — Signal processing foundations
- Finalize `01_lempel_ziv_stability` (✅ done as of April 2026)
- Build `02_fft_wavelet_features`:
  - Classical FFT spectrum analysis on synthetic grinding signal
  - Short-time Fourier transform (STFT) for time-frequency view
  - Continuous wavelet transform (CWT) using `pywt` library
  - Compare: which representation best localizes the instability event?
- **Milestone:** three signal-processing techniques applied to the same
  signal, with a comparison write-up in the module README.

### June 2026 — Synthetic dataset generation
- Build `03_synthetic_burn_dataset`:
  - Parametric generator for grinding signals with configurable
    burn-event parameters (onset time, severity, duration)
  - Multi-channel: force + vibration + acoustic emission (AE) channels
  - Dataset class in the style of scikit-learn / PyTorch
  - Generate ~1000 labeled examples (balanced normal / burn)
- **Milestone:** reproducible dataset generator, saved as a Python
  package module with unit tests.

### July 2026 — First ML pipeline
- Build `04_ml_burn_detection`:
  - Feature extraction: combine LZC, FFT-bands, wavelet energies
  - Train classical classifiers: logistic regression, random forest, SVM
  - Proper train/test split, cross-validation, confusion matrix
  - Compare models; report precision/recall per class
- **Milestone:** end-to-end pipeline from raw signal → burn classification,
  with a Jupyter notebook showing the analysis.

### August 2026 — Multi-sensor fusion
- Build `05_multi_sensor_fusion`:
  - Feature-level fusion across force + vibration + AE
  - KPCA for dimensionality reduction (following Guo et al. 2019)
  - Compare: single-sensor vs. fused multi-sensor performance
  - First deep-learning baseline: a small 1D-CNN or TCN on raw signals
- **Milestone:** clear, published comparison of fusion strategies with
  plotted results.

### September–October 2026 — Polish & write-up
- Clean all module READMEs; ensure every demo runs from a fresh clone
- Write a top-level technical blog post summarizing the summer's work:
  - Problem framing (SiC grinding challenge)
  - Techniques demonstrated
  - Key findings
  - Open questions for PhD research
- Post to GitHub Pages or Medium; link from the repo README
- Back-reference to next semester's coursework connections
- **Milestone:** blog post published. First external-facing artifact.

## Time budget

Roughly 8–10 hours per week during school terms, ramping up during
breaks. This is a part-time researcher's pace — sustainable over years
rather than sprinting and burning out.

## What I am NOT trying to do this summer

- Publish a paper (too early; aim for 2027–2028)
- Train state-of-the-art deep models (foundations first)
- Work with real grinding data (no equipment access; synthetic is fine
  for prototyping signal-processing and ML pipelines)
- Compete with published work in the field (goal is to **demonstrate
  readiness for PhD-level research**, not outperform established labs)

## Review cadence

- **Weekly:** Friday review of progress against the month's milestone
- **Monthly:** write a short (few-paragraph) summary in the repo's
  `progress/` folder; this becomes raw material for the September blog post

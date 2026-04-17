# In-Process Monitoring for SiC Wafer Grinding

Research prototype repository exploring multi-sensor signal processing and
machine learning for real-time surface quality prediction in silicon carbide
precision grinding.

## Motivation

Silicon carbide (SiC) power electronics are a key enabler for electric
mobility, renewable energy infrastructure, and efficient industrial systems.
Wafer-scale SiC grinding, however, remains one of the most challenging
steps in the SiC manufacturing chain due to the material's extreme hardness
and brittleness.

This repository develops the signal-processing and ML foundations for
**adaptive, real-time grinding control** — predicting surface quality and
detecting process anomalies (burn events, chatter, wheel wear) from
multi-sensor data before they damage the wafer.

## What's here

| Module | Techniques | Status |
|---|---|---|
| `01_lempel_ziv_stability` | Information-theoretic signal stability | ✅ Working |
| `02_fft_wavelet_features` | Frequency & time-frequency analysis | 🚧 Summer 2026 |
| `03_synthetic_burn_dataset` | Burn-event data generator | 🚧 Summer 2026 |
| `04_ml_burn_detection` | Classical ML + feature fusion | 🚧 Summer 2026 |
| `05_multi_sensor_fusion` | KPCA + deep learning on fused signals | 🚧 Summer 2026 |

See [`SUMMER_ROADMAP.md`](SUMMER_ROADMAP.md) for the timeline.

## Quick start

```bash
git clone https://github.com/<your-username>/sic-grinding-monitoring.git
cd sic-grinding-monitoring
pip install -r requirements.txt
python 01_lempel_ziv_stability/lzc_stability.py
```

## References

Key papers informing this work are listed in [`references/papers.md`](references/papers.md).

## About

Developed as part of ongoing research toward a PhD in adaptive control of
SiC/GaN precision manufacturing. Feedback from researchers in the field is
warmly welcomed — please open an issue or reach out directly.

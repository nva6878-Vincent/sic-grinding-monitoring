# Module 01 — Lempel-Ziv Complexity for Grinding Stability

## What this module does

Implements **Lempel-Ziv Complexity (LZC)** as a signal stability metric for
grinding processes, and demonstrates on a synthetic vibration signal that
LZC cleanly separates stable from unstable grinding regions.

## Why LZC?

LZC is an information-theoretic complexity measure originally developed
for data compression (Lempel & Ziv, 1976). Applied to sensor signals:

- **Quasi-periodic signals** (clean grinding: spindle + wheel resonances)
  compress efficiently — the same patterns repeat. **Low LZC.**
- **Aperiodic signals** (chatter, burn onset, wheel wear) have few
  repeating patterns. **High LZC.**

Unlike FFT-based stability metrics, LZC makes no assumption about the
signal's frequency content — it captures a different axis of "complexity"
that is complementary to spectral features.

## Results

On a 2-second synthetic signal with a 600 ms injected instability zone:

| Region | Mean Normalized LZC |
|---|---|
| Stable | ~0.97 |
| Unstable | ~1.74 |
| **Contrast** | **~1.8×** |

The instability is detected within one window (~50 ms), making LZC
suitable as a real-time stability monitor.

![LZC stability demo](lzc_stability_demo.png)

## How it works

1. **Binarize** the vibration signal using median-threshold → binary string
2. **Parse** the binary string left-to-right, consuming the shortest novel
   substring at each step (classical LZ76 algorithm)
3. **Count** the number of distinct substrings — that's the LZC
4. **Normalize** by the random-sequence upper bound `n / log₂(n)`
5. Compute over **sliding windows** for real-time tracking

## Running it

```bash
pip install numpy matplotlib
python lzc_stability.py
```

Produces `lzc_stability_demo.png` in the current directory.

## Reference

Guo, B., Zhang, Q., Peng, Q., Zhuang, J., Wu, F., & Zhang, Q. (2019).
*Silicon Carbide Surface Quality Prediction Based on Artificial
Intelligence Methods on Multi-sensor Fusion Detection Test Platform.*
Machining Science and Technology, 23(1), 1–17.
DOI: [10.1080/10910344.2018.1486414](https://doi.org/10.1080/10910344.2018.1486414)

## Next steps

This module produces a stability feature. In module `04_ml_burn_detection`,
LZC will be combined with FFT and wavelet features as input to a
classifier that distinguishes normal grinding from burn-onset events.

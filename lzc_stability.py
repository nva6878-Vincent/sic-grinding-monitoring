"""
Lempel-Ziv Complexity for Grinding Process Stability Analysis
==============================================================

Reproduces the core stability-analysis idea from:
  Guo et al. (2019), "Silicon Carbide Surface Quality Prediction Based on
  Artificial Intelligence Methods on Multi-sensor Fusion Detection Test
  Platform", Machining Science and Technology, Vol 23 No 1.
  DOI: 10.1080/10910344.2018.1486414

The paper uses Lempel-Ziv Complexity (LZC) as a stability metric for the
grinding process. Intuition:
  - When the grinding wheel engages cleanly, the vibration signal is
    quasi-periodic (spindle + wheel resonances dominate). LOW LZC.
  - When instability develops (chatter, wheel wear, burn onset, chip
    loading), the signal becomes less periodic. HIGH LZC.

This demo generates a synthetic grinding vibration signal with an
injected instability zone in the middle, and shows sliding-window LZC
tracking the instability in real time.

Usage:  python lzc_stability.py
Output: lzc_stability_demo.png  (two-panel plot)
"""

import numpy as np
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
# 1. Synthetic signal generator
# -----------------------------------------------------------------------------

def generate_grinding_signal(duration=2.0, fs=10_000,
                              spindle_hz=50, wheel_hz=200,
                              unstable_start=0.7, unstable_end=1.3,
                              seed=42):
    """
    Generate synthetic grinding vibration with an injected instability zone.

    Stable regions: sum of two sinusoids representing spindle + grinding-
      wheel resonances, plus small Gaussian measurement noise. This signal
      is quasi-periodic and compresses well -> low LZC.

    Unstable region: additive broadband noise plus a non-linearly modulated
      high-frequency burst (mimicking chatter / chip loading). Breaks the
      periodic structure -> high LZC.

    Parameters
    ----------
    duration : float, seconds
    fs       : int, sampling rate in Hz (default 10 kHz, typical for
               accelerometer or AE sensing in grinding)
    """
    rng = np.random.default_rng(seed)
    t = np.arange(0, duration, 1 / fs)

    # Stable baseline: quasi-periodic
    signal = (
        np.sin(2 * np.pi * spindle_hz * t)
        + 0.5 * np.sin(2 * np.pi * wheel_hz * t)
        + 0.1 * rng.standard_normal(len(t))
    )

    # Inject instability: chaotic burst in the middle window
    mask = (t >= unstable_start) & (t <= unstable_end)
    chaos = 1.5 * rng.standard_normal(mask.sum())
    chaos += (0.8 * np.sin(2 * np.pi * 350 * t[mask])
              * rng.standard_normal(mask.sum()))
    signal[mask] += chaos

    return t, signal


# -----------------------------------------------------------------------------
# 2. Lempel-Ziv complexity
# -----------------------------------------------------------------------------

def lempel_ziv_complexity(binary_sequence):
    """
    Compute Lempel-Ziv 1976 complexity by parsing distinct substrings.

    Algorithm (classical LZ76 parsing):
      Walk the sequence left-to-right. At each position, consume the
      SHORTEST substring not previously encountered. Each such novel
      substring increments the complexity counter.

    For a signal of length n:
      - A purely random sequence has expected complexity ~ n / log2(n)
      - A purely periodic sequence has complexity that grows like log(n)
      - Real signals fall between these extremes

    Parameters
    ----------
    binary_sequence : str
        A string of '0' and '1' characters.

    Returns
    -------
    int : number of distinct substrings (the LZ76 complexity)
    """
    substrings = set()
    n = len(binary_sequence)
    ind = 0
    inc = 1

    while ind + inc <= n:
        candidate = binary_sequence[ind: ind + inc]
        if candidate in substrings:
            # Already seen this pattern; try extending by one character
            inc += 1
        else:
            # Novel pattern; record it and restart from the next position
            substrings.add(candidate)
            ind += inc
            inc = 1

    return len(substrings)


def normalized_lzc(binary_sequence):
    """
    LZC normalized by the theoretical upper bound for random sequences.

    For long random binary sequences, LZC approaches n / log2(n).
    Dividing by this bound gives a value in roughly [0, 1]:
      near 0  -> highly periodic / predictable
      near 1  -> maximally random / unpredictable
    """
    n = len(binary_sequence)
    if n < 2:
        return 0.0
    c = lempel_ziv_complexity(binary_sequence)
    upper_bound = n / np.log2(n)
    return c / upper_bound


def binarize(signal):
    """
    Median-threshold binarization: x > median -> '1', else '0'.

    This is the standard first step for LZC on continuous signals.
    Median (not mean) is used for robustness to outliers.
    """
    median = np.median(signal)
    return ''.join('1' if x > median else '0' for x in signal)


# -----------------------------------------------------------------------------
# 3. Sliding-window analysis
# -----------------------------------------------------------------------------

def sliding_lzc(signal, window_size, step):
    """
    Compute normalized LZC over sliding windows of the signal.

    Returns arrays of (window_center_index, lzc_value). The window center
    is used as the time reference for plotting.
    """
    centers = []
    lzc_values = []

    for start in range(0, len(signal) - window_size + 1, step):
        window = signal[start: start + window_size]
        binary = binarize(window)
        lzc_values.append(normalized_lzc(binary))
        centers.append(start + window_size // 2)

    return np.array(centers), np.array(lzc_values)


# -----------------------------------------------------------------------------
# 4. Demo
# -----------------------------------------------------------------------------

def main():
    fs = 10_000
    duration = 2.0
    unstable_start = 0.7
    unstable_end = 1.3

    # Generate signal
    t, signal = generate_grinding_signal(duration=duration, fs=fs,
                                         unstable_start=unstable_start,
                                         unstable_end=unstable_end)

    # Sliding-window LZC
    window_size = 500   # 50 ms windows at 10 kHz
    step = 100          # 10 ms step -> 100 Hz update rate
    centers, lzc = sliding_lzc(signal, window_size, step)
    t_lzc = centers / fs

    # Report the contrast
    stable_mask = (t_lzc < unstable_start) | (t_lzc > unstable_end)
    unstable_mask = (t_lzc >= unstable_start) & (t_lzc <= unstable_end)
    print(f"Mean normalized LZC (stable region):   {lzc[stable_mask].mean():.3f}")
    print(f"Mean normalized LZC (unstable region): {lzc[unstable_mask].mean():.3f}")
    print(f"Contrast ratio: {lzc[unstable_mask].mean() / lzc[stable_mask].mean():.2f}x")

    # Plot
    fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

    axes[0].plot(t, signal, linewidth=0.5, color='steelblue')
    axes[0].axvspan(unstable_start, unstable_end, alpha=0.18, color='crimson',
                    label='Injected instability zone')
    axes[0].set_ylabel('Vibration amplitude')
    axes[0].set_title('Synthetic grinding vibration signal')
    axes[0].legend(loc='upper right')
    axes[0].grid(alpha=0.3)

    axes[1].plot(t_lzc, lzc, color='darkorange', linewidth=1.8)
    axes[1].axvspan(unstable_start, unstable_end, alpha=0.18, color='crimson')
    axes[1].set_xlabel('Time (s)')
    axes[1].set_ylabel('Normalized LZC')
    axes[1].set_title('Lempel-Ziv complexity per 50 ms window')
    axes[1].grid(alpha=0.3)

    plt.tight_layout()
    output_path = 'lzc_stability_demo.png'
    plt.savefig(output_path, dpi=150)
    print(f"\nPlot saved to {output_path}")
    plt.show()


if __name__ == '__main__':
    main()

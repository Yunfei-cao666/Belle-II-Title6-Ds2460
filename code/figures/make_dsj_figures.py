#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make illustrative figures for the Belle 2003 D_sJ analysis note.

IMPORTANT
---------
These are TOY REPRODUCTIONS based on the published Belle 2003 yields and
resolutions. They are NOT a reanalysis of Belle/Belle II data. The figures are
for planning / group meetings only.

Run:
    python code/figures/make_dsj_figures.py
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


ROOT = Path(__file__).resolve().parents[2]
FIG = ROOT / "figures"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})


def truncated_exp(rng, n, xmin, xmax, scale):
    """Sample a truncated exponential on [xmin, xmax]."""
    u = rng.random(n)
    return xmin - scale * np.log(1.0 - u * (1.0 - np.exp(-(xmax - xmin) / scale)))


def toy_hist(mean, sigma, n_sig, n_bkg, xmin, xmax, nbins, seed,
             xlabel, title, annotation, outname, extra_peak=None,
             bkg_scale=0.10):
    """Draw a toy histogram + illustrative fit curve."""
    rng = np.random.default_rng(seed)
    sig = rng.normal(mean, sigma, int(n_sig))
    bkg = truncated_exp(rng, int(n_bkg), xmin, xmax, bkg_scale)

    samples = [sig, bkg]
    if extra_peak is not None:
        m2, s2, n2 = extra_peak
        samples.append(rng.normal(m2, s2, int(n2)))
    data = np.concatenate(samples)
    data = data[(data >= xmin) & (data <= xmax)]

    edges = np.linspace(xmin, xmax, nbins + 1)
    counts, _ = np.histogram(data, bins=edges)
    centers = 0.5 * (edges[1:] + edges[:-1])
    width = edges[1] - edges[0]
    yerr = np.sqrt(np.maximum(counts, 1))

    x = np.linspace(xmin, xmax, 1000)

    def gauss(m, s, n):
        return n * width / (s * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - m) / s) ** 2)

    bkg_norm = n_bkg * width / (bkg_scale * (1 - np.exp(-(xmax - xmin) / bkg_scale)))
    yfit = gauss(mean, sigma, n_sig) + bkg_norm * np.exp(-(x - xmin) / bkg_scale)
    if extra_peak is not None:
        yfit += gauss(*extra_peak)

    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    ax.errorbar(centers, counts, yerr=yerr, fmt="o", ms=3.2, lw=1,
                color="black", label="toy data")
    ax.plot(x, yfit, color="#c0392b", lw=2, label="fit model")
    ax.axvspan(mean - 2 * sigma, mean + 2 * sigma, color="#f1c40f", alpha=0.15)
    ax.axvline(mean, color="#7f8c8d", ls="--", lw=1)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(f"Events / ({width * 1000:.1f} MeV)")
    ax.set_title(title)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper right", frameon=False, fontsize=9)
    ax.text(0.03, 0.95, annotation, transform=ax.transAxes,
            va="top", ha="left", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#bdc3c7", alpha=0.9))
    fig.text(0.99, 0.01,
             "Toy reproduction of published Belle 2003 yields/resolutions — not raw data",
             ha="right", va="bottom", fontsize=7, color="#7f8c8d")
    fig.savefig(FIG / outname)
    plt.close(fig)


def combined_plot():
    """Four-panel summary."""
    panels = [
        dict(mean=0.3487, sigma=0.0071, n_sig=761, n_bkg=1500, xmin=0.10, xmax=0.60,
             title=r"(a) $D_{sJ}(2317)^+ \to D_s^+ \pi^0$",
             xlabel=r"$\Delta M(D_s^+ \pi^0)$ [GeV]",
             annotation="Belle 2003: N = 761 ± 44 ± 30\nm = 2317.2 MeV",
             seed=11),
        dict(mean=0.3441, sigma=0.0058, n_sig=126, n_bkg=520, xmin=0.10, xmax=0.60,
             title=r"(b) $D_{sJ}(2457)^+ \to D_s^{*+} \pi^0$",
             xlabel=r"$\Delta M(D_s^{*+} \pi^0)$ [GeV]",
             annotation="Belle 2003: N = 126 ± 25 ± 12\nm = 2456.5 MeV",
             seed=12),
        dict(mean=0.4910, sigma=0.0080, n_sig=152, n_bkg=420, xmin=0.35, xmax=0.65,
             title=r"(c) $D_{sJ}(2457)^+ \to D_s^+ \gamma$",
             xlabel=r"$\Delta M(D_s^+ \gamma)$ [GeV]",
             annotation="Belle 2003: N = 152 ± 18\nm = 2459.5 MeV",
             seed=13),
        dict(mean=0.4914, sigma=0.0058, n_sig=59.7, n_bkg=480, xmin=0.35, xmax=0.65,
             title=r"(d) $D_{sJ}(2457)^+ \to D_s^+ \pi^+ \pi^-$",
             xlabel=r"$\Delta M(D_s^+ \pi^+ \pi^-)$ [GeV]",
             annotation="Belle 2003: N = 59.7 ± 11.5\nplus $D_{s1}(2536)$: 56.5 ± 13.4",
             seed=14, extra_peak=(0.5700, 0.0060, 56.5)),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.2))
    for ax, p in zip(axes.ravel(), panels):
        rng = np.random.default_rng(p["seed"])
        sig = rng.normal(p["mean"], p["sigma"], int(p["n_sig"]))
        bkg = truncated_exp(rng, int(p["n_bkg"]), p["xmin"], p["xmax"], 0.10)
        samples = [sig, bkg]
        if "extra_peak" in p:
            m2, s2, n2 = p["extra_peak"]
            samples.append(rng.normal(m2, s2, int(n2)))
        data = np.concatenate(samples)
        data = data[(data >= p["xmin"]) & (data <= p["xmax"])]
        edges = np.linspace(p["xmin"], p["xmax"], 51)
        counts, _ = np.histogram(data, bins=edges)
        centers = 0.5 * (edges[1:] + edges[:-1])
        width = edges[1] - edges[0]
        yerr = np.sqrt(np.maximum(counts, 1))

        x = np.linspace(p["xmin"], p["xmax"], 1000)

        def gauss(m, s, n):
            return n * width / (s * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - m) / s) ** 2)

        bkg_norm = p["n_bkg"] * width / (0.10 * (1 - np.exp(-(p["xmax"] - p["xmin"]) / 0.10)))
        yfit = gauss(p["mean"], p["sigma"], p["n_sig"]) + bkg_norm * np.exp(-(x - p["xmin"]) / 0.10)
        if "extra_peak" in p:
            yfit += gauss(*p["extra_peak"])

        ax.errorbar(centers, counts, yerr=yerr, fmt="o", ms=2.6, lw=1, color="black")
        ax.plot(x, yfit, color="#c0392b", lw=1.8)
        ax.axvspan(p["mean"] - 2 * p["sigma"], p["mean"] + 2 * p["sigma"],
                   color="#f1c40f", alpha=0.15)
        ax.set_xlim(p["xmin"], p["xmax"])
        ax.set_ylim(bottom=0)
        ax.set_title(p["title"])
        ax.set_xlabel(p["xlabel"])
        ax.set_ylabel(f"Events / ({width * 1000:.0f} MeV)")
        ax.text(0.03, 0.95, p["annotation"], transform=ax.transAxes,
                va="top", ha="left", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#bdc3c7", alpha=0.9))

    fig.suptitle("Belle 2003 $D_{sJ}$ analysis — toy reproduction (not raw data)", y=1.01)
    fig.text(0.99, 0.01,
             "Based on published yields/resolutions; for planning only.",
             ha="right", va="bottom", fontsize=7, color="#7f8c8d")
    fig.tight_layout()
    fig.savefig(FIG / "fig_combined.png")
    plt.close(fig)


def yields_plot():
    modes = [
        r"$D_{sJ}(2317)^+\to D_s^+\pi^0$",
        r"$D_{sJ}(2457)^+\to D_s^{*+}\pi^0$",
        r"$D_{sJ}(2457)^+\to D_s^+\gamma$",
        r"$D_{sJ}(2457)^+\to D_s^+\pi^+\pi^-$",
        r"$D_{s1}(2536)^+\to D_s^+\pi^+\pi^-$",
    ]
    yields = [761, 126, 152, 59.7, 56.5]
    effs = [8.2, 4.7, 10.2, 15.8, 14.3]

    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ypos = np.arange(len(modes))[::-1]
    bars = ax.barh(ypos, yields, color="#2e86de", alpha=0.85)
    ax.set_yticks(ypos)
    ax.set_yticklabels(modes, fontsize=9)
    ax.set_xlabel("Published signal yield (Belle 2003)")
    ax.set_title("Belle 2003 $D_{sJ}$ yields and reconstruction efficiencies")
    for b, n, e in zip(bars, yields, effs):
        ax.text(b.get_width() + 12, b.get_y() + b.get_height() / 2,
                f"N={n:g}  ($\\varepsilon$={e:g}%)", va="center", fontsize=8)
    ax.set_xlim(0, max(yields) * 1.28)
    ax.grid(axis="x", alpha=0.25)
    fig.text(0.99, 0.01,
             "Published Belle 2003 values; not a Belle II measurement.",
             ha="right", va="bottom", fontsize=7, color="#7f8c8d")
    fig.tight_layout()
    fig.savefig(FIG / "fig_yields.png")
    plt.close(fig)


def chain_plot():
    """Schematic of the simplified Belle 2003-style chain."""
    fig, ax = plt.subplots(figsize=(11.5, 6.0))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6)
    ax.axis("off")

    def box(x, y, w, h, text, fc="#eaf2f8", ec="#2e86de", fs=9):
        p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.08",
                           fc=fc, ec=ec, lw=1.5)
        ax.add_patch(p)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)

    def arrow(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                     arrowstyle="->", mutation_scale=12,
                                     lw=1.2, color="#34495e"))

    # top
    box(3.6, 5.05, 3.8, 0.55, r"$e^+e^-\to c\bar c$ (continuum)", fc="#fef9e7", ec="#f39c12")
    box(3.6, 4.15, 3.8, 0.55, r"$D_{sJ}^+$ resonance", fc="#eaf2f8", ec="#2e86de")
    arrow(5.5, 5.05, 5.5, 4.70)

    # four decay modes
    modes = [
        (0.20, r"$D_s^+\pi^0$"),
        (2.85, r"$D_s^{*+}\pi^0$"),
        (5.50, r"$D_s^+\gamma$"),
        (8.15, r"$D_s^+\pi^+\pi^-$"),
    ]
    for x, label in modes:
        box(x, 3.10, 2.55, 0.55, label)
        arrow(5.5, 4.15, x + 1.275, 3.65)

    # D_s* -> D_s gamma for the D_s* pi0 mode
    box(8.15, 2.15, 2.55, 0.55, r"$D_s^{*+}\to D_s^+\gamma$",
        fc="#e8f8f5", ec="#16a085", fs=9)
    arrow(9.425, 3.10, 9.425, 2.70)

    # common D_s -> phi pi
    box(0.20, 0.80, 7.55, 0.60,
        r"$D_s^+\to\phi\pi^+$  (common for all modes)",
        fc="#e8f8f5", ec="#16a085", fs=9)
    for x in [1.475, 4.125, 6.775]:
        arrow(x, 3.10, x, 1.40)
    arrow(9.425, 2.15, 7.75, 1.40)

    # phi -> KK
    box(7.95, 0.80, 1.65, 0.60, r"$\phi\to K^+K^-$",
        fc="#e8f8f5", ec="#16a085", fs=9)
    arrow(7.75, 1.10, 7.95, 1.10)

    # Delta M
    box(9.75, 0.80, 1.10, 0.60, r"$\Delta M$ fit",
        fc="#fdedec", ec="#c0392b", fs=9)
    arrow(9.60, 1.10, 9.75, 1.10)

    ax.text(0.15, 5.78, "Belle 2003-style $D_{sJ}$ reconstruction (simplified)",
            fontsize=13, fontweight="bold", ha="left")
    fig.text(0.99, 0.01,
             "Schematic, not to scale. For planning only.",
             ha="right", va="bottom", fontsize=7, color="#7f8c8d")
    fig.tight_layout()
    fig.savefig(FIG / "fig_chain.png")
    plt.close(fig)


if __name__ == "__main__":
    toy_hist(
        mean=0.3487, sigma=0.0071, n_sig=761, n_bkg=1500,
        xmin=0.10, xmax=0.60, nbins=50, seed=11,
        xlabel=r"$\Delta M(D_s^+ \pi^0)$ [GeV]",
        title=r"$D_{sJ}(2317)^+ \to D_s^+ \pi^0$ (toy)",
        annotation="Belle 2003: N = 761 ± 44 ± 30\nm = 2317.2 MeV",
        outname="fig_dm_dspi0.png",
    )
    toy_hist(
        mean=0.3441, sigma=0.0058, n_sig=126, n_bkg=520,
        xmin=0.10, xmax=0.60, nbins=50, seed=12,
        xlabel=r"$\Delta M(D_s^{*+} \pi^0)$ [GeV]",
        title=r"$D_{sJ}(2457)^+ \to D_s^{*+} \pi^0$ (toy)",
        annotation="Belle 2003: N = 126 ± 25 ± 12\nm = 2456.5 MeV",
        outname="fig_dm_dsstpi0.png",
    )
    toy_hist(
        mean=0.4910, sigma=0.0080, n_sig=152, n_bkg=420,
        xmin=0.35, xmax=0.65, nbins=50, seed=13,
        xlabel=r"$\Delta M(D_s^+ \gamma)$ [GeV]",
        title=r"$D_{sJ}(2457)^+ \to D_s^+ \gamma$ (toy)",
        annotation="Belle 2003: N = 152 ± 18\nm = 2459.5 MeV",
        outname="fig_dm_dsgamma.png",
    )
    toy_hist(
        mean=0.4914, sigma=0.0058, n_sig=59.7, n_bkg=480,
        xmin=0.35, xmax=0.65, nbins=50, seed=14,
        xlabel=r"$\Delta M(D_s^+ \pi^+ \pi^-)$ [GeV]",
        title=r"$D_{sJ}(2457)^+ \to D_s^+ \pi^+ \pi^-$ (toy)",
        annotation="Belle 2003: N = 59.7 ± 11.5\nplus $D_{s1}(2536)$: 56.5 ± 13.4",
        outname="fig_dm_dspipi.png",
        extra_peak=(0.5700, 0.0060, 56.5),
    )
    combined_plot()
    yields_plot()
    chain_plot()
    print("figures written to", FIG)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Belle II Title 6: B -> Dbar(*) D_s1(2460), D_s1 -> D_s pi pi
Baseline: D_s -> phi pi, phi -> K K; B+ -> D*0bar D_s1+, B0 -> D*- D_s1+

STATUS: skeleton, not yet validated on KEKCC.
All cuts are INITIAL values and must be optimized with MC.

Usage:
    basf2 -n 1000 steering_ntuple.py
or import build_path() from a b2luigi task.
"""

import basf2 as b2
import modularAnalysis as ma
import vertex as vx
from variables import variables as vm
from stdV0s import stdKshorts


def add_aliases():
    """Aliases for nested daughters. D_s1 is assumed to be daughter(1) of B."""
    # B-level
    vm.addAlias("B_Mbc", "Mbc")
    vm.addAlias("B_deltaE", "deltaE")
    vm.addAlias("B_M", "M")
    vm.addAlias("B_pstar", "p*")
    vm.addAlias("B_chiProb", "chiProb")
    vm.addAlias("B_dr", "dr")
    vm.addAlias("B_dz", "dz")
    vm.addAlias("B_cosTheta", "cosTheta")
    vm.addAlias("BDT", "extraInfo(BDT)")

    # D_s1 = B daughter 1
    vm.addAlias("Ds1_M", "daughter(1, M)")
    vm.addAlias("Ds1_pstar", "daughter(1, p*)")
    vm.addAlias("Ds1_chiProb", "daughter(1, chiProb)")

    # D_s1 daughters: 0 = D_s, 1 = pi+, 2 = pi-
    vm.addAlias("Ds_M", "daughter(1, daughter(0, M))")
    vm.addAlias("Ds_pstar", "daughter(1, daughter(0, p*))")
    vm.addAlias("Ds_sigDist", "daughter(1, daughter(0, significanceOfDistance))")

    for name, idx in [("pip", 1), ("pim", 2)]:
        vm.addAlias(f"{name}_pstar", f"daughter(1, daughter({idx}, p*))")
        vm.addAlias(f"{name}_px", f"daughter(1, daughter({idx}, px))")
        vm.addAlias(f"{name}_py", f"daughter(1, daughter({idx}, py))")
        vm.addAlias(f"{name}_pz", f"daughter(1, daughter({idx}, pz))")
        vm.addAlias(f"{name}_E", f"daughter(1, daughter({idx}, E))")

    # D_s 4-momentum
    for var in ["px", "py", "pz", "E"]:
        vm.addAlias(f"Ds_{var}", f"daughter(1, daughter(0, {var}))")


def build_path(input_files, output_bc="ntuple_Bc.root", output_bn="ntuple_Bn.root"):
    main = b2.Path()

    ma.inputMdstList(
        environmentType="default",
        filelist=input_files,
        path=main,
    )

    # ---------- final-state particles ----------
    ma.fillParticleList(
        "pi+:good",
        "thetaInCDCAcceptance and dr < 0.5 and abs(dz) < 2.0 "
        "and pionID > 0.5 and p > 0.08 and pt > 0.05",
        path=main,
    )
    ma.fillParticleList(
        "K+:good",
        "thetaInCDCAcceptance and dr < 0.5 and abs(dz) < 2.0 "
        "and kaonID > 0.5 and p > 0.10 and pt > 0.05",
        path=main,
    )
    ma.fillParticleList(
        "gamma:good",
        "E > 0.05 and inCDCAcceptance and abs(clusterTiming) < 200 "
        "and clusterE1E9 > 0.4",
        path=main,
    )
    ma.reconstructDecay(
        "pi0:good -> gamma:good gamma:good",
        "0.11 < M < 0.15",
        path=main,
    )
    stdKshorts(path=main)

    # ---------- D_s -> phi pi ----------
    ma.reconstructDecay(
        "phi:good -> K+:good K-:good",
        "1.00 < M < 1.04",
        path=main,
    )
    ma.reconstructDecay(
        "D_s+:phi -> phi:good pi+:good",
        "1.93 < M < 2.00",
        path=main,
    )
    vx.treeFit("D_s+:phi", conf_level=0.001, updateAllDaughters=True, path=main)
    ma.applyCuts(
        "D_s+:phi",
        "[p* > 1.2] and [chiProb > 0.001] and [significanceOfDistance > 2.0]",
        path=main,
    )

    # ---------- D0 and D* ----------
    ma.reconstructDecay(
        "anti-D0:kp -> K+:good pi-:good",
        "1.83 < M < 1.90",
        path=main,
    )
    vx.treeFit("anti-D0:kp", conf_level=0.001, updateAllDaughters=True, path=main)
    ma.applyCuts(
        "anti-D0:kp",
        "[p* > 1.0] and [chiProb > 0.001] and [significanceOfDistance > 2.0]",
        path=main,
    )

    ma.reconstructDecay(
        "anti-D*0:g -> anti-D0:kp gamma:good",
        "0.130 < M - daughter(0, M) < 0.155",
        path=main,
    )
    vx.treeFit("anti-D*0:g", conf_level=0.001, updateAllDaughters=True, path=main)

    ma.reconstructDecay(
        "D*-:pi -> anti-D0:kp pi-:good",
        "0.140 < M - daughter(0, M) < 0.150",
        path=main,
    )
    vx.treeFit("D*-:pi", conf_level=0.001, updateAllDaughters=True, path=main)

    # ---------- D_s1 -> D_s pi pi ----------
    ma.reconstructDecay(
        "D_s1+:sig -> D_s+:phi pi+:good pi-:good",
        "2.42 < M < 2.50",
        path=main,
    )
    vx.treeFit("D_s1+:sig", conf_level=0.001, updateAllDaughters=True, path=main)
    ma.applyCuts(
        "D_s1+:sig",
        "[p* > 1.0] and [chiProb > 0.001]",
        path=main,
    )

    # ---------- B candidates ----------
    ma.reconstructDecay(
        "B+:dstDs1 -> anti-D*0:g D_s1+:sig",
        "5.20 < Mbc < 5.30 and abs(deltaE) < 0.10",
        path=main,
    )
    ma.reconstructDecay(
        "B+:dDs1 -> anti-D0:kp D_s1+:sig",
        "5.20 < Mbc < 5.30 and abs(deltaE) < 0.10",
        path=main,
    )
    ma.reconstructDecay(
        "B0:dsDs1 -> D*-:pi D_s1+:sig",
        "5.20 < Mbc < 5.30 and abs(deltaE) < 0.10",
        path=main,
    )

    ma.reconstructDecay(
        "D-:kpipi -> K+:good pi-:good pi-:good",
        "1.85 < M < 1.89",
        path=main,
    )
    vx.treeFit("D-:kpipi", conf_level=0.001, updateAllDaughters=True, path=main)
    ma.reconstructDecay(
        "B0:dDs1 -> D-:kpipi D_s1+:sig",
        "5.20 < Mbc < 5.30 and abs(deltaE) < 0.10",
        path=main,
    )

    # merge charge conjugates
    ma.copyLists(
        "Bc:all",
        ["B+:dstDs1", "B+:dDs1", "B-:dstDs1", "B-:dDs1"],
        path=main,
    )
    ma.copyLists(
        "Bn:all",
        ["B0:dsDs1", "B0:dDs1", "anti-B0:dsDs1", "anti-B0:dDs1"],
        path=main,
    )

    vx.treeFit("Bc:all", conf_level=0.001, updateAllDaughters=True, path=main)
    vx.treeFit("Bn:all", conf_level=0.001, updateAllDaughters=True, path=main)

    for name in ["Bc:all", "Bn:all"]:
        ma.applyCuts(
            name,
            "[chiProb > 0.001] and [dr < 1.0] and [abs(dz) < 2.0] "
            "and [p* < 0.6] and [abs(cosTheta) < 0.9]",
            path=main,
        )
        ma.rankByHighest(name, "chiProb", numBest=1, path=main)

    # ---------- ROE / continuum suppression ----------
    ma.buildRestOfEvent("Bc:all", path=main)
    ma.buildContinuumSuppression("Bc:all", "all", path=main)
    ma.buildRestOfEvent("Bn:all", path=main)
    ma.buildContinuumSuppression("Bn:all", "all", path=main)

    # Uncomment after training Ds1_BDT.root:
    # mva = b2.register_module("MVAExpert")
    # mva.param("listNames", ["Bc:all", "Bn:all"])
    # mva.param("extraInfoName", "BDT")
    # mva.param("identifier", "Ds1_BDT.root")
    # main.add_module(mva)

    # ---------- ntuple ----------
    add_aliases()
    variables = [
        "B_Mbc", "B_deltaE", "B_M", "B_pstar", "B_chiProb", "B_dr", "B_dz",
        "B_cosTheta", "nTracks", "R2", "cosTBTO", "charge",
        "Ds1_M", "Ds1_pstar", "Ds1_chiProb",
        "Ds_M", "Ds_pstar", "Ds_sigDist",
        "pip_pstar", "pim_pstar",
        "pip_px", "pip_py", "pip_pz", "pip_E",
        "pim_px", "pim_py", "pim_pz", "pim_E",
        "Ds_px", "Ds_py", "Ds_pz", "Ds_E",
    ]

    ma.variablesToNtuple(
        "Bc:all",
        variables,
        treename="Bc",
        filename=output_bc,
        path=main,
    )
    ma.variablesToNtuple(
        "Bn:all",
        variables,
        treename="Bn",
        filename=output_bn,
        path=main,
    )

    return main


if __name__ == "__main__":
    path = build_path(["/path/to/your/mdst_or_udst.root"])
    b2.process(path)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RooFit yield-fit skeleton for m(D_s pi pi).

STATUS: skeleton. Units are GeV. Not validated on real data.
"""

import ROOT

ROOT.gROOT.SetBatch(True)
ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)


def fit(input_file="ntuple_Bc.root", tree_name="Bc", output_pdf="fit_Ds1_M.pdf"):
    f = ROOT.TFile.Open(input_file)
    tree = f.Get(tree_name)

    x = ROOT.RooRealVar("Ds1_M", "m(D_{s}#pi#pi)", 2.40, 2.52, "GeV")
    x.setBins(60)

    # Signal: Voigtian = BW (x) Gaussian
    mean = ROOT.RooRealVar("mean", "mean", 2.4595, 2.450, 2.470)
    width = ROOT.RooRealVar("width", "natural width [GeV]", 0.0015, 0.0001, 0.005)
    sigma = ROOT.RooRealVar("sigma", "resolution [GeV]", 0.004, 0.001, 0.020)
    width.setConstant(True)
    sig = ROOT.RooVoigtian("sig", "signal", x, mean, width, sigma)

    # Background: exponential
    tau = ROOT.RooRealVar("tau", "tau", -8.0, -50.0, -0.1)
    bkg = ROOT.RooExponential("bkg", "background", x, tau)

    nsig = ROOT.RooRealVar("nsig", "N_{sig}", 100, 0, 1e6)
    nbkg = ROOT.RooRealVar("nbkg", "N_{bkg}", 1000, 0, 1e6)

    model = ROOT.RooAddPdf(
        "model", "sig+bkg",
        ROOT.RooArgList(sig, bkg),
        ROOT.RooArgList(nsig, nbkg),
        ROOT.kTRUE,
    )

    data = ROOT.RooDataSet("data", "data", tree, ROOT.RooArgSet(x))
    model.fitTo(data, ROOT.RooFit.Save(True), ROOT.RooFit.PrintLevel(-1))

    frame = x.frame(ROOT.RooFit.Title("B^{+} #rightarrow #bar{D}^{*0} D_{s1}^{+}"))
    data.plotOn(frame, ROOT.RooFit.Name("data"))
    model.plotOn(frame, ROOT.RooFit.Name("fit"))
    frame.Draw()

    c = ROOT.TCanvas("c", "c", 800, 600)
    frame.Draw()
    c.SaveAs(output_pdf)

    print("N_sig =", nsig.getVal(), "+/-", nsig.getError())
    print("N_bkg =", nbkg.getVal(), "+/-", nbkg.getError())
    return model, data


if __name__ == "__main__":
    fit()

#!/usr/bin/env bash
# FastBDT training skeleton for continuum suppression.
# STATUS: skeleton; variable names must match the ntuple.

set -euo pipefail

SIG=${SIG:-signal_ntuple.root}
BKG=${BKG:-bkg_ntuple.root}
OUT=${OUT:-Ds1_BDT.root}

# 1) merge signal/background and split train/test
basf2_mva_merge_mc \
  -s "${SIG}" \
  -b "${BKG}" \
  -o train.root \
  --ftest 0.2

# 2) train FastBDT
basf2_mva_teacher \
  --datafiles train_train.root \
  --treename tree \
  --identifier "${OUT}" \
  --variables \
      R2 cosTBTO thrust foxWolframR2 nTracks \
      B_pstar B_cosTheta Ds1_pstar Ds1_chiProb \
      Ds_sigDist Ds_pstar D0_pstar Dst_pstar \
  --target_variable isSignal \
  --method FastBDT

# 3) evaluate
basf2_mva_evaluate.py \
  -id "${OUT}" \
  -data train_test.root \
  -tree tree \
  -out bdt_report.zip

echo "done: ${OUT}"

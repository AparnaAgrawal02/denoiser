#!/bin/bash
# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# authors: adiyoss and adefossez
#SBATCH -A research
#SBATCH -n 5
#SBATCH -w gnode019
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=2G
#SBATCH --time=4-00:00:00
#SBATCH --mail-type=END
python train.py \
  dset=marathi \
  #demucs.causal=1 \
  #demucs.hidden=64 \
  #demucs.resample=4 \
  #batch_size=128 \
  #revecho=1 \
  #segment=10 \
  #stride=2 \
  #shift=16000 \
  #shift_same=True \
  #epochs=250 \
  $@

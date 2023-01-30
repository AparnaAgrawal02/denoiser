# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
# author: adefossez and adiyoss

import json
import logging
import os
import re
import random
import pandas as pd


from .audio import Audioset

logger = logging.getLogger(__name__)


def match_dns(noisy, clean):
    """match_dns.
    Match noisy and clean DNS dataset filenames.

    :param noisy: list of the noisy filenames
    :param clean: list of the clean filenames
    """
    logger.debug("Matching noisy and clean for dns dataset")
    noisydict = {}
    extra_noisy = []
    for path, size in noisy:
        match = re.search(r'fileid_(\d+)\.wav$', path)
        if match is None:
            # maybe we are mixing some other dataset in
            extra_noisy.append((path, size))
        else:
            noisydict[match.group(1)] = (path, size)
    noisy[:] = []
    extra_clean = []
    copied = list(clean)
    clean[:] = []
    for path, size in copied:
        match = re.search(r'fileid_(\d+)\.wav$', path)
        if match is None:
            extra_clean.append((path, size))
        else:
            noisy.append(noisydict[match.group(1)])
            clean.append((path, size))
    extra_noisy.sort()
    extra_clean.sort()
    clean += extra_clean
    noisy += extra_noisy


def match_files(noisy, clean, matching="sort"):
    """ match_files.
    Sort files to match noisy and clean filenames.
    :param noisy: list of the noisy filenames
    :param clean: list of the clean filenames
    :param matching: the matching function, at this point only sort is supported
    
    if matching == "dns":
        # dns dataset filenames don't match when sorted, we have to manually match them
        match_dns(noisy, clean)
    elif matching == "sort":
        noisy.sort()
        clean.sort()
    else:
        raise ValueError(f"Invalid value for matching {matching}")
    """
    l1 = len(noisy)
    l2 = len(clean)
    new_noisy = []
    new_clean = []
    for i in range(l1):
        for j in range(l2):
            new_noisy.append(noisy[i])
            new_clean.append(clean[j])
    return new_noisy, new_clean



class NoisyCleanSet:
    def __init__(self, json_dir, matching="sort", length=None, stride=None,
                 pad=True, sample_rate=None):
        """__init__.

        :param json_dir: directory containing both clean.json and noisy.json
        :param matching: matching function for the files
        :param length: maximum sequence length
        :param stride: the stride used for splitting audio sequences
        :param pad: pad the end of the sequence with zeros
        :param sample_rate: the signals sampling rate
        """
        noisy_json = os.path.join(json_dir, 'noisy.json')
        clean_json = os.path.join(json_dir, 'clean.json')

        print("load pe phat raha")
        
        self.noisy = pd.read_json(noisy_json)
      
        self.clean =  pd.read_json(clean_json)
        print(self.noisy)

        self.noisy, self.clean = match_files(self.noisy, self.clean, matching)
        print("fine")

        kw = {'clean_files':self.clean,'length': length, 'stride': stride, 'pad': pad, 'sample_rate': sample_rate}
        print("x")
        self.clean_set = Audioset(self.clean, **kw)
        print("x1")
        self.noisy_set = Audioset(self.noisy, **kw,tag = 'noisy')
        print("x2")

        assert len(self.clean_set) == len(self.noisy_set)

    def __getitem__(self, index):
        print("data")
        print(self.noisy_set[index].shape,self.clean_set[index].shape)
        return self.noisy_set[index], self.clean_set[index]

    def __len__(self):
        return len(self.noisy_set)


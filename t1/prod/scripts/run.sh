#!/bin/bash

source /usr/local/Miniconda3-py37_4.8.3-Linux-x86_64/etc/profile.d/conda.sh && conda activate rnsp
cd ~/GIT_REPOS/rnsp/t1/prod && python3 main.py $1
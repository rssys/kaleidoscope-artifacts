#!/bin/bash

dir="$1"

python3 plot-scripts/plot_ptd.py "$1"
python3 plot-scripts/plot_cfi.py "$1"
python3 plot-scripts/plot_cfi2.py "$1"

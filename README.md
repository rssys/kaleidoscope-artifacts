# Kaleidoscope Artifacts


Please set up passwordless `sudo` on your machine.

## Compile LLVM and Binutils

This script compiles the Gold linker from `binutils` and the modified LLVM 12
compiler toolchain. Note that this will update your system linker to the Gold
linker.

`./llvm-setup.sh`

## Run Kaleidoscope on the application bitcodes

We provide the bitcodes in the directory `kaleidoscope-pta/apps/`. The 
applications can be compiled to regenerate the bitcodes as denoted below.

`./run-kaleidoscope.sh`

This script generates a results directory in
`kaleidoscope-pta/apps/full-results-dir_MM_DD_YY`. Note the name of the
directory generated. 


## Generate the result plots and CSV files

Run the following command to generate the plots and the CSV files for the reduction
in the average number of points-to sets and CFI targets. 

`./plot.sh ./kaleidoscope-pta/apps/full-results-dir_MM_DD_YY`

## [Optional] Compile the applications to generate the bitcodes

TODO.

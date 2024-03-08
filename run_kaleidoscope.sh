#!/bin/bash

for subdir in "./kaleidoscope-pta/apps"/*/; do
	  # Trim the trailing slash for display or further processing
		subdir="${subdir%/}"
		echo "Processing $subdir"
		echo "$PWD"
		cd $subdir
		source run.cmd
		cd ../../..
done

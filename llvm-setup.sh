#!/bin/bash
# Script to set up binutils for Gold linker, LLVM, etc

# compile the gold linker

sudo apt-get -y install libgmp-dev libmpfr-dev
git clone --depth 1 git://sourceware.org/git/binutils-gdb.git binutils
mkdir gold-build
cd gold-build
../binutils/configure --enable-gold --enable-plugins --disable-werror
make all-gold -j8

cd ..
# change the system-wide linker after backing it up
sudo mv /usr/bin/ld /usr/bin/ld-bkup
sudo ln -s "$(realpath ./gold-build/gold/ld-new)" /usr/bin/ld

# Build the LLVM compiler
git submodule update --init
cd llvm12

export BINUTILS_INC_DIR="$(realpath ./binutils/include)"
cmake -S llvm -B debug-build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug \
-DLLVM_ENABLE_DUMP=ON  -DLLVM_ENABLE_PROJECTS="compiler-rt;clang;lld" \
-DLLVM_BINUTILS_INCDIR=$BINUTILS_INC_DIR  -DCMAKE_INSTALL_PREFIX=/usr/
cd debug-build
make -j8
cd ../..

echo "export PATH=\"$(realpath ./llvm12/debug-build/bin):\$PATH\"" >> ~/.bashrc
echo "export LLVM_DIR=\"$(realpath ./llvm12/debug-build/bin)\"" >> ~/.bashrc
LLVM_DIR=$(realpath ./llvm12/debug-build/bin)
echo "export LLVM_HOME=$LLVM_DIR" >> ~/.bashrc
source ~/.bashrc

cd kaleidoscope-pta
./build.sh debug
cd ../

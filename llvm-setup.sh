#!/bin/bash
# Script to set up binutils for Gold linker, LLVM, etc

# compile the gold linker

set -x
apt-get -y install libgmp-dev libmpfr-dev

yes | ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N ""
ssh-keyscan -H github.com >> ~/.ssh/known_hosts
ssh -o StrictHostKeyChecking=no user@github.com

git clone --depth 1 git://sourceware.org/git/binutils-gdb.git binutils
mkdir gold-build
cd gold-build
../binutils/configure --enable-gold --enable-plugins --disable-werror
make all-gold -j8

cd ..
# change the system-wide linker after backing it up
apt reinstall binutils
mv /usr/bin/ld /usr/bin/ld-bkup
ln -s "$(realpath ./gold-build/gold/ld-new)" /usr/bin/ld

# Build the LLVM compiler
git submodule update --init
cd llvm12

export BINUTILS_INC_DIR="$(realpath ../binutils/include)"
cmake -S llvm -B debug-build -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug \
	-DLLVM_ENABLE_DUMP=ON  -DLLVM_ENABLE_PROJECTS="compiler-rt;clang;lld" \
	-DLLVM_BINUTILS_INCDIR=$BINUTILS_INC_DIR  -DCMAKE_INSTALL_PREFIX=/usr/
cd debug-build
make -j8
exit 0
cd ../..

echo "export PATH=\"$(realpath ./llvm12/debug-build/bin):\$PATH\"" >>
~/.bashrc
echo "export LLVM_DIR=\"$(realpath ./llvm12/debug-build/bin)\"" >> ~/.bashrc
LLVM_DIR=$(realpath ./llvm12/debug-build/bin)
echo "export LLVM_HOME=$LLVM_DIR" >> ~/.bashrc
source ~/.bashrc

cd kaleidoscope-pta
./build.sh debug
cd ../

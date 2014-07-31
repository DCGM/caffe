CAFFE_DIR=`pwd`

export LD_LIBRARY_PATH="/usr/local/share/cuda/lib64:${CAFFE_DIR}/dep/lib/:$LD_LIBRARY_PATH"
export PATH=${CAFFE_DIR}/dep/bin/:$PATH

cp Makefile.config.SGE Makefile.config
make -j 8
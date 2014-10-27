cd dep
INSTALL_PATH=`pwd`

#svn checkout http://google-glog.googlecode.com/svn/trunk/ google-glog-read-only
cd google-glog-read-only
./configure --prefix="$INSTALL_PATH" && make -j 6 && make install

cd "$INSTALL_PATH"
git clone https://code.google.com/p/gflags/
cd gflags
mkdir build
cd build
CXXFLAGS=-fPIC cmake -DCMAKE_INSTALL_PREFIX:PATH="$INSTALL_PATH" ../
make -j 6
make install

cd "$INSTALL_PATH"
wget http://protobuf.googlecode.com/files/protobuf-2.5.0.tar.gz  
tar xzf protobuf-2.5.0.tar.gz
#svn checkout http://protobuf.googlecode.com/svn/trunk/ protobuf-read-only
cd protobuf-2.5.0
./autogen.sh
./configure --prefix="$INSTALL_PATH" && make -j 6 && make install

cd "$INSTALL_PATH"
git clone https://code.google.com/p/leveldb/
cd leveldb
make -j 6
cp libleveldb* ../lib
cp -r ./include/leveldb ../include/

cd "$INSTALL_PATH"
git clone https://github.com/google/snappy.git
cd snappy
./autogen.sh
./configure --prefix="$INSTALL_PATH" && make -j 6 && make install

cd "$INSTALL_PATH"
git clone https://git.gitorious.org/mdb/mdb.git 
cd ./mdb/libraries/liblmdb 
make 
cp lib* "$INSTALL_PATH/lib"
cp *.h "$INSTALL_PATH/include"


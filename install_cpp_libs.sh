sudo rm -rf /usr/local/include/Sopra*
sudo rm /usr/local/lib/libSopra*


set -e

cd /tmp
git clone https://github.com/SoPra-Team-17/LibClient
cd LibClient
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

cd /tmp
git clone git@github.com:SoPra-Team-17/WebsocketCPP.git
cd WebsocketCPP
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

cd /tmp
git clone git@github.com:SoPra-Team-17/LibCommon.git
cd LibCommon
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

sudo ldconfig

cd /usr/lib/
sudo ln -s /usr/local/lib/libSopraClient.so
sudo ln -s /usr/local/lib/libSopraCommon.so
sudo ln -s /usr/local/lib/libSopraNetwork.so
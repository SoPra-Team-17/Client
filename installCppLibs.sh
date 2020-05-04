#!/usr/bin/env bash

# delete prev. downloads
sudo rm -rf /tmp/json /tmp/WebsocketCPP /tmp/LibCommon/ /tmp/LibClient/ /tmp/libwebsockets/

# delete symbolic links and installed libs with headers
sudo rm -rf /usr/lib/libSopra*
sudo rm -rf /usr/local/lib/libSopra*
sudo rm -rf /usr/local/include/Sopra*

# Exit the script if any command fails
set -e


# Dependencies from LibCommon
# libuuid
sudo apt install uuid-dev
# nlohmann json
dpkg -s nlohmann-json-dev > /dev/null 2>&1 && {
  echo "nlohmann-json-dev already installed"
} || {
  echo "nlohmann-json-dev not installed. Installing now..."
  cd /tmp
  git clone --depth 1 https://github.com/nlohmann/json.git
  cd json
  mkdir build && cd build
  cmake -DJSON_BuildTests=false ..
  make -j$(nproc)
  sudo make install
}



# Dependencies from WebsocketCPP
# Libwebsockets
sudo apt install libssl-dev
if [ ! -f /usr/local/lib/libwebsockets.so ]; then
    echo "Libwebsockets not installed. Installing now"
    cd /tmp
    git clone https://github.com/warmcat/libwebsockets.git
    cd libwebsockets
    mkdir build && cd build
    cmake ..
    make -j$(nproc)
    sudo make install
fi


# Install LibCommon
cd /tmp
git clone https://github.com/SoPra-Team-17/LibCommon.git
cd LibCommon
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

# Install WebsocketCPP
cd /tmp
git clone https://github.com/SoPra-Team-17/WebsocketCPP.git
cd WebsocketCPP
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

# Install LibClient
cd /tmp
git clone https://github.com/SoPra-Team-17/LibClient.git
cd LibClient
git submodule update --init
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

# symbolic links for cppyy
cd /usr/lib
sudo ln -s /usr/local/lib/libSopraCommon.so
sudo ln -s /usr/local/lib/libSopraNetwork.so
sudo ln -s /usr/local/lib/libSopraClient.so


sudo ldconfig
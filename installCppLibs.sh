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
sudo apt -y install uuid-dev
# xsel for pasting to textentry field
sudo apt -y install xsel
# nlohmann json
dpkg -s nlohmann-json-dev > /dev/null 2>&1 && {
  echo "nlohmann-json-dev already installed"
} || {
  echo "nlohmann-json-dev not installed. Installing now..."
  cd /tmp
  git clone --depth 1 -b v3.7.3 https://github.com/nlohmann/json.git
  cd json
  mkdir build && cd build
  cmake -DJSON_BuildTests=false ..
  make -j$(nproc)
  sudo make install
}


cd /tmp
git clone https://github.com/SoPra-Team-17/LibCommon.git
cd LibCommon
git checkout v0.1.2
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

# Install WebsocketCPP
cd /tmp
git clone https://github.com/SoPra-Team-17/WebsocketCPP.git
cd WebsocketCPP
./installDependencies.sh
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

# Install LibClient
cd /tmp
git clone https://github.com/SoPra-Team-17/LibClient.git
cd LibClient
git checkout v0.1.3
git submodule update --init
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

sudo ldconfig

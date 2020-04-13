//
// Created by Carolin on 13.04.2020.
//

#include "Network.hpp"


void Network::sentSetText(std::string t) {
    model.setText(t);
}

std::string Network::receivedGetText() {
    callback.receivedGetText(model);
}
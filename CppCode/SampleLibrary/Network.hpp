//
// Created by Carolin on 13.04.2020.
//

#ifndef SAMPLELIBRARY_NETWORK_HPP
#define SAMPLELIBRARY_NETWORK_HPP

#include "CallbackClass.hpp"
#include "Model.hpp"

class Network {
public:
    Network(CallbackClass *c, Model *m) {
        callback = c;
        model = m;
    }

    CallbackClass *callback;
    Model *model;

    void sentSetText(std::string t);

    std::string receivedGetText();

    Model* getModel();

};


#endif //SAMPLELIBRARY_NETWORK_HPP

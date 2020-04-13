//
// Created by Carolin on 13.04.2020.
//

#ifndef SAMPLELIBRARY_CALLBACKCLASS_HPP
#define SAMPLELIBRARY_CALLBACKCLASS_HPP

#include <string>
#include <iostream>
#include "Model.hpp"
//#include "Network.hpp"

class CallbackClass {
public:

    CallbackClass() = default;

    virtual ~CallbackClass() = default;

    Model model = Model();

    virtual void receivedGetText() = 0;

};


#endif //SAMPLELIBRARY_CALLBACKCLASS_HPP

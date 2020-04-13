//
// Created by Carolin on 13.04.2020.
//

#ifndef SAMPLELIBRARY_CALLBACKCLASS_HPP
#define SAMPLELIBRARY_CALLBACKCLASS_HPP

#include <string>
#include "Model.hpp"

class CallbackClass {
public:

    explicit CallbackClass() = default;

    void receivedGetText(Model m);

};


#endif //SAMPLELIBRARY_CALLBACKCLASS_HPP
